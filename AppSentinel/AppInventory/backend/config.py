import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_LEVEL = 'INFO'
    # Use either SQLALCHEMY_DATABASE_URI or DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    """Development configuration."""
    FLASK_ENV = 'development'
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/appinventory_dev'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('TEST_DATABASE_URL') or 'postgresql://postgres:postgres@localhost:5432/appinventory_test'

class ProductionConfig(Config):
    """Production configuration."""
    FLASK_ENV = 'production'
    DEBUG = False
    LOG_LEVEL = 'INFO'
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
