import pytest
from app import create_app
from app.models import db, SecurityScore, ScoreCategory

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_get_security_scores(client):
    response = client.get('/api/security-scores')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_security_score(client):
    data = {
        "application_id": 1,
        "total_score": 85.5,
        "assessment_date": "2024-01-01",
        "assessor_id": "user123",
        "status": "COMPLETED",
        "metrics": [
            {
                "category_id": 1,
                "name": "Password Policy",
                "score": 4,
                "max_score": 5,
                "notes": "Strong password requirements"
            }
        ]
    }
    headers = {
        "X-User-ID": "test_user",
        "X-Jira-Ticket": "JIRA-123"
    }
    response = client.post('/api/security-scores', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json["total_score"] == 85.5

def test_get_score_categories(client):
    response = client.get('/api/score-categories')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_application_score_history(client):
    response = client.get('/api/applications/1/score-history')
    assert response.status_code == 200
    assert isinstance(response.json, list)
