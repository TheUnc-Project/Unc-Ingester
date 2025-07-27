"""
Webhook handler for POST /webhooks requests.
"""

# Import logger_setup first to initialize logging configuration
# This import is used for its side effects

import config
from logger_setup import logger

from typing import Dict, Any

def handler(event: Dict[str, Any], body: Any) -> Dict[str, Any]:
    """
    Handle POST /webhooks requests.

    Args:
        event: The full Lambda event dict
        body: The parsed request body

    Returns:
        Dict containing the response data
    """
    logger.info(
        "Processing webhook request",
        extra={
            "event_type": "webhook_received",
            "body_size": len(str(body)),
            "event": event,
        },
    )

    return {
        "message": "Webhook received",
        "body": body,
    }
