from typing import Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from models.score_history import ScoreHistory
from .rules_engine import RulesEngine
from .ml_engine import SecurityScorePredictor

class SecurityScoreService:
    def __init__(self, session: Session):
        self.session = session
        self.rules_engine = RulesEngine()
        self.ml_predictor = SecurityScorePredictor(session)
        self.rules_weight = 0.7  # 70% weight to rules-based score
        self.ml_weight = 0.3     # 30% weight to ML-based score

    async def compute_score(self, application_id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        """Compute security score using both rules and ML"""
        try:
            # Get rules-based score
            rules_result = self.rules_engine.compute_score(data)
            rules_score = rules_result['score']

            # Get ML-based score
            ml_score = self.ml_predictor.predict(data)

            # Compute weighted final score
            final_score = (rules_score * self.rules_weight) + (ml_score * self.ml_weight)

            # Store score history
            score_history = ScoreHistory(
                application_id=application_id,
                rules_score=rules_score,
                ml_score=ml_score,
                final_score=final_score,
                features=data,
                metadata={
                    'triggered_rules': rules_result['triggered_rules'],
                    'ml_features': self.ml_predictor.feature_columns
                }
            )
            self.session.add(score_history)
            self.session.commit()

            return {
                'final_score': final_score,
                'rules_score': rules_score,
                'ml_score': ml_score,
                'rules_details': rules_result['triggered_rules'],
                'score_id': score_history.id,
                'timestamp': datetime.utcnow().isoformat()
            }

        except Exception as e:
            self.session.rollback()
            print(f"Error computing score: {str(e)}")
            raise

    async def train_ml_model(self):
        """Train ML model using historical data"""
        try:
            # Get historical data
            history = self.session.query(ScoreHistory).all()
            
            if not history:
                return {"status": "error", "message": "No historical data available for training"}

            # Prepare training data
            training_data = [h.features for h in history]
            actual_scores = [h.final_score for h in history]

            # Train model
            training_result = self.ml_predictor.train(training_data, actual_scores)

            return {
                "status": "success",
                "model_version": training_result['version'],
                "metrics": training_result['metrics']
            }

        except Exception as e:
            print(f"Error training model: {str(e)}")
            return {"status": "error", "message": str(e)}

    async def get_score_history(self, application_id: int, limit: int = 10) -> List[Dict]:
        """Get score history for an application"""
        try:
            history = (
                self.session.query(ScoreHistory)
                .filter_by(application_id=application_id)
                .order_by(ScoreHistory.created_at.desc())
                .limit(limit)
                .all()
            )
            
            return [h.to_dict() for h in history]

        except Exception as e:
            print(f"Error fetching score history: {str(e)}")
            return []
