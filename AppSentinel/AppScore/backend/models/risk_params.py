from sqlalchemy import Column, Integer, Float, JSON
from extensions import db

class RiskParameters(db.Model):
    __tablename__ = 'risk_parameters'

    id = Column(Integer, primary_key=True)
    
    # Weights for internal applications (0-1)
    internal_weights = Column(JSON, nullable=False, default={
        'code_review': 0.3,
        'security_testing': 0.2,
        'dependency_scanning': 0.2,
        'deployment_security': 0.15,
        'access_control': 0.15
    })
    
    # Thresholds for internal applications (0-100)
    internal_thresholds = Column(JSON, nullable=False, default={
        'high_risk': 60,
        'medium_risk': 80,
        'low_risk': 90
    })
    
    # Weights for vendor applications (0-1)
    vendor_weights = Column(JSON, nullable=False, default={
        'vendor_assessment': 0.3,
        'contract_security': 0.2,
        'integration_security': 0.2,
        'data_handling': 0.15,
        'support_sla': 0.15
    })
    
    # Thresholds for vendor applications (0-100)
    vendor_thresholds = Column(JSON, nullable=False, default={
        'high_risk': 60,
        'medium_risk': 80,
        'low_risk': 90
    })

    def to_dict(self):
        return {
            'id': self.id,
            'internal_weights': self.internal_weights,
            'internal_thresholds': self.internal_thresholds,
            'vendor_weights': self.vendor_weights,
            'vendor_thresholds': self.vendor_thresholds
        }

    @staticmethod
    def get_default():
        """Get or create default risk parameters"""
        default_params = RiskParameters.query.first()
        if not default_params:
            default_params = RiskParameters()
            db.session.add(default_params)
            db.session.commit()
        return default_params
