from app import db
from datetime import datetime
from app.utils import logger
from .security_control import ControlFamily
from .application_control import ControlStatus

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

    def __init__(self, name, department=None, team=None, control_family=None, status=None,
                 implementation_date_start=None, implementation_date_end=None):
        logger.debug("Creating new ExportFilterPreset instance - name: %s, department: %s, team: %s, control_family: %s, status: %s, implementation_date_start: %s, implementation_date_end: %s" % 
                    (name, department, team, control_family, status, implementation_date_start, implementation_date_end))
        self.name = name
        self.department = department
        self.team = team
        self.control_family = control_family
        self.status = status
        self.implementation_date_start = implementation_date_start
        self.implementation_date_end = implementation_date_end

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department,
            'team': self.team,
            'control_family': self.control_family.value if self.control_family else None,
            'status': self.status.value if self.status else None,
            'implementation_date_start': self.implementation_date_start.isoformat() if self.implementation_date_start else None,
            'implementation_date_end': self.implementation_date_end.isoformat() if self.implementation_date_end else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_used': self.last_used.isoformat() if self.last_used else None
        }
