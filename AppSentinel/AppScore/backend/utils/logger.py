import logging
import sys
from functools import wraps
from config import get_config

config = get_config()

# Create logger
logger = logging.getLogger('security_score_card')
logger.setLevel(getattr(logging, config.LOG_LEVEL))

# Create console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(getattr(logging, config.LOG_LEVEL))

# Create formatter
formatter = logging.Formatter(config.LOG_FORMAT)
console_handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(console_handler)

def debug_log(func):
    """Decorator to log function entry and exit in debug mode."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if config.is_development:
            func_name = func.__name__
            logger.debug(f"Entering {func_name}")
            try:
                result = func(*args, **kwargs)
                logger.debug(f"Exiting {func_name}")
                return result
            except Exception as e:
                logger.error(f"Error in {func_name}: {str(e)}")
                raise
        return func(*args, **kwargs)
    return wrapper

def log_info(message):
    """Log info message."""
    logger.info(message)

def log_debug(message):
    """Log debug message only in development mode."""
    if config.is_development:
        logger.debug(message)

def log_error(message, exc_info=None):
    """Log error message."""
    logger.error(message, exc_info=exc_info)

def log_warning(message):
    """Log warning message."""
    logger.warning(message)

def log_critical(message):
    """Log critical message."""
    logger.critical(message)
