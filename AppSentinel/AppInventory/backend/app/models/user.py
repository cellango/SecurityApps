from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils.logger import logger


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, username, email, password=None, role='user', first_name=None, last_name=None):
        logger.info(f"Creating new user: {username}")
        self.username = username
        self.email = email
        if password:
            self.set_password(password)
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def set_password(self, password):
        logger.info(f"Setting password for user: {self.username}")
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

    def check_password(self, password):
        logger.info(f"[User.check_password] Checking password for user: {self.username}")
        if not self.password_hash:
            logger.error(f"[User.check_password] No password hash found for user: {self.username}")
            return False
        result = check_password_hash(self.password_hash, password)
        if not result:
            logger.error(f"[User.check_password] Invalid password for user: {self.username}")
        else:
            logger.info(f"[User.check_password] Password check successful for user: {self.username}")
        return result

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<User {self.username}>'
