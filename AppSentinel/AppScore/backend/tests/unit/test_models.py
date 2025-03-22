import pytest
from app.models import SecurityScore, ScoreCategory, ScoreMetric

def test_create_security_score():
    score = SecurityScore(
        application_id=1,
        total_score=85.5,
        assessment_date="2024-01-01",
        assessor_id="user123",
        status="COMPLETED"
    )
    assert score.total_score == 85.5
    assert score.status == "COMPLETED"

def test_create_score_category():
    category = ScoreCategory(
        name="Authentication",
        weight=0.3,
        description="Authentication security measures"
    )
    assert category.name == "Authentication"
    assert category.weight == 0.3

def test_create_score_metric():
    metric = ScoreMetric(
        category_id=1,
        name="Password Policy",
        score=4,
        max_score=5,
        notes="Strong password requirements implemented"
    )
    assert metric.name == "Password Policy"
    assert metric.score == 4
    assert metric.max_score == 5

def test_calculate_weighted_score():
    category = ScoreCategory(
        name="Authentication",
        weight=0.3
    )
    metric = ScoreMetric(
        category_id=category.id,
        score=4,
        max_score=5
    )
    weighted_score = (metric.score / metric.max_score) * category.weight * 100
    assert weighted_score == 24.0  # (4/5) * 0.3 * 100
