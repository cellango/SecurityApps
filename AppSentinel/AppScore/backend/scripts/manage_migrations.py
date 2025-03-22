import os
import shutil
import logging
from flask_migrate import init, migrate, upgrade
from app import app

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def manage_migrations():
    """Handle database migrations."""
    try:
        migrations_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'migrations')
        versions_dir = os.path.join(migrations_dir, 'versions')

        # Check if we need to initialize migrations
        if not os.path.exists(migrations_dir) or not os.path.exists(versions_dir) or not any(f.endswith('.py') for f in os.listdir(versions_dir) if not f.startswith('__')):
            logger.info("No migration scripts found. Initializing fresh migrations...")
            
            # Remove existing migrations directory if it exists
            if os.path.exists(migrations_dir):
                logger.info("Removing existing migrations directory...")
                shutil.rmtree(migrations_dir)
            
            # Initialize new migrations
            logger.info("Initializing alembic...")
            with app.app_context():
                init()
                migrate(message='Initial schema')
        else:
            logger.info("Found existing migration scripts")
            logger.info("Migration files in versions directory:")
            for f in os.listdir(versions_dir):
                if f.endswith('.py') and not f.startswith('__'):
                    logger.info(f"  - {f}")

        # Run the upgrade
        logger.info("Running database upgrade...")
        with app.app_context():
            upgrade()
            
        logger.info("Migration process completed successfully")
        return True

    except Exception as e:
        logger.error(f"Error during migration process: {str(e)}")
        raise

if __name__ == '__main__':
    manage_migrations()
