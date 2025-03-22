from app.celery_app import celery_app
from app.models.application import Application
from app.utils.logger import logger
from app import db
from datetime import datetime
import requests
from celery.exceptions import MaxRetriesExceededError
from sqlalchemy.exc import SQLAlchemyError

@celery_app.task(bind=True, max_retries=3, name='tasks.check_application_health')
def check_application_health(self, application_id):
    """Check the health of an application"""
    try:
        application = Application.query.get(application_id)
        if not application:
            logger.error(f"Application {application_id} not found")
            return False

        # Add health check logic here
        health_status = _perform_health_check(application)
        
        # Update application status
        application.last_health_check = datetime.utcnow()
        application.health_status = health_status
        db.session.commit()

        return health_status

    except SQLAlchemyError as e:
        logger.error(f"Database error checking application health: {str(e)}")
        raise self.retry(exc=e, countdown=60)  # Retry in 60 seconds
    except Exception as e:
        logger.error(f"Error checking application health: {str(e)}")
        return False

@celery_app.task(bind=True, max_retries=3, name='tasks.update_application_metadata')
def update_application_metadata(self, application_id):
    """Update application metadata"""
    try:
        application = Application.query.get(application_id)
        if not application:
            logger.error(f"Application {application_id} not found")
            return False

        # Add metadata update logic here
        metadata = _fetch_application_metadata(application)
        
        # Update application metadata
        application.metadata = metadata
        application.last_metadata_update = datetime.utcnow()
        db.session.commit()

        return True

    except SQLAlchemyError as e:
        logger.error(f"Database error updating application metadata: {str(e)}")
        raise self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error(f"Error updating application metadata: {str(e)}")
        return False

@celery_app.task(name='tasks.schedule_health_checks')
def schedule_health_checks():
    """Schedule health checks for all active applications"""
    try:
        applications = Application.query.filter_by(active=True).all()
        for app in applications:
            check_application_health.delay(app.id)
        return True
    except Exception as e:
        logger.error(f"Error scheduling health checks: {str(e)}")
        return False

def _perform_health_check(application):
    """Perform health check for an application"""
    try:
        if not application.health_check_url:
            return "UNKNOWN"

        response = requests.get(
            application.health_check_url,
            timeout=10,
            verify=False  # For development only
        )
        
        if response.status_code == 200:
            return "HEALTHY"
        else:
            return "UNHEALTHY"

    except requests.RequestException:
        return "UNHEALTHY"

def _fetch_application_metadata(application):
    """Fetch metadata for an application"""
    # Implement metadata fetching logic here
    # This could include:
    # - Version information
    # - Dependencies
    # - Configuration
    # - Usage statistics
    return {
        "last_checked": datetime.utcnow().isoformat(),
        "version": application.version or "unknown",
        "status": application.health_status or "unknown"
    }
