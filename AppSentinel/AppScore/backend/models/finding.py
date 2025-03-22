from datetime import datetime
from extensions import db

class Finding(db.Model):
    __tablename__ = 'findings'

    id = db.Column(db.Integer, primary_key=True)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.String(50))  # e.g., 'critical', 'high', 'medium', 'low'
    status = db.Column(db.String(50))    # e.g., 'open', 'closed', 'in_progress'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    remediation_plan = db.Column(db.Text)
    remediation_deadline = db.Column(db.DateTime)
    assigned_to = db.Column(db.String(255))

    # Relationships
    application = db.relationship('Application', backref=db.backref('findings', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'application_id': self.application_id,
            'title': self.title,
            'description': self.description,
            'severity': self.severity,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'remediation_plan': self.remediation_plan,
            'remediation_deadline': self.remediation_deadline.isoformat() if self.remediation_deadline else None,
            'assigned_to': self.assigned_to
        }
