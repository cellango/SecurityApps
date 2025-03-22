from celery import Celery
from flask import Flask

def create_celery_app(app: Flask = None):
    """Create and configure Celery instance"""
    
    celery = Celery(
        'AppInventory',
        broker='redis://redis:6379/0',
        backend='redis://redis:6379/0',
        include=['app.tasks']
    )

    # Configure Celery
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=30 * 60,  # 30 minutes
        worker_prefetch_multiplier=1,
        worker_concurrency=2
    )

    if app:
        # Update celery with Flask context
        class ContextTask(celery.Task):
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return self.run(*args, **kwargs)

        celery.Task = ContextTask

    return celery

# Create the celery app
celery_app = create_celery_app()
