from app import db
from enum import Enum
from app.utils import logger
from .base import AuditableMixin

class ControlFamily(Enum):
    ACCESS_CONTROL = 'access_control'
    AUDIT_LOGGING = 'audit_logging'
    AUTHENTICATION = 'authentication'
    AUTHORIZATION = 'authorization'
    CONFIGURATION = 'configuration'
    CRYPTOGRAPHY = 'cryptography'
    DATA_PROTECTION = 'data_protection'
    ERROR_HANDLING = 'error_handling'
    INPUT_VALIDATION = 'input_validation'
    MALWARE_DEFENSE = 'malware_defense'
    NETWORK_SECURITY = 'network_security'
    PASSWORD_POLICY = 'password_policy'
    PATCH_MANAGEMENT = 'patch_management'
    SECURE_CODING = 'secure_coding'
    SESSION_MANAGEMENT = 'session_management'
    VULNERABILITY_MANAGEMENT = 'vulnerability_management'

class SecurityControl(db.Model, AuditableMixin):
    __tablename__ = 'security_controls'
    
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.String(50), unique=True, nullable=False)
    family = db.Column(db.Enum(ControlFamily), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    applicable_states = db.Column(db.String(200))
    
    applications = db.relationship('Application', secondary='application_controls', lazy='dynamic')
    application_controls = db.relationship('ApplicationControl', back_populates='control')

    def __init__(self, control_id, family, title, description=None, applicable_states=None):
        logger.debug("Creating new SecurityControl instance - control_id: %s, family: %s, title: %s, applicable_states: %s",
                    control_id, family, title, applicable_states)
        self.control_id = control_id
        self.family = family
        self.title = title
        self.description = description
        self.applicable_states = applicable_states

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'control_id': self.control_id,
            'family': self.family.value if self.family else None,
            'title': self.title,
            'description': self.description,
            'applicable_states': self.applicable_states,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
