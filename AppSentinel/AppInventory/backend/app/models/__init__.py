"""
Models package initialization.
"""
from app import db

# Import models
from .base import AuditableMixin
from .user import User
from .department import Department
from .team import Team
from .application import Application
from .security_control import SecurityControl
from .application_control import ApplicationControl
from .export_filter_preset import ExportFilterPreset
from app.utils import logger

__all__ = [
    'db',
    'User',
    'Department',
    'Team',
    'Application',
    'SecurityControl',
    'ApplicationControl',
    'ExportFilterPreset',
    'logger'
]

def init_models():
    """Initialize all models with SQLAlchemy"""
    from app import db
    db.create_all()