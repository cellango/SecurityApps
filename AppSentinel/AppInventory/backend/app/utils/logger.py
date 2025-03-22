import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import sys

def get_logger():
    logger = logging.getLogger('AppInventory')
    logger.setLevel(logging.DEBUG)
    logger.propagate = False  # Prevent propagation to parent loggers

    # Create console handler and set level to debug
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')

    # Add formatter to console handler
    console_handler.setFormatter(formatter)

    # Add console handler to logger
    logger.addHandler(console_handler)

    # Try to set up file logging if possible
    try:
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate log filename with date
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f'appinventory_{current_date}.log')

        # Create file handler
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        file_handler.setLevel(logging.DEBUG)  
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Could not set up file logging: {str(e)}")  
    
    return logger

logger = get_logger()