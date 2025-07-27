"""
Bootstraps environment variables and secrets into os.environ.
This should be imported early in the Lambda lifecycle.
"""

import os
import boto3
from botocore.exceptions import ClientError

# Determine the AWS region (default to us-east-1)
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
secrets_client = boto3.client("secretsmanager", region_name=AWS_REGION)


def get_secret(secret_name: str) -> str:
    """Retrieve a secret string from AWS Secrets Manager."""
    try:
        response = secrets_client.get_secret_value(SecretId=secret_name)
        return response.get("SecretString", "")
    except ClientError as e:
        raise RuntimeError(
            f"Unable to retrieve secret '{secret_name}': {e.response['Error']['Message']}"
        )
    except Exception as e:
        raise RuntimeError(
            f"Unexpected error retrieving secret '{secret_name}': {str(e)}"
        )


# Map of environment variables to secrets in AWS Secrets Manager
secrets_map = {
    "DD_API_KEY": "DATADOG_API_KEY",
    "DD_API_KEY_ID": "DATADOG_API_KEY_ID",
}

# Load secrets into os.environ if not already set
for env_var, secret_name in secrets_map.items():
    if not os.environ.get(env_var):
        secret_value = get_secret(secret_name)
        if secret_value:  # Only set if the secret was retrieved
            os.environ[env_var] = secret_value


# Apply default values for common Datadog config
defaults = {
    "DD_SITE": "datadoghq.com",
    "DD_ENV": "dev",
    "DD_SERVICE": "unc-ingester",
    "DD_VERSION": "1.0.0",
}

for key, default in defaults.items():
    os.environ.setdefault(key, default)
