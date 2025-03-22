from . import db
from enum import Enum
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.ext.declarative import declared_attr
import json
from app.utils.logger import logger

class ApplicationType(Enum):
    INTERNAL = 'internal'
    VENDOR = 'vendor'

class ApplicationState(Enum):
    PLANNING = 'planning'
    DEVELOPMENT = 'development'
    TESTING = 'testing'
    PRODUCTION = 'production'
    RETIRED = 'retired'

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

class ControlStatus(Enum):
    NOT_IMPLEMENTED = 'not_implemented'
    PLANNED = 'planned'
    PARTIALLY_IMPLEMENTED = 'partially_implemented'
    IMPLEMENTED = 'implemented'

class AuditableMixin:
    """Mixin for auditable models"""
    
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    @declared_attr
    def created_by(cls):
        return db.Column(db.String(100))
    
    @declared_attr
    def updated_by(cls):
        return db.Column(db.String(100))

class Application(db.Model, AuditableMixin):
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    application_type = db.Column(db.String(50), nullable=False)
    owner_id = db.Column(db.String(50))
    owner_email = db.Column(db.String(100))
    department_name = db.Column(db.String(100))
    team_name = db.Column(db.String(100))
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
    
    security_controls = db.relationship('SecurityControl', secondary='application_controls', lazy='dynamic')
    application_controls = db.relationship('ApplicationControl', back_populates='application')

    def __init__(self, name, description=None, owner_id=None, owner_email=None, department_name=None, team_name=None, test_score=None, test_score_date=None, last_security_review=None, next_security_review=None, deployment_date=None, last_update_date=None, vendor_name=None, vendor_contact=None, contract_expiration=None, data_classification=None, authentication_method=None, requires_2fa=None, application_type=None):
        logger.debug(f"Creating new Application instance", 
                    name=name, owner_id=owner_id, owner_email=owner_email, department_name=department_name, team_name=team_name, test_score=test_score, test_score_date=test_score_date, last_security_review=last_security_review, next_security_review=next_security_review, deployment_date=deployment_date, last_update_date=last_update_date, vendor_name=vendor_name, vendor_contact=vendor_contact, contract_expiration=contract_expiration, data_classification=data_classification, authentication_method=authentication_method, requires_2fa=requires_2fa, application_type=application_type)
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.owner_email = owner_email
        self.department_name = department_name
        self.team_name = team_name
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
        logger.debug(f"Updating Application {self.id}", 
                    application_id=self.id, updates=kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        logger.info(f"Application {self.id} updated successfully", 
                   application_id=self.id)

    def to_dict(self):
        logger.debug(f"Converting Application {self.id} to dictionary", 
                    application_id=self.id)
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'owner_id': self.owner_id,
            'owner_email': self.owner_email,
            'department_name': self.department_name,
            'team_name': self.team_name,
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
            'application_type': self.application_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

class SecurityControl(db.Model):
    __tablename__ = 'security_controls'
    
    id = db.Column(db.Integer, primary_key=True)
    control_id = db.Column(db.String(50), unique=True, nullable=False)
    family = db.Column(db.Enum(ControlFamily), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    applicable_states = db.Column(db.String(200))  # Comma-separated list of states
    
    applications = db.relationship('Application', secondary='application_controls', lazy='dynamic')
    application_controls = db.relationship('ApplicationControl', back_populates='control')

    def __init__(self, control_id, family, title, description=None, applicable_states=None):
        logger.debug(f"Creating new SecurityControl instance", 
                    control_id=control_id, family=family, title=title, applicable_states=applicable_states)
        self.control_id = control_id
        self.family = family
        self.title = title
        self.description = description
        self.applicable_states = applicable_states

    def update(self, **kwargs):
        logger.debug(f"Updating SecurityControl {self.id}", 
                    control_id=self.id, updates=kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        logger.info(f"SecurityControl {self.id} updated successfully", 
                   control_id=self.id)

    def to_dict(self):
        logger.debug(f"Converting SecurityControl {self.id} to dictionary", 
                    control_id=self.id)
        return {
            'id': self.id,
            'control_id': self.control_id,
            'family': self.family.value,
            'title': self.title,
            'description': self.description,
            'applicable_states': self.applicable_states
        }

class ApplicationControl(db.Model):
    __tablename__ = 'application_controls'
    
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), primary_key=True)
    control_id = db.Column(db.Integer, db.ForeignKey('security_controls.id'), primary_key=True)
    status = db.Column(db.Enum(ControlStatus), nullable=False, default=ControlStatus.NOT_IMPLEMENTED)
    notes = db.Column(db.Text)
    implementation_date = db.Column(db.DateTime)
    last_review_date = db.Column(db.DateTime)
    
    application = db.relationship('Application', back_populates='application_controls')
    control = db.relationship('SecurityControl', back_populates='application_controls')

    def __init__(self, application_id, control_id, status=None, notes=None, implementation_date=None, last_review_date=None):
        logger.debug(f"Creating new ApplicationControl instance", 
                    application_id=application_id, control_id=control_id, status=status, notes=notes, implementation_date=implementation_date, last_review_date=last_review_date)
        self.application_id = application_id
        self.control_id = control_id
        self.status = status
        self.notes = notes
        self.implementation_date = implementation_date
        self.last_review_date = last_review_date

    def update(self, **kwargs):
        logger.debug(f"Updating ApplicationControl {self.application_id}-{self.control_id}", 
                    application_id=self.application_id, control_id=self.control_id, updates=kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        logger.info(f"ApplicationControl {self.application_id}-{self.control_id} updated successfully", 
                   application_id=self.application_id, control_id=self.control_id)

    def to_dict(self):
        logger.debug(f"Converting ApplicationControl {self.application_id}-{self.control_id} to dictionary", 
                    application_id=self.application_id, control_id=self.control_id)
        return {
            'application_id': self.application_id,
            'control_id': self.control_id,
            'status': self.status.value,
            'notes': self.notes,
            'implementation_date': self.implementation_date.isoformat() if self.implementation_date else None,
            'last_review_date': self.last_review_date.isoformat() if self.last_review_date else None
        }

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(20), nullable=False)  # INSERT, UPDATE, DELETE
    changed_fields = db.Column(db.JSON)
    user_id = db.Column(db.String(100))  # User who made the change
    jira_ticket = db.Column(db.String(20))  # JIRA ticket reference
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, table_name, record_id, action, changed_fields=None, user_id=None, jira_ticket=None):
        logger.debug(f"Creating new AuditLog entry", 
                    table_name=table_name, record_id=record_id, action=action, user_id=user_id, jira_ticket=jira_ticket)
        self.table_name = table_name
        self.record_id = record_id
        self.action = action
        self.changed_fields = changed_fields
        self.user_id = user_id
        self.jira_ticket = jira_ticket

    def to_dict(self):
        logger.debug(f"Converting AuditLog {self.id} to dictionary", 
                    log_id=self.id)
        return {
            'id': self.id,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'action': self.action,
            'changed_fields': self.changed_fields,
            'user_id': self.user_id,
            'jira_ticket': self.jira_ticket,
            'timestamp': self.timestamp.isoformat()
        }

class ExportFilterPreset(db.Model):
    __tablename__ = 'export_filter_presets'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    team = db.Column(db.String(100))
    control_family = db.Column(db.Enum(ControlFamily))
    status = db.Column(db.Enum(ControlStatus))
    implementation_date_start = db.Column(db.DateTime)
    implementation_date_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    last_used = db.Column(db.DateTime)

    def __init__(self, name, department=None, team=None, control_family=None, status=None, implementation_date_start=None, implementation_date_end=None):
        logger.debug(f"Creating new ExportFilterPreset instance", 
                    name=name, department=department, team=team, control_family=control_family, status=status, implementation_date_start=implementation_date_start, implementation_date_end=implementation_date_end)
        self.name = name
        self.department = department
        self.team = team
        self.control_family = control_family
        self.status = status
        self.implementation_date_start = implementation_date_start
        self.implementation_date_end = implementation_date_end

    def update(self, **kwargs):
        logger.debug(f"Updating ExportFilterPreset {self.id}", 
                    preset_id=self.id, updates=kwargs)
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        logger.info(f"ExportFilterPreset {self.id} updated successfully", 
                   preset_id=self.id)

    def to_dict(self):
        logger.debug(f"Converting ExportFilterPreset {self.id} to dictionary", 
                    preset_id=self.id)
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'team': self.team,
            'control_family': self.control_family.value if self.control_family else None,
            'status': self.status.value if self.status else None,
            'implementation_date_start': self.implementation_date_start.isoformat() if self.implementation_date_start else None,
            'implementation_date_end': self.implementation_date_end.isoformat() if self.implementation_date_end else None,
            'created_at': self.created_at.isoformat(),
            'last_used': self.last_used.isoformat() if self.last_used else None
        }

def track_modifications(mapper, connection, target):
    """Track model modifications for audit logging"""
    state = db.inspect(target)
    audited_fields = {}
    
    # Get the changes
    for attr in state.attrs:
        hist = attr.history
        if hist.has_changes():
            if hist.deleted and hist.added:
                # Handle updates
                audited_fields[attr.key] = {
                    'old': hist.deleted[0] if len(hist.deleted) > 0 else None,
                    'new': hist.added[0] if len(hist.added) > 0 else None
                }
            elif hist.added:
                # Handle inserts
                audited_fields[attr.key] = {
                    'old': None,
                    'new': hist.added[0] if len(hist.added) > 0 else None
                }
    
    if audited_fields:
        # Create audit log entry
        audit = AuditLog(
            table_name=target.__tablename__,
            record_id=target.id if hasattr(target, 'id') else None,
            action='UPDATE' if state.persistent else 'INSERT',
            changed_fields=audited_fields,
            # These will be set by the application context
            user_id=getattr(target, '_audit_user_id', None),
            jira_ticket=getattr(target, '_audit_jira_ticket', None)
        )
        db.session.add(audit)

def track_deletions(mapper, connection, target):
    """Track model deletions for audit logging"""
    audit = AuditLog(
        table_name=target.__tablename__,
        record_id=target.id if hasattr(target, 'id') else None,
        action='DELETE',
        changed_fields=None,
        user_id=getattr(target, '_audit_user_id', None),
        jira_ticket=getattr(target, '_audit_jira_ticket', None)
    )
    db.session.add(audit)

event.listen(Application, 'after_insert', track_modifications)
event.listen(Application, 'after_update', track_modifications)
event.listen(Application, 'after_delete', track_deletions)
