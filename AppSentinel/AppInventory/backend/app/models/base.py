from datetime import datetime
from sqlalchemy.ext.declarative import declared_attr
from app import db

class AuditableMixin:
    """Mixin for auditable models"""
    
    @declared_attr
    def created_at(cls):
        return db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @declared_attr
    def updated_at(cls):
        return db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)