# Unc Ingester Lambda Function

A Python-based AWS Lambda function with automated CI/CD deployment using GitHub Actions.

## 📋 Prerequisites

- Python 3.9 or higher
- AWS Account with appropriate permissions
- AWS CLI configured locally (for manual deployments)

## 🛠️ Local Development

### Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd Unc-Ingester
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the function locally:
```bash
python lambda_function.py
```

### Response Format

All responses follow this structure:
```json
{
  "statusCode": 200,
  "headers": {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*"
  },
  "body": "{\"message\": \"Success\"}"
}
```

### Local Testing

Test the function locally with different event types:
```python
from lambda_function import ingester_handler

# Test webhook
event = {
    'httpMethod': 'POST',
    'path': '/webhooks',
    'headers': {'X-GitHub-Event': 'push'},
    'requestContext': {'identity': {'sourceIp': '192.30.252.1'}},
    'body': '{"ref": "refs/heads/main", "repository": {"name": "my-repo"}}'
}

result = ingester_handler(event, None)
print(result)

# Test other endpoints
event = {
    'httpMethod': 'GET',
    'path': '/test',
    'queryStringParameters': {'param': 'value'}
}

result = ingester_handler(event, None)
print(result)
``` 