import boto3
from moto import mock_aws

import unittest
from unittest.mock import patch
import json
import bcrypt
import os
import base64

@mock_aws
class BasePostTest(unittest.TestCase):
    def setUp(self):
        self.bucket_name = 'test-post-bucket'
        self.post_table_name = 'test-post-table'

        self.s3_client = boto3.resource("s3", region_name="us-east-1")
        self.s3_bucket = self.s3_client.create_bucket(Bucket=self.bucket_name)

        self.dynamodb_client = boto3.resource("dynamodb", region_name="us-east-1")
        self.dynamodb_table = self.dynamodb_client.create_table(
            TableName=self.post_table_name,
            KeySchema=[
                {
                    'AttributeName': 'id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'id',
                    'AttributeType': 'S'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 1,
                'WriteCapacityUnits': 1
            }
        )
        self.dynamodb_table.meta.client.get_waiter('table_exists').wait(TableName=self.post_table_name)

        self.env_vars = {
            'POSTS_TABLE': self.post_table_name,
            'IMAGES_BUCKET': self.bucket_name
        }
        patch.dict(os.environ, self.env_vars).start()
