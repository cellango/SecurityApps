from app import db
from enum import Enum
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
from app.utils import logger
from .base import AuditableMixin

class ApplicationType(Enum):
    WEB = 'web'
    MOBILE = 'mobile'
    DESKTOP = 'desktop'
    API = 'api'
    SERVICE = 'service'


class Application(db.Model, AuditableMixin):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    application_type = db.Column(db.String(50), nullable=False, default='web')
    owner_id = db.Column(db.String(50))
    owner_email = db.Column(db.String(100))
    department_name = db.Column(db.String(100))
    team_name = db.Column(db.String(100))
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'))
    test_score = db.Column(db.Float)
    test_score_date = db.Column(db.DateTime)
    last_security_review = db.Column(db.DateTime)
    next_security_review = db.Column(db.DateTime)
    deployment_date = db.Column(db.DateTime)
    last_update_date = db.Column(db.DateTime)
    vendor_name = db.Column(db.String(100))
    vendor_contact = db.Column(db.String(100))
    contract_expiration = db.Column(db.DateTime)
    data_classification = db.Column(db.String(50))
    authentication_method = db.Column(db.String(50))
    requires_2fa = db.Column(db.Boolean)
    
    # Relationships
    team = db.relationship('Team', back_populates='applications', overlaps="teams,applications")
    security_controls = db.relationship('SecurityControl', secondary='application_controls', lazy='dynamic')
    application_controls = db.relationship('ApplicationControl', back_populates='application')

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, description=None, owner_id=None, owner_email=None, department_name=None, 
                 team_name=None, team_id=None, test_score=None, test_score_date=None, last_security_review=None, 
                 next_security_review=None, deployment_date=None, last_update_date=None, vendor_name=None, 
                 vendor_contact=None, contract_expiration=None, data_classification=None, authentication_method=None, 
                 requires_2fa=None, application_type=None):
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.owner_email = owner_email
        self.department_name = department_name
        self.team_name = team_name
        self.team_id = team_id
        self.test_score = test_score
        self.test_score_date = test_score_date
        self.last_security_review = last_security_review
        self.next_security_review = next_security_review
        self.deployment_date = deployment_date
        self.last_update_date = last_update_date
        self.vendor_name = vendor_name
        self.vendor_contact = vendor_contact
        self.contract_expiration = contract_expiration
        self.data_classification = data_classification
        self.authentication_method = authentication_method
        self.requires_2fa = requires_2fa
        self.application_type = application_type

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'application_type': self.application_type,
            'owner_id': self.owner_id,
            'owner_email': self.owner_email,
            'department_name': self.department_name,
            'team_name': self.team_name,
            'team_id': self.team_id,
            'test_score': self.test_score,
            'test_score_date': self.test_score_date.isoformat() if self.test_score_date else None,
            'last_security_review': self.last_security_review.isoformat() if self.last_security_review else None,
            'next_security_review': self.next_security_review.isoformat() if self.next_security_review else None,
            'deployment_date': self.deployment_date.isoformat() if self.deployment_date else None,
            'last_update_date': self.last_update_date.isoformat() if self.last_update_date else None,
            'vendor_name': self.vendor_name,
            'vendor_contact': self.vendor_contact,
            'contract_expiration': self.contract_expiration.isoformat() if self.contract_expiration else None,
            'data_classification': self.data_classification,
            'authentication_method': self.authentication_method,
            'requires_2fa': self.requires_2fa,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Application {self.name}>'
