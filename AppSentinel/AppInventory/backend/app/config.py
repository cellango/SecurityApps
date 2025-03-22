import os
import boto3
from botocore.exceptions import ClientError
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_secret(secret_name):
    """Retrieve secret from AWS Secrets Manager"""
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=os.getenv('AWS_REGION', 'us-west-2')
        )
        
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        raise e
    else:
        if 'SecretString' in get_secret_value_response:
            return json.loads(get_secret_value_response['SecretString'])
        else:
            raise ValueError("Secret value is not a string")

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
    
    # JWT Configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev')
    JWT_ACCESS_TOKEN_EXPIRES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600))
    
    # CORS Configuration
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000').split(',')
    
    # Database Configuration
    if os.getenv('FLASK_ENV') == 'production':
        try:
            secret = get_secret(os.getenv('AWS_SECRET_NAME'))
            SQLALCHEMY_DATABASE_URI = (f"postgresql://{secret['username']}:{secret['password']}@"
                                   f"{secret['host']}:{secret['port']}/{secret['dbname']}")
        except Exception as e:
            print(f"Error getting database credentials from Secrets Manager: {e}")
            raise
    else:
        SQLALCHEMY_DATABASE_URI = (f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
                                f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'false').lower() == 'true'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    LOG_LEVEL = 'INFO'
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
