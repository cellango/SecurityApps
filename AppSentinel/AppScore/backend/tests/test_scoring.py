import pytest
from datetime import datetime
from unittest.mock import Mock, patch
from models.score_history import ScoreHistory
from scoring.rules_engine import RulesEngine
from scoring.ml_engine import SecurityScorePredictor
from scoring.score_service import SecurityScoreService

@pytest.fixture
def mock_session():
    return Mock()

@pytest.fixture
def rules_engine():
    return RulesEngine()

@pytest.fixture
def mock_ml_predictor(mock_session):
    predictor = SecurityScorePredictor(mock_session)
    predictor.predict = Mock(return_value=85.0)
    return predictor

@pytest.fixture
def score_service(mock_session):
    return SecurityScoreService(mock_session)

def test_rules_engine_scoring():
    """Test rules-based scoring"""
    engine = RulesEngine()
    
    # Test case with critical vulnerabilities
    data = {
        'critical_vulns': 2,
        'high_vulns': 1,
        'outdated_deps_percentage': 15,
        'compliance_violations': 0
    }
    
    result = engine.compute_score(data)
    assert result['score'] <= 60  # Score should be reduced due to critical vulns
    assert len(result['triggered_rules']) > 0
    
    # Test case with no vulnerabilities
    clean_data = {
        'critical_vulns': 0,
        'high_vulns': 0,
        'outdated_deps_percentage': 5,
        'compliance_violations': 0
    }
    
    clean_result = engine.compute_score(clean_data)
    assert clean_result['score'] == 100
    assert len(clean_result['triggered_rules']) == 0

@pytest.mark.asyncio
async def test_score_service_computation(score_service, mock_ml_predictor):
    """Test score computation service"""
    with patch('scoring.score_service.SecurityScorePredictor', return_value=mock_ml_predictor):
        data = {
            'critical_vulns': 1,
            'high_vulns': 2,
            'medium_vulns': 3,
            'low_vulns': 4,
            'outdated_deps_percentage': 15,
            'compliance_violations': 0,
            'security_hotspots': 2,
            'code_coverage': 80,
            'duplicate_lines': 5
        }
        
        result = await score_service.compute_score(1, data)
        
        assert 'final_score' in result
        assert 'rules_score' in result
        assert 'ml_score' in result
        assert result['ml_score'] == 85.0  # From mock
        assert isinstance(result['timestamp'], str)

def test_score_history_model():
    """Test ScoreHistory model"""
    score = ScoreHistory(
        application_id=1,
        rules_score=90.0,
        ml_score=85.0,
        final_score=88.5,
        features={
            'critical_vulns': 0,
            'high_vulns': 1
        },
        metadata={
            'triggered_rules': []
        }
    )
    
    score_dict = score.to_dict()
    assert score_dict['application_id'] == 1
    assert score_dict['rules_score'] == 90.0
    assert score_dict['ml_score'] == 85.0
    assert score_dict['final_score'] == 88.5
    assert 'features' in score_dict
    assert 'metadata' in score_dict

@pytest.mark.asyncio
async def test_ml_predictor_training(mock_session):
    """Test ML model training"""
    predictor = SecurityScorePredictor(mock_session)
    
    training_data = [
        {
            'critical_vulns': 0,
            'high_vulns': 1,
            'medium_vulns': 2,
            'low_vulns': 3,
            'outdated_deps_percentage': 10,
            'compliance_violations': 0,
            'security_hotspots': 1,
            'code_coverage': 85,
            'duplicate_lines': 4
        },
        {
            'critical_vulns': 1,
            'high_vulns': 2,
            'medium_vulns': 3,
            'low_vulns': 4,
            'outdated_deps_percentage': 20,
            'compliance_violations': 1,
            'security_hotspots': 2,
            'code_coverage': 75,
            'duplicate_lines': 6
        }
    ]
    
    scores = [95.0, 75.0]
    
    # Mock the model save operations
    with patch('joblib.dump'):
        result = await predictor.train(training_data, scores)
        
        assert 'version' in result
        assert 'metrics' in result
        assert 'feature_importance' in result['metrics']

@pytest.mark.asyncio
async def test_score_service_error_handling(score_service):
    """Test error handling in score service"""
    with pytest.raises(Exception):
        await score_service.compute_score(999, {})  # Invalid application ID

def test_rules_engine_invalid_data():
    """Test rules engine with invalid data"""
    engine = RulesEngine()
    
    # Test with missing required fields
    data = {'some_invalid_field': 123}
    result = engine.compute_score(data)
    
    assert result['score'] == 100  # Should default to perfect score
    assert len(result['triggered_rules']) == 0

def test_rules_engine_edge_cases():
    """Test rules engine edge cases"""
    engine = RulesEngine()
    
    # Test with extreme values
    data = {
        'critical_vulns': 1000,
        'high_vulns': 1000,
        'outdated_deps_percentage': 100,
        'compliance_violations': 1000
    }
    
    result = engine.compute_score(data)
    assert result['score'] == 0  # Should be minimum score
    assert len(result['triggered_rules']) > 0

    # Test with negative values
    data = {
        'critical_vulns': -1,
        'high_vulns': -1,
        'outdated_deps_percentage': -10,
        'compliance_violations': -1
    }
    
    result = engine.compute_score(data)
    assert result['score'] == 100  # Should ignore negative values
