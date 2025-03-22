import os
from enum import Enum

class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    PRODUCTION = "production"

class Config:
    """Base configuration."""
    APP_ENV = Environment(os.getenv("FLASK_ENV", "development"))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # JWT Settings
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600))  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES", 2592000))  # 30 days

    @property
    def is_development(self):
        return self.APP_ENV == Environment.DEVELOPMENT

    @property
    def is_production(self):
        return self.APP_ENV == Environment.PRODUCTION

    @property
    def is_testing(self):
        return self.APP_ENV == Environment.TESTING

class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/appscore_dev")

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DEBUG = False
    LOG_LEVEL = "INFO"
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/appscore_test")

def get_config():
    """Get configuration based on environment."""
    env = os.getenv("FLASK_ENV", "development")
    configs = {
        "development": DevelopmentConfig(),
        "production": ProductionConfig(),
        "testing": TestingConfig(),
    }
    return configs.get(env, DevelopmentConfig())
