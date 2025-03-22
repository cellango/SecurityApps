# Task Queue System Documentation

## Overview

AppSentinel uses Celery with Redis as the message broker for managing asynchronous tasks and scheduled jobs. This system handles application lifecycle management, health checks, and metadata updates.

## Architecture

The task queue system consists of several components:

1. **Celery**: The distributed task queue
2. **Redis**: Message broker and result backend
3. **Celery Beat**: Scheduler for periodic tasks
4. **Flower**: Web-based task monitoring tool

## Components

### Message Broker (Redis)
- Running on port 6379
- Handles task queue management
- Stores task results

### Celery Workers
- Process asynchronous tasks
- Handle retries and error cases
- Maintain Flask application context

### Celery Beat
- Schedules periodic tasks
- Manages task intervals
- Handles task distribution

### Flower Dashboard
- Available at http://localhost:5555
- Monitors task execution
- Provides task statistics
- Shows worker status

## Task Types

### Application Health Checks
```python
from app.tasks.application_lifecycle import check_application_health

# Schedule a health check for an application
result = check_application_health.delay(application_id)

# Get task status
status = result.status  # 'SUCCESS', 'FAILURE', 'PENDING'
```

### Application Metadata Updates
```python
from app.tasks.application_lifecycle import update_application_metadata

# Update application metadata
result = update_application_metadata.delay(application_id)

# Get task result
if result.successful():
    metadata = result.get()
```

## Periodic Tasks

Current periodic tasks:

| Task | Schedule | Description |
|------|----------|-------------|
| Health Checks | Every 5 minutes | Checks health status of all active applications |

## Configuration

### Environment Variables
```bash
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### Task Settings
```python
# Default settings in celery_app.py
CELERY_CONFIG = {
    'task_serializer': 'json',
    'accept_content': ['json'],
    'result_serializer': 'json',
    'timezone': 'UTC',
    'enable_utc': True,
    'task_track_started': True,
    'task_time_limit': 30 * 60,  # 30 minutes
    'worker_prefetch_multiplier': 1,
    'worker_concurrency': 2
}
```

## Development Guidelines

### Creating New Tasks

1. Add task to `app/tasks/application_lifecycle.py`:
```python
@celery_app.task(bind=True, max_retries=3)
def my_new_task(self, *args, **kwargs):
    try:
        # Task logic here
        return result
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
```

2. Register periodic tasks in `app/__init__.py`:
```python
celery.conf.beat_schedule = {
    'my-periodic-task': {
        'task': 'tasks.my_new_task',
        'schedule': 300.0,  # 5 minutes
    },
}
```

### Error Handling

Tasks should:
1. Use proper exception handling
2. Implement retry logic for transient failures
3. Log errors appropriately
4. Return meaningful status information

Example:
```python
@celery_app.task(bind=True, max_retries=3)
def example_task(self, task_data):
    try:
        result = process_data(task_data)
        return {'status': 'success', 'result': result}
    except TransientError as e:
        raise self.retry(exc=e, countdown=60)
    except Exception as e:
        logger.error(f"Fatal error in example_task: {str(e)}")
        return {'status': 'error', 'message': str(e)}
```

### Monitoring

1. Access Flower dashboard:
   - URL: http://localhost:5555
   - Features:
     - Real-time task monitoring
     - Worker status
     - Task history
     - Error tracking

2. Check task status programmatically:
```python
from celery.result import AsyncResult

def get_task_status(task_id):
    result = AsyncResult(task_id)
    return {
        'status': result.status,
        'result': result.result if result.successful() else None,
        'error': str(result.result) if result.failed() else None
    }
```

## Docker Integration

Services are defined in `docker-compose.yml`:

1. **Celery Worker**:
   - Processes tasks
   - Maintains application context
   - Handles database connections

2. **Celery Beat**:
   - Schedules periodic tasks
   - Manages task timing

3. **Flower**:
   - Provides monitoring interface
   - Shows task statistics

4. **Redis**:
   - Message broker
   - Result backend

### Starting the Services

```bash
# Start all services
docker compose up -d

# Start specific service
docker compose up -d celery_worker

# View logs
docker compose logs -f celery_worker
```

## Best Practices

1. **Task Design**
   - Keep tasks small and focused
   - Use meaningful task names
   - Include proper logging
   - Handle errors gracefully

2. **Performance**
   - Monitor task queue length
   - Set appropriate timeouts
   - Use task priorities when needed
   - Implement proper retry policies

3. **Monitoring**
   - Regular check of Flower dashboard
   - Monitor Redis memory usage
   - Track failed tasks
   - Set up alerts for critical failures

4. **Security**
   - Secure Redis instance
   - Monitor task access
   - Validate task parameters
   - Handle sensitive data appropriately

## Troubleshooting

Common issues and solutions:

1. **Tasks not executing**
   - Check Redis connection
   - Verify worker status
   - Check task registration

2. **Worker not starting**
   - Verify Redis connection
   - Check environment variables
   - Review worker logs

3. **Tasks failing**
   - Check task logs
   - Verify database connection
   - Review error messages

4. **Performance issues**
   - Monitor queue length
   - Check worker concurrency
   - Review task execution time
