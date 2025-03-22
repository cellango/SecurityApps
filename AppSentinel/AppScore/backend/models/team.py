from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from extensions import db

class Team(db.Model):
    __tablename__ = 'teams'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)
    applications = relationship('Application', back_populates='team', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'applicationCount': self.applications.count(),
            'averageScore': sum(app.security_score or 0 for app in self.applications) / self.applications.count() if self.applications.count() > 0 else 0
        }
