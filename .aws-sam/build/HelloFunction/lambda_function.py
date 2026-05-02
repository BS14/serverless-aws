import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    logger.info("Lambda invoked")
    logger.info(f"Event received: {json.dumps(event)}")

    try:
        response = {
            "message": "Hello, World!"
        }

        logger.info("Successfully processed request")

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(response)
        }

    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)

        return {
            "statusCode": 500,
            "body": json.dumps({
                "error": "Internal Server Error"
            })
        }
