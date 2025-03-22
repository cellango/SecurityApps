from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, JSON, ForeignKey, String, Boolean
from sqlalchemy.orm import relationship
from extensions import db

class ScoreHistory(db.Model):
    __tablename__ = 'score_history'

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    score = Column(Integer, nullable=False)
    rules_score = Column(Integer)
    ml_score = Column(Integer)
    details = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

    application = relationship('Application', back_populates='score_history')

    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'score': self.score,
            'rules_score': self.rules_score,
            'ml_score': self.ml_score,
            'details': self.details,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class MLModelVersion(db.Model):
    __tablename__ = 'ml_model_versions'

    id = Column(Integer, primary_key=True)
    version = Column(String(50), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
