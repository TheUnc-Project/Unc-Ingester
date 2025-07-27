"""
Logger setup for the application.
This module should be imported first to ensure proper logging configuration.
"""

import logging
import json_logging
from config import DD_ENV, DD_SERVICE, DD_VERSION

# Configure JSON logging
json_logging.init_lambda()
json_logging.init_request_instrument()

# Configure root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Add custom fields to all log records
class DatadogContextFilter(logging.Filter):
    def filter(self, record):
        record.dd_service = DD_SERVICE
        record.dd_env = DD_ENV
        record.dd_version = DD_VERSION
        return True


logger.addFilter(DatadogContextFilter())
