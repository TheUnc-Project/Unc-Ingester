"""
Sets up structured JSON logging for the application.
This module should be imported first to ensure logging is configured properly.
"""
import config
import logging
import os

# Fallback defaults for environments that may not preload these variables
DD_SERVICE = os.environ.get("DD_SERVICE", "unc-ingester")
DD_ENV = os.environ.get("DD_ENV", "dev")
DD_VERSION = os.environ.get("DD_VERSION", "1.0.0")

print("ENV", DD_SERVICE, DD_ENV, DD_VERSION)

# Get root logger and set level
logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DatadogContextFilter(logging.Filter):
    """Injects Datadog-specific fields into each log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.dd_service = DD_SERVICE
        record.dd_env = DD_ENV
        record.dd_version = DD_VERSION
        return True


logger.addFilter(DatadogContextFilter())

__all__ = ["logger"]
