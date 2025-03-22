"""
Secrets Manager Service

Handles fetching secrets from AWS Secrets Manager.
Can be extended to support other secret management services.
"""

import json
import logging
import os
from abc import ABC, abstractmethod
import boto3
from botocore.exceptions import ClientError
from typing import Dict, Optional

logger = logging.getLogger(__name__)

class SecretsManagerBase(ABC):
    """Abstract base class for secrets management"""
    
    @abstractmethod
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Retrieve a secret by name"""
        pass
    
    @abstractmethod
    def get_secrets(self, secret_names: list) -> Dict[str, str]:
        """Retrieve multiple secrets by name"""
        pass

class AWSSecretsManager(SecretsManagerBase):
    """AWS Secrets Manager implementation"""
    
    def __init__(self):
        """Initialize AWS Secrets Manager client"""
        self.region_name = os.getenv('AWS_REGION', 'us-east-1')
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='secretsmanager',
            region_name=self.region_name
        )
        
    def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Retrieve a secret value from AWS Secrets Manager
        
        Args:
            secret_name: Name or ARN of the secret
            
        Returns:
            Secret value if found, None otherwise
            
        Raises:
            ClientError: If there's an error accessing AWS Secrets Manager
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            if 'SecretString' in response:
                secret = response['SecretString']
                # Handle JSON string secrets
                try:
                    secret_dict = json.loads(secret)
                    # If it's a simple key-value pair, return the value
                    if len(secret_dict) == 1:
                        return next(iter(secret_dict.values()))
                    # Otherwise return the whole JSON string
                    return secret
                except json.JSONDecodeError:
                    # If it's not JSON, return as is
                    return secret
            else:
                logger.warning(f"Secret {secret_name} found but contains no string value")
                return None
                
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                logger.error(f"Secret {secret_name} not found")
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                logger.error(f"Invalid request for secret {secret_name}")
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                logger.error(f"Invalid parameter in request for secret {secret_name}")
            else:
                logger.error(f"Error accessing secret {secret_name}: {str(e)}")
            raise
            
    def get_secrets(self, secret_names: list) -> Dict[str, str]:
        """
        Retrieve multiple secrets from AWS Secrets Manager
        
        Args:
            secret_names: List of secret names or ARNs
            
        Returns:
            Dictionary mapping secret names to their values
        """
        secrets = {}
        for name in secret_names:
            try:
                value = self.get_secret(name)
                if value is not None:
                    secrets[name] = value
            except ClientError as e:
                logger.error(f"Failed to retrieve secret {name}: {str(e)}")
                # Continue with other secrets even if one fails
                continue
        return secrets

class LocalSecretsManager(SecretsManagerBase):
    """Local secrets manager for development/testing"""
    
    def __init__(self, secrets_file: str = None):
        """
        Initialize local secrets manager
        
        Args:
            secrets_file: Path to JSON file containing secrets (optional)
        """
        self.secrets = {}
        if secrets_file and os.path.exists(secrets_file):
            with open(secrets_file, 'r') as f:
                self.secrets = json.load(f)
                
    def get_secret(self, secret_name: str) -> Optional[str]:
        """Get secret from local storage"""
        return self.secrets.get(secret_name)
        
    def get_secrets(self, secret_names: list) -> Dict[str, str]:
        """Get multiple secrets from local storage"""
        return {name: self.secrets.get(name) for name in secret_names if name in self.secrets}

def get_secrets_manager() -> SecretsManagerBase:
    """
    Factory function to get appropriate secrets manager based on environment
    
    Returns:
        SecretsManager instance
    """
    env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return AWSSecretsManager()
    else:
        # For development and staging, use local secrets
        secrets_file = os.getenv('LOCAL_SECRETS_FILE', '.secrets.json')
        return LocalSecretsManager(secrets_file)
