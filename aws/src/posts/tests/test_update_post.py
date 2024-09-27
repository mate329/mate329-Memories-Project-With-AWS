import unittest
from unittest.mock import patch
import boto3
from moto import mock_aws
import os
import json

from base_post_test import BasePostTest

import sys
sys.path.append('..')
from CreatePost.lambda_handler import lambda_handler as create_post_lambda_handler
from UpdatePost.lambda_handler import lambda_handler as update_post_lambda_handler

@mock_aws
class TestUpdatePost(BasePostTest):
    def test_missing_post_id(self):
        """Test the response when no post ID is provided."""
        event = {}
        response = json.loads(update_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Missing post ID', response['message'])

    def test_no_updates_provided(self):
        """Test the response when no update fields are provided."""
        create_post_event = {
            "title": "title",
            "creator": "steve",
            "description": "is awesome",
            "image": "YXNkYXNkYXNk",
        }
        create_post_response = json.loads(create_post_lambda_handler(create_post_event, None))

        event = {'post_id': create_post_response['post_id']}
        response = json.loads(update_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('No updates provided', response['message'])

    def test_successful_update(self):
        """Test successful update of a post."""
        # Insert a sample item into DynamoDB
        create_post_event = {
            "title": "title",
            "creator": "steve",
            "description": "is awesome",
            "image": "YXNkYXNkYXNk",
        }
        create_post_response = json.loads(create_post_lambda_handler(create_post_event, None))

        # Update the post
        event = {
            'post_id': create_post_response['post_id'],
            'title': 'Updated Title',
            'description': 'updated description',
        }
        response = json.loads(update_post_lambda_handler(event, None))

        # Use the DynamoDB client to get the item and verify the title was updated
        post_item = self.dynamodb_table.get_item(Key={'id': create_post_response['post_id']})['Item']
        self.assertEqual(post_item['title'], 'Updated Title')
        self.assertEqual(post_item['description'], 'updated description')

    # def test_dynamodb_update_error(self):
    #     """Test error handling if DynamoDB update fails."""
    #     event = {'body': json.dumps({'id': '123', 'title': 'Updated Title'})}
    #     with patch('boto3.resource') as mock_dynamodb:
    #         mock_dynamodb.return_value.Table.return_value.update_item.side_effect = Exception("Update error")
    #         response = lambda_handler(event, None)
    #         self.assertEqual(response['statusCode'], 500)
    #         self.assertIn('An error occurred', response['message'])
