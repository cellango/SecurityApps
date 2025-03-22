from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add parent directory to path so we can import our models
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User, Base

# Get database URL from environment or use default
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@postgres:5432/security_score_card')

def create_admin_user():
    """Create admin user if it doesn't exist"""
    try:
        # Create database engine
        logger.info(f"Connecting to database: {DATABASE_URL}")
        engine = create_engine(DATABASE_URL)
        
        # Create tables
        Base.metadata.create_all(engine)
        logger.info("Database tables created successfully")
        
        # Create session
        Session = sessionmaker(bind=engine)
        session = Session()
        
        try:
            # Check if admin already exists
            existing_admin = session.query(User).filter_by(username='admin').first()
            if existing_admin:
                logger.info("Admin user exists, checking if password needs to be reset")
                # Reset admin password if needed
                existing_admin.set_password('admin')
                session.commit()
                logger.info("Admin password has been reset")
                return
            
            logger.info("Creating new admin user")
            # Create new admin user
            admin = User(
                username='admin',
                email='admin@example.com',
                is_active=True
            )
            admin.set_password('admin')
            
            # Add to database
            session.add(admin)
            session.commit()
            logger.info("Admin user created successfully")
            
        except Exception as e:
            logger.error(f"Error creating admin user: {str(e)}")
            session.rollback()
            raise
        finally:
            session.close()
            
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise

if __name__ == '__main__':
    try:
        create_admin_user()
    except Exception as e:
        logger.error(f"Failed to create admin user: {str(e)}")
        sys.exit(1)
