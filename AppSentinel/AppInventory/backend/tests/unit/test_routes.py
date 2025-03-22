import pytest
from app import create_app
from app.models import db, Application

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_get_applications(client):
    response = client.get('/api/applications')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_application(client):
    data = {
        "name": "Test App",
        "description": "Test Description",
        "application_type": "WEB",
        "state": "DEVELOPMENT",
        "owner_id": "user123"
    }
    headers = {
        "X-User-ID": "test_user",
        "X-Jira-Ticket": "JIRA-123"
    }
    response = client.post('/api/applications', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json["name"] == "Test App"

def test_get_audit_logs(client):
    response = client.get('/api/audit-logs')
    assert response.status_code == 200
    assert isinstance(response.json, list)
