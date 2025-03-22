"""
PyTest configuration file for secret rotation tests.
"""

import os
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def aws_credentials():
    """Mock AWS credentials for testing"""
    with patch.dict(os.environ, {
        'AWS_ACCESS_KEY_ID': 'testing',
        'AWS_SECRET_ACCESS_KEY': 'testing',
        'AWS_SECURITY_TOKEN': 'testing',
        'AWS_SESSION_TOKEN': 'testing',
        'AWS_DEFAULT_REGION': 'us-east-1'
    }):
        yield

@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mock environment variables for testing"""
    with patch.dict(os.environ, {
        'DB_HOST': 'test-db-host',
        'DB_PORT': '5432',
        'DB_NAME': 'test_db',
        'DB_USER': 'test_user'
    }):
        yield
