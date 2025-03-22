from app import db
from datetime import datetime
from app.utils import logger

class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    table_name = db.Column(db.String(100), nullable=False)
    record_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(20), nullable=False)
    changed_fields = db.Column(db.JSON)
    user_id = db.Column(db.String(100))
    jira_ticket = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, table_name, record_id, action, changed_fields=None, user_id=None, jira_ticket=None):
        logger.debug(f"Creating new AuditLog entry", 
                    table_name=table_name, record_id=record_id, action=action,
                    user_id=user_id, jira_ticket=jira_ticket)
        self.table_name = table_name
        self.record_id = record_id
        self.action = action
        self.changed_fields = changed_fields
        self.user_id = user_id
        self.jira_ticket = jira_ticket

    def to_dict(self):
        return {
            'id': self.id,
            'table_name': self.table_name,
            'record_id': self.record_id,
            'action': self.action,
            'changed_fields': self.changed_fields,
            'user_id': self.user_id,
            'jira_ticket': self.jira_ticket,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
