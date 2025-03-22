import pytest
from app.models import Application, SecurityControl, AuditLog
from datetime import datetime

def test_create_application():
    app = Application(
        name="Test App",
        description="Test Description",
        application_type="WEB",
        state="DEVELOPMENT",
        owner_id="user123"
    )
    assert app.name == "Test App"
    assert app.application_type == "WEB"
    assert app.state == "DEVELOPMENT"

def test_create_security_control():
    control = SecurityControl(
        control_id="SEC-001",
        name="Password Policy",
        description="Password must be complex",
        category="Authentication"
    )
    assert control.control_id == "SEC-001"
    assert control.category == "Authentication"

def test_create_audit_log():
    audit = AuditLog(
        table_name="applications",
        record_id=1,
        action="UPDATE",
        changed_fields={"name": "New Name"},
        user_id="user123",
        jira_ticket="JIRA-456"
    )
    assert audit.table_name == "applications"
    assert audit.action == "UPDATE"
    assert audit.changed_fields["name"] == "New Name"
