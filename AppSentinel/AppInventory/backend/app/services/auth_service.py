from datetime import datetime, timedelta
import jwt
from flask import current_app
from app.models.user import User
from app import db
from app.utils.logger import logger

class AuthService:
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate a user with username/password"""
        logger.debug(f"Authenticating user: {username}")
        user = User.query.filter_by(username=username).first()
        
        if not user:
            logger.debug(f"User not found: {username}")
            return None
            
        if not user.check_password(password):
            logger.debug(f"Invalid password for user: {username}")
            return None
            
        logger.debug(f"User authenticated successfully: {username}")
        return user

    @staticmethod
    def generate_token(user):
        """Generate JWT token for authenticated user"""
        logger.debug(f"Generating token for user: {user.id}")
        try:
            payload = {
                'user_id': user.id,
                'username': user.username,
                'role': user.role,
                'exp': datetime.utcnow() + timedelta(days=1)
            }
            token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')
            logger.debug(f"Token generated successfully for user: {user.id}")
            return token
        except Exception as e:
            logger.error(f"Error generating token: {str(e)}")
            return None

    @staticmethod
    def verify_token(token):
        """Verify JWT token and return user"""
        logger.debug("Verifying token")
        try:
            payload = jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(payload['user_id'])
            if not user:
                logger.debug("User not found for token")
                return None
            logger.debug(f"Token verified successfully for user: {user.id}")
            return user
        except jwt.ExpiredSignatureError:
            logger.debug("Token has expired")
            return None
        except jwt.InvalidTokenError as e:
            logger.debug(f"Invalid token: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {str(e)}")
            return None

    @staticmethod
    def create_user(username, email, password, first_name=None, last_name=None, role='user'):
        """Create a new user"""
        logger.debug(f"Creating new user: {username}, email: {email}")
        user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def oauth_authenticate(provider, oauth_id, user_info):
        """Authenticate or create user via OAuth"""
        logger.debug(f"OAuth authentication attempt: {provider}, oauth_id: {oauth_id}")
        user = User.query.filter_by(oauth_provider=provider, oauth_id=oauth_id).first()
        
        if not user:
            # Create new user from OAuth data
            user = User(
                username=user_info.get('email').split('@')[0],  # Use email prefix as username
                email=user_info.get('email'),
                first_name=user_info.get('given_name'),
                last_name=user_info.get('family_name'),
                oauth_provider=provider,
                oauth_id=oauth_id
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new user via OAuth: {user.username}")
        
        user.update_last_login()
        return user
