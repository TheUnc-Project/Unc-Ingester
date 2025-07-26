import json
import logging
from typing import Dict, Any
from handlers.post_webhooks import handler as webhook_handler

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        logger.info(f"Received event: {json.dumps(event)}")

        # Extract HTTP method and path if available
        http_method = event.get("httpMethod", "UNKNOWN")
        path = event.get("path", "/")

        body = event.get("body")
        if body:
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                logger.warning("Failed to parse request body as JSON")

        # Process the request based on HTTP method and path
        if http_method == "POST" and path == "/webhooks":
            response_data = webhook_handler(event, body)
        else:
            response_data = {
                "message": f"Method {http_method} not implemented",
                "path": path,
            }

        # Return successful response
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
        logger.error(f"Error processing request: {str(e)}")

        # Return error response
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps({"error": "Internal server error", "message": str(e)}),
        }
