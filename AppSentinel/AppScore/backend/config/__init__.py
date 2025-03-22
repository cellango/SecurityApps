"""
Configuration management module for the Security Score Card application.
"""

from enum import Enum
import os
from typing import Dict
from dotenv import load_dotenv
from services.secrets_manager import get_secrets_manager

# Load environment variables from .env file
load_dotenv()

class Environment(Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Config:
    """Base configuration class"""
    # Application settings
    APP_ENV = Environment(os.getenv('FLASK_ENV', 'development'))
    DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 't')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    
    # AWS Settings
    AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')
    
    # Database settings
    DB_HOST = os.getenv('DB_HOST', 'postgres')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'security_score_card')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
    
    @property
    def DATABASE_URL(self):
        """Constructs database URL from components"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    # Security settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key-change-in-production')
    
    # API settings
    API_VERSION = '1.0'
    API_PREFIX = '/api/v1'
    
    # Logging settings
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    @property
    def is_development(self):
        """Check if environment is development"""
        return os.getenv('FLASK_ENV', 'development') == 'development'

    @property
    def is_production(self):
        """Check if environment is production"""
        return os.getenv('FLASK_ENV', 'development') == 'production'

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class StagingConfig(Config):
    """Staging configuration"""
    DEBUG = False
    LOG_LEVEL = 'INFO'

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    # AWS Secrets Manager secret names
    SECRET_NAMES = {
        'DB_PASSWORD': 'prod/security-score-card/db-password',
        'SECRET_KEY': 'prod/security-score-card/secret-key',
        'JWT_SECRET_KEY': 'prod/security-score-card/jwt-secret-key'
    }
    
    def __init__(self):
        """Initialize production configuration with secrets from AWS"""
        super().__init__()
        self._load_secrets()
    
    def _load_secrets(self):
        """Load secrets from AWS Secrets Manager"""
        try:
            secrets_manager = get_secrets_manager()
            secrets = secrets_manager.get_secrets(list(self.SECRET_NAMES.values()))
            
            # Map secret values to config attributes
            secret_mapping = {
                self.SECRET_NAMES['DB_PASSWORD']: 'DB_PASSWORD',
                self.SECRET_NAMES['SECRET_KEY']: 'SECRET_KEY',
                self.SECRET_NAMES['JWT_SECRET_KEY']: 'JWT_SECRET_KEY'
            }
            
            for secret_name, value in secrets.items():
                if secret_name in secret_mapping:
                    setattr(self, secret_mapping[secret_name], value)
                    
        except Exception as e:
            # Log the error but don't expose secret details
            import logging
            logging.error(f"Failed to load secrets from AWS: {str(e)}")
            raise RuntimeError("Failed to load production secrets. Check logs for details.")

# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'staging': StagingConfig,
    'production': ProductionConfig
}

def get_config(environment: str = None) -> Config:
    """Get configuration based on environment"""
    if environment is None:
        environment = os.getenv('FLASK_ENV', 'development')
    return config_by_name[environment]()

# Get current configuration
current_env = os.getenv('FLASK_ENV', 'development')
current_config = get_config(current_env)
