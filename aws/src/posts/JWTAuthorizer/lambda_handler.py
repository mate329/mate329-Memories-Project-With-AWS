import json
import jwt  # Make sure to include `pyjwt` in your deployment package or layer
from jwt.exceptions import InvalidTokenError
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Event: %s', json.dumps(event))
    token = event.get('headers', {}).get('authorization')

    secret = os.getenv('JWT_SECRET')

    try:
        # Decode the JWT token
        logger.info('Trying to decode token: %s', token)
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        logger.info('Allowed Payload: %s', payload)

        response = {
            "isAuthorized": True,
            "context": {
                "user": payload.get('email'),
            }
        }
        return response

    except InvalidTokenError as e:
        logger.error('Invalid token: %s', e)

        response = {
            "isAuthorized": False,
            "context": {
            }
        }
        return response

    except Exception as e:
        logger.error('Error: %s', e)
        raise e
