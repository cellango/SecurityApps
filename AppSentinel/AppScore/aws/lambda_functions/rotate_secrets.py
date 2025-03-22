"""
AWS Lambda function for rotating secrets in AWS Secrets Manager.
This function handles the rotation of database passwords and application secrets.
"""

import json
import logging
import os
import boto3
import psycopg2
from botocore.exceptions import ClientError
import string
import random

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def get_secret_dict(secret_value):
    """Parse and return secret dictionary"""
    if 'SecretString' in secret_value:
        return json.loads(secret_value['SecretString'])
    raise ValueError("Secret value is not a string")

def generate_password(length=32):
    """Generate a secure random password"""
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|"
    return ''.join(random.choice(alphabet) for _ in range(length))

def update_database_password(host, port, dbname, user, current_password, new_password):
    """Update the database user password"""
    try:
        # Connect with current password
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=current_password
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Escape special characters in the password
            escaped_password = new_password.replace("'", "''")
            cur.execute(f"ALTER USER {user} WITH PASSWORD '{escaped_password}'")
            
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Failed to update database password: {str(e)}")
        raise

def lambda_handler(event, context):
    """Rotate secrets based on the rotation strategy"""
    
    try:
        # Initialize AWS clients
        session = boto3.session.Session()
        secrets_client = session.client('secretsmanager')
        
        # Get the secret ID from the event
        secret_id = event['SecretId']
        step = event.get('Step', 'createSecret')
        
        # Get the secret value
        secret_value = secrets_client.get_secret_value(SecretId=secret_id)
        current_secret = get_secret_dict(secret_value)
        
        # Handle different types of secrets
        if 'db-password' in secret_id:
            # Database password rotation
            if step == 'createSecret':
                # Generate new password
                new_password = generate_password()
                
                # Create new secret version
                secrets_client.put_secret_value(
                    SecretId=secret_id,
                    ClientRequestToken=event['ClientRequestToken'],
                    SecretString=json.dumps({'password': new_password}),
                    VersionStages=['AWSPENDING']
                )
                
            elif step == 'setSecret':
                # Get pending secret
                pending_secret = get_secret_dict(
                    secrets_client.get_secret_value(
                        SecretId=secret_id,
                        VersionStage='AWSPENDING'
                    )
                )
                
                # Update database password
                update_database_password(
                    host=os.environ['DB_HOST'],
                    port=int(os.environ.get('DB_PORT', 5432)),
                    dbname=os.environ['DB_NAME'],
                    user=os.environ['DB_USER'],
                    current_password=current_secret['password'],
                    new_password=pending_secret['password']
                )
                
            elif step == 'testSecret':
                # Test the new password
                pending_secret = get_secret_dict(
                    secrets_client.get_secret_value(
                        SecretId=secret_id,
                        VersionStage='AWSPENDING'
                    )
                )
                
                # Try connecting with new password
                conn = psycopg2.connect(
                    host=os.environ['DB_HOST'],
                    port=int(os.environ.get('DB_PORT', 5432)),
                    dbname=os.environ['DB_NAME'],
                    user=os.environ['DB_USER'],
                    password=pending_secret['password']
                )
                conn.close()
                
            elif step == 'finishSecret':
                # Mark the secret version as current
                secrets_client.update_secret_version_stage(
                    SecretId=secret_id,
                    VersionStage='AWSCURRENT',
                    MoveToVersionId=event['ClientRequestToken']
                )
                
        else:
            # Application secrets rotation (JWT keys, etc.)
            if step == 'createSecret':
                # Generate new secret
                new_secret = generate_password(64)
                
                # Create new secret version
                secrets_client.put_secret_value(
                    SecretId=secret_id,
                    ClientRequestToken=event['ClientRequestToken'],
                    SecretString=json.dumps({'key': new_secret}),
                    VersionStages=['AWSPENDING']
                )
                
            elif step == 'setSecret':
                # No additional setup needed for application secrets
                pass
                
            elif step == 'testSecret':
                # No specific test for application secrets
                pass
                
            elif step == 'finishSecret':
                # Mark the secret version as current
                secrets_client.update_secret_version_stage(
                    SecretId=secret_id,
                    VersionStage='AWSCURRENT',
                    MoveToVersionId=event['ClientRequestToken']
                )
        
        return {
            'statusCode': 200,
            'body': json.dumps({'message': f'Successfully completed step {step}'})
        }
        
    except Exception as e:
        logger.error(f'Error during secret rotation: {str(e)}')
        raise
