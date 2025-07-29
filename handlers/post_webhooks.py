"""
Webhook handler for POST /webhooks requests.
"""

from typing import Dict, Any
from logger_setup import get_logger

# Get logger
logger = get_logger("webhook_handler")


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
        event_type="webhook_received",
        body=body,
        event=event,
    )

    return {
        "message": "Webhook received",
        "body": body,
    }
