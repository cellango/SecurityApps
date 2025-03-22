from app import db
from enum import Enum
from app.utils import logger
from .base import AuditableMixin

class ControlStatus(Enum):
    NOT_IMPLEMENTED = 'not_implemented'
    PLANNED = 'planned'
    PARTIALLY_IMPLEMENTED = 'partially_implemented'
    IMPLEMENTED = 'implemented'

class ApplicationControl(db.Model, AuditableMixin):
    __tablename__ = 'application_controls'
    
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), primary_key=True)
    control_id = db.Column(db.Integer, db.ForeignKey('security_controls.id'), primary_key=True)
    status = db.Column(db.Enum(ControlStatus), nullable=False, default=ControlStatus.NOT_IMPLEMENTED)
    notes = db.Column(db.Text)
    implementation_date = db.Column(db.DateTime)
    last_review_date = db.Column(db.DateTime)
    
    application = db.relationship('Application', back_populates='application_controls')
    control = db.relationship('SecurityControl', back_populates='application_controls', overlaps="applications,security_controls")

    def __init__(self, application_id, control_id, status=None, notes=None, implementation_date=None, last_review_date=None):
        logger.debug(f"Creating new ApplicationControl instance", 
                    application_id=application_id, control_id=control_id, status=status, notes=notes,
                    implementation_date=implementation_date, last_review_date=last_review_date)
        self.application_id = application_id
        self.control_id = control_id
        self.status = status
        self.notes = notes
        self.implementation_date = implementation_date
        self.last_review_date = last_review_date

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            'application_id': self.application_id,
            'control_id': self.control_id,
            'status': self.status.value if self.status else None,
            'notes': self.notes,
            'implementation_date': self.implementation_date.isoformat() if self.implementation_date else None,
            'last_review_date': self.last_review_date.isoformat() if self.last_review_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
