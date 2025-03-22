import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime

class Logger:
    def __init__(self):
        self.logger = logging.getLogger('AppScore')
        self.setup_logger()

    def setup_logger(self):
        # Create logs directory if it doesn't exist
        log_dir = 'logs'
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Generate log filename with date
        current_date = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(log_dir, f'appscore_{current_date}.log')

        # Set logging level based on environment
        log_level = logging.DEBUG if os.getenv('FLASK_ENV') == 'development' else logging.INFO

        # Configure logger
        self.logger.setLevel(log_level)

        # Create handlers
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10485760,  # 10MB
            backupCount=10
        )
        console_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        log_format = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(module)s:%(lineno)d] %(message)s'
        )
        file_handler.setFormatter(log_format)
        console_handler.setFormatter(log_format)

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def debug(self, message, **kwargs):
        """Debug level log with optional context"""
        self._log(logging.DEBUG, message, **kwargs)

    def info(self, message, **kwargs):
        """Info level log with optional context"""
        self._log(logging.INFO, message, **kwargs)

    def warning(self, message, **kwargs):
        """Warning level log with optional context"""
        self._log(logging.WARNING, message, **kwargs)

    def error(self, message, **kwargs):
        """Error level log with optional context"""
        self._log(logging.ERROR, message, **kwargs)

    def critical(self, message, **kwargs):
        """Critical level log with optional context"""
        self._log(logging.CRITICAL, message, **kwargs)

    def _log(self, level, message, **kwargs):
        """Internal method to handle logging with context"""
        if kwargs:
            context = ' '.join([f'{k}={v}' for k, v in kwargs.items()])
            message = f'{message} - Context: {context}'
        self.logger.log(level, message)

# Create a global logger instance
logger = Logger().logger
