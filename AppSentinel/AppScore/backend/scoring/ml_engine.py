import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Any, Tuple
import joblib
import os
from datetime import datetime
from sqlalchemy.orm import Session
from models.score_history import MLModelVersion

class SecurityScorePredictor:
    def __init__(self, session: Session):
        self.model = None
        self.scaler = None
        self.feature_columns = [
            'critical_vulns', 'high_vulns', 'medium_vulns', 'low_vulns',
            'outdated_deps_percentage', 'compliance_violations',
            'security_hotspots', 'code_coverage', 'duplicate_lines'
        ]
        self.session = session
        self._load_latest_model()

    def _load_latest_model(self):
        """Load the latest active model version"""
        try:
            latest_model = (
                self.session.query(MLModelVersion)
                .filter_by(active=True)
                .order_by(MLModelVersion.created_at.desc())
                .first()
            )

            if latest_model:
                model_path = os.path.join('models', f'model_{latest_model.version}.joblib')
                scaler_path = os.path.join('models', f'scaler_{latest_model.version}.joblib')
                
                self.model = joblib.load(model_path)
                self.scaler = joblib.load(scaler_path)
            else:
                # Initialize new model if none exists
                self.model = RandomForestRegressor(
                    n_estimators=100,
                    max_depth=10,
                    random_state=42
                )
                self.scaler = StandardScaler()
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()

    def prepare_features(self, data: Dict[str, Any]) -> np.ndarray:
        """Prepare features for prediction"""
        features = np.array([[
            data.get(col, 0) for col in self.feature_columns
        ]])
        
        if self.scaler.n_features_in_:
            return self.scaler.transform(features)
        return features

    def predict(self, data: Dict[str, Any]) -> float:
        """Predict security score"""
        features = self.prepare_features(data)
        prediction = self.model.predict(features)[0]
        return max(0, min(100, prediction))

    def train(self, training_data: List[Dict[str, Any]], actual_scores: List[float]):
        """Train the model on historical data"""
        try:
            # Prepare features and targets
            X = np.array([[
                data.get(col, 0) for col in self.feature_columns
            ] for data in training_data])
            y = np.array(actual_scores)

            # Fit scaler and transform features
            X_scaled = self.scaler.fit_transform(X)

            # Train model
            self.model.fit(X_scaled, y)

            # Save new model version
            version = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            model_path = os.path.join('models', f'model_{version}.joblib')
            scaler_path = os.path.join('models', f'scaler_{version}.joblib')

            os.makedirs('models', exist_ok=True)
            joblib.dump(self.model, model_path)
            joblib.dump(self.scaler, scaler_path)

            # Create model version record
            model_version = MLModelVersion(
                version=version,
                model_type='RandomForestRegressor',
                parameters=self.model.get_params(),
                metrics={
                    'feature_importance': self.model.feature_importances_.tolist(),
                    'n_estimators': self.model.n_estimators,
                    'max_depth': self.model.max_depth
                },
                active=True
            )

            # Deactivate other models
            self.session.query(MLModelVersion).filter_by(active=True).update({'active': False})
            self.session.add(model_version)
            self.session.commit()

            return {
                'version': version,
                'metrics': model_version.metrics
            }

        except Exception as e:
            print(f"Error training model: {str(e)}")
            self.session.rollback()
            raise
