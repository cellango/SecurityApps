from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from extensions import db
import logging

class User(db.Model):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    last_login = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Set password hash"""
        try:
            logging.info(f"Setting password for user: {self.username}")
            self.password_hash = generate_password_hash(password)
            logging.info(f"Password hash set: {self.password_hash[:20]}...")
        except Exception as e:
            logging.error(f"Error setting password: {str(e)}", exc_info=True)

    def check_password(self, password):
        """Check if password matches"""
        try:
            logger = logging.getLogger(__name__)
            logger.info(f"[Password Check] Starting password verification for user: {self.username}")
            logger.info(f"[Password Check] Password hash exists: {'yes' if self.password_hash else 'no'}")
            logger.info(f"[Password Check] Stored password hash: {self.password_hash[:20]}...")
            logger.info(f"[Password Check] Input password length: {len(password)}")
            
            if not self.password_hash:
                logger.error("[Password Check] No password hash found")
                return False
                
            result = check_password_hash(self.password_hash, password)
            logger.info(f"[Password Check] Password verification result: {'SUCCESS' if result else 'FAILED'}")
            return result
        except Exception as e:
            logger.error(f"[Password Check] Error during password verification: {str(e)}", exc_info=True)
            return False

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
