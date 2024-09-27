import unittest
from unittest.mock import patch
import json
import boto3
import os
from moto import mock_aws

from base_post_test import BasePostTest

import sys
sys.path.append('..')
from DeletePost.lambda_handler import lambda_handler as delete_post_lambda_handler
from CreatePost.lambda_handler import lambda_handler as create_post_lambda_handler

@mock_aws
class TestDeletePost(BasePostTest):
    def test_missing_post_id(self):
        """ Test the function with missing post ID """
        event = {}
        response = json.loads(delete_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Missing post ID', response['message'])

    def test_post_not_found(self):
        """ Test the function with non-existent post ID """
        event = {'post_id': 'nonexistent'}
        response = json.loads(delete_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 404)

    def test_successful_deletion(self):
        """ Test successful deletion of a post and associated image """
        # Insert a sample item into DynamoDB
        create_post_event = {
            "title": "title",
            "creator": "steve",
            "description": "is awesome",
            "image": "YXNkYXNkYXNk",
        }
        create_post_response = json.loads(create_post_lambda_handler(create_post_event, None))

        event = {"body": json.dumps({'post_id': create_post_response['post_id']})}
        response = json.loads(delete_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('deleted successfully', response['message'])

    # def test_dynamodb_delete_error(self):
    #     """ Test DynamoDB deletion error """
    #     event = {"body": json.dumps({'post_id': '123'})}
    #     response = json.loads(delete_post_lambda_handler(event, None))
    #     self.assertEqual(response['statusCode'], 500)

    # def test_s3_delete_error(self):
    #     """ Test S3 deletion error when post exists """
    #     # Insert a sample item with an image id into DynamoDB
    #     dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
    #     table = dynamodb_resource.Table(self.table_name)
    #     table.put_item(Item={'id': '123', 'image_id': 'image123.jpg'})

    #     event = {"body": json.dumps({'post_id': '123'})}
    #     with patch('boto3.client') as mock_s3:
    #         mock_s3.return_value.delete_object.side_effect = Exception("S3 Deletion error")
    #         response = json.loads(delete_post_lambda_handler(event, None))
    #         self.assertEqual(response['statusCode'], 500)

