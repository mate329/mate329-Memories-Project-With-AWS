import unittest
from unittest.mock import patch
import json
import bcrypt
import jwt
from moto import mock_aws
import boto3
import os

@mock_aws
class BaseAuthTest(unittest.TestCase):
    def setUp(self):
        # os.environ['SECRET_KEY'] = 'secret'
        # Set up the DynamoDB mock table
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.create_table(
            TableName='users',
            KeySchema=[
                {'AttributeName': 'uuid', 'KeyType': 'HASH'}
            ],
            AttributeDefinitions=[
                {'AttributeName': 'uuid', 'AttributeType': 'S'}
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        self.table.wait_until_exists()
        
        self.env_vars = {
            'SECRET_KEY': "secret"
        }
        patch.dict(os.environ, self.env_vars).start()