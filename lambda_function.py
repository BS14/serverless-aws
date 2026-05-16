import json
import logging
import os
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

ssm = boto3.client('ssm')
secrets_manager = boto3.client('secretsmanager')

# Cached outside the handler — fetched once per cold start
def _get_parameter(name):
    response = ssm.get_parameter(Name=name, WithDecryption=True)
    return response['Parameter']['Value']

def _get_secret(secret_arn):
    response = secrets_manager.get_secret_value(SecretId=secret_arn)
    return json.loads(response['SecretString'])

# Cold-start cache
_api_url = _get_parameter(os.environ['SSM_PARAMETER_NAME'])
_secret = _get_secret(os.environ['SECRET_ARN'])


def lambda_handler(event, context):
    logger.info("Lambda invoked")
    logger.info(f"Event received: {json.dumps(event)}")

    try:
        response = {
            "message": "Hello, World!",
            "api_url": _api_url,
            # Never log or return the actual secret — only show it's loaded
            "secret_loaded": "api_key" in _secret,
        }

        logger.info("Successfully processed request")

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(response),
        }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)

        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error"}),
        }
