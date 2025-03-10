import logging
import os
from logging.handlers import RotatingFileHandler

# Log file retention period (30 days)
LOG_RETENTION_DAYS = 30
LOG_DIR = os.path.join(os.getcwd(), "logs")

# Ensure logs directory exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

def setup_logger(module_name):
    """Setup a logger for a specific module."""
    log_file = os.path.join(LOG_DIR, f"{module_name}.log")

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=LOG_RETENTION_DAYS)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

def log_error(module_name, message, exception=None):
    """Logs an error message and optional exception details."""
    logger = setup_logger(module_name)
    if exception:
        logger.error(f"{message} | Exception: {str(exception)}")
    else:
        logger.error(message)

def log_warning(module_name, message):
    """Logs a warning message."""
    logger = setup_logger(module_name)
    logger.warning(message)

def log_info(module_name, message):
    """Logs an info message."""
    logger = setup_logger(module_name)
    logger.info(message)
