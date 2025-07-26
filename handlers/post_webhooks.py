"""
Webhook handler for POST /webhooks requests.
"""

import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def handler(event: Dict[str, Any], body: Any) -> Dict[str, Any]:
    """
    Handle POST /webhooks requests.

    Args:
        event: The full Lambda event dict
        body: The parsed request body

    Returns:
        Dict containing the response data
    """
    logger.info("Processing webhook request")

    return {
        "message": "Webhook received",
        "body": body,
    }
