"""
AWS Lambda ingester function.
"""

# Import logger_setup first to initialize logging configuration
# This import is used for its side effects
import config
from logger_setup import logger

import json
import logging
from typing import Dict, Any
from handlers.post_webhooks import handler as webhook_handler

def ingester_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.

    Args:
        event: The event dict that contains the request data
        context: The context object that contains information about the runtime

    Returns:
        Dict containing the response with statusCode, headers, and body
    """
    try:
        http_method = event.get("httpMethod", "UNKNOWN")
        path = event.get("path", "/")

        logger.info(
            "Processing request",
            extra={"http_method": http_method, "path": path, "event": event},
        )

        body = event.get("body")
        if body:
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                logger.warning(
                    "Failed to parse request body as JSON", extra={"body": body}
                )

        # Process the request based on HTTP method and path
        if http_method == "POST" and path == "/webhooks":
            response_data = webhook_handler(event, body)
        else:
            response_data = {
                "message": f"Method {http_method} not implemented",
                "path": path,
            }

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS",
            },
            "body": json.dumps(response_data),
        }

    except Exception as e:
        logger.error(
            "Error processing request",
            extra={
                "error": str(e),
                "http_method": event.get("httpMethod", "UNKNOWN"),
                "path": event.get("path", "/"),
            },
        )

        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Internal server error", "message": str(e)}),
        }
