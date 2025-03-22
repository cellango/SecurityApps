"""
Tests for the secret rotation Lambda function.
"""

import json
import pytest
import boto3
import psycopg2
from unittest.mock import Mock, patch, MagicMock
from botocore.exceptions import ClientError
from rotate_secrets import (
    lambda_handler,
    generate_password,
    get_secret_dict,
    update_database_password
)

@pytest.fixture
def mock_secrets_client():
    """Mock AWS Secrets Manager client"""
    with patch('boto3.session.Session') as mock_session:
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        yield mock_client

@pytest.fixture
def mock_db_connection():
    """Mock PostgreSQL connection"""
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value.__enter__.return_value = mock_cursor
        mock_connect.return_value = mock_conn
        yield mock_conn, mock_cursor

def test_generate_password():
    """Test password generation"""
    # Test default length
    password = generate_password()
    assert len(password) == 32
    
    # Test custom length
    custom_length = 64
    password = generate_password(custom_length)
    assert len(password) == custom_length
    
    # Test password complexity
    password = generate_password()
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    assert all([has_upper, has_lower, has_digit, has_special])

def test_get_secret_dict():
    """Test secret dictionary parsing"""
    # Test valid JSON string
    valid_secret = {'SecretString': '{"password": "test123"}'}
    result = get_secret_dict(valid_secret)
    assert result == {"password": "test123"}
    
    # Test invalid secret
    with pytest.raises(ValueError):
        get_secret_dict({})

@patch('psycopg2.connect')
def test_update_database_password(mock_connect):
    """Test database password update"""
    mock_cursor = Mock()
    mock_connect.return_value.cursor.return_value.__enter__.return_value = mock_cursor
    
    # Test successful password update
    result = update_database_password(
        'localhost',
        5432,
        'test_db',
        'test_user',
        'old_pass',
        'new_pass'
    )
    assert result is True
    mock_cursor.execute.assert_called_once()
    
    # Test database error
    mock_connect.side_effect = psycopg2.Error("Database error")
    with pytest.raises(Exception):
        update_database_password(
            'localhost',
            5432,
            'test_db',
            'test_user',
            'old_pass',
            'new_pass'
        )

def test_lambda_handler_create_secret(mock_secrets_client):
    """Test createSecret step of rotation"""
    event = {
        'SecretId': 'prod/security-score-card/db-password',
        'ClientRequestToken': 'test-token',
        'Step': 'createSecret'
    }
    
    # Mock get_secret_value response
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"password": "old-password"}'
    }
    
    response = lambda_handler(event, None)
    
    # Verify secret was created
    mock_secrets_client.put_secret_value.assert_called_once()
    assert response['statusCode'] == 200

def test_lambda_handler_set_secret(mock_secrets_client, mock_db_connection):
    """Test setSecret step of rotation"""
    mock_conn, mock_cursor = mock_db_connection
    
    event = {
        'SecretId': 'prod/security-score-card/db-password',
        'ClientRequestToken': 'test-token',
        'Step': 'setSecret'
    }
    
    # Mock current and pending secret values
    mock_secrets_client.get_secret_value.side_effect = [
        {'SecretString': '{"password": "old-password"}'},
        {'SecretString': '{"password": "new-password"}'}
    ]
    
    with patch.dict('os.environ', {
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user'
    }):
        response = lambda_handler(event, None)
    
    # Verify database password was updated
    mock_cursor.execute.assert_called_once()
    assert response['statusCode'] == 200

def test_lambda_handler_test_secret(mock_secrets_client, mock_db_connection):
    """Test testSecret step of rotation"""
    mock_conn, _ = mock_db_connection
    
    event = {
        'SecretId': 'prod/security-score-card/db-password',
        'ClientRequestToken': 'test-token',
        'Step': 'testSecret'
    }
    
    # Mock pending secret value
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"password": "new-password"}'
    }
    
    with patch.dict('os.environ', {
        'DB_HOST': 'localhost',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user'
    }):
        response = lambda_handler(event, None)
    
    # Verify connection was tested
    mock_conn.close.assert_called_once()
    assert response['statusCode'] == 200

def test_lambda_handler_finish_secret(mock_secrets_client):
    """Test finishSecret step of rotation"""
    event = {
        'SecretId': 'prod/security-score-card/db-password',
        'ClientRequestToken': 'test-token',
        'Step': 'finishSecret'
    }
    
    response = lambda_handler(event, None)
    
    # Verify secret version was updated
    mock_secrets_client.update_secret_version_stage.assert_called_once()
    assert response['statusCode'] == 200

def test_lambda_handler_error_handling(mock_secrets_client):
    """Test error handling in lambda handler"""
    event = {
        'SecretId': 'prod/security-score-card/db-password',
        'ClientRequestToken': 'test-token',
        'Step': 'createSecret'
    }
    
    # Mock AWS error
    mock_secrets_client.get_secret_value.side_effect = ClientError(
        {'Error': {'Code': 'ResourceNotFoundException', 'Message': 'Secret not found'}},
        'GetSecretValue'
    )
    
    with pytest.raises(ClientError):
        lambda_handler(event, None)

@pytest.mark.parametrize('secret_id,step', [
    ('prod/security-score-card/jwt-secret-key', 'createSecret'),
    ('prod/security-score-card/secret-key', 'createSecret'),
])
def test_lambda_handler_application_secrets(mock_secrets_client, secret_id, step):
    """Test rotation of application secrets"""
    event = {
        'SecretId': secret_id,
        'ClientRequestToken': 'test-token',
        'Step': step
    }
    
    mock_secrets_client.get_secret_value.return_value = {
        'SecretString': '{"key": "old-key"}'
    }
    
    response = lambda_handler(event, None)
    
    if step == 'createSecret':
        mock_secrets_client.put_secret_value.assert_called_once()
    
    assert response['statusCode'] == 200
