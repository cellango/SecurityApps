from datetime import datetime, timedelta
import jwt
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from models.user import User
import logging
import traceback
import secrets
from werkzeug.security import check_password_hash

class AuthService:
    def __init__(self, session: Session, secret_key: str):
        self.session = session
        self.secret_key = secret_key
        self.token_expiry = timedelta(hours=1)  # Shorter expiry for access tokens
        self.refresh_token_expiry = timedelta(days=7)  # Longer expiry for refresh tokens
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def authenticate(self, username: str, password: str = None, refresh: bool = False) -> Optional[Dict[str, Any]]:
        """Authenticate user and return tokens"""
        try:
            self.logger.info(f"=== Starting authentication for user: {username} ===")
            self.logger.info(f"Password provided: {'yes' if password else 'no'}")
            self.logger.info(f"Refresh mode: {refresh}")
            
            if not username:
                self.logger.warning("Missing username")
                return None
            
            # Query user
            user = self.session.query(User).filter_by(username=username).first()
            self.logger.info(f"User found: {'yes' if user else 'no'}")
            
            if not user:
                self.logger.warning(f"User not found: {username}")
                return None
            
            if not user.is_active:
                self.logger.warning(f"Inactive user attempted to login: {username}")
                return None
            
            # Check password if not refreshing
            if not refresh:
                self.logger.info("Checking password...")
                if not password:
                    self.logger.warning("Password not provided")
                    return None
                    
                password_match = user.check_password(password)
                self.logger.info(f"Password verification result: {'SUCCESS' if password_match else 'FAILED'}")
                if not password_match:
                    self.logger.warning("Invalid password")
                    return None
                self.logger.info("Password check passed")
            
            # Update last login
            user.last_login = datetime.utcnow()
            self.session.commit()
            
            # Generate tokens
            token = self._generate_token(user)
            refresh_token = self._generate_refresh_token(user)
            
            self.logger.info("Authentication successful, returning tokens")
            return {
                'access_token': token,
                'refresh_token': refresh_token,
                'user': user.to_dict()
            }
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}", exc_info=True)
            return None

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload if valid"""
        try:
            if not token:
                return None
            
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            
            user_id = payload.get('user_id')
            if not user_id:
                return None
            
            user = self.session.query(User).get(user_id)
            
            if not user or not user.is_active:
                return None
            
            return payload
        except jwt.ExpiredSignatureError:
            self.logger.warning("Token expired")
            return None
        except jwt.InvalidTokenError:
            self.logger.warning("Invalid token")
            return None
        except Exception as e:
            self.logger.error(f"Token verification error: {str(e)}")
            return None

    def verify_refresh_token(self, refresh_token: str) -> Optional[User]:
        """Verify a refresh token and return the associated user"""
        try:
            payload = jwt.decode(refresh_token, self.secret_key, algorithms=['HS256'])
            user_id = payload.get('user_id')
            if not user_id:
                return None
            
            user = self.session.query(User).get(user_id)
            if not user or not user.is_active:
                return None
            
            return user
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
        except Exception as e:
            self.logger.error(f"Error verifying refresh token: {str(e)}", exc_info=True)
            return None

    def refresh_auth_token(self, refresh_token: str) -> Optional[Dict[str, Any]]:
        """Generate new access token using refresh token"""
        try:
            user = self.verify_refresh_token(refresh_token)
            if not user:
                return None
            
            # Generate new tokens
            new_token = self._generate_token(user)
            new_refresh_token = self._generate_refresh_token(user)
            
            return {
                'access_token': new_token,
                'refresh_token': new_refresh_token
            }
        except Exception as e:
            self.logger.error(f"Token refresh error: {str(e)}")
            return None

    def _generate_token(self, user: User) -> str:
        """Generate a JWT token for a user"""
        return jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.utcnow() + self.token_expiry
            },
            self.secret_key,
            algorithm='HS256'
        )

    def _generate_refresh_token(self, user: User) -> str:
        """Generate a refresh token for a user"""
        return jwt.encode(
            {
                'user_id': user.id,
                'exp': datetime.utcnow() + self.refresh_token_expiry
            },
            self.secret_key,
            algorithm='HS256'
        )
