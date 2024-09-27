import unittest
from unittest.mock import patch
import boto3
from moto import mock_aws
import os
import json

from base_post_test import BasePostTest

import sys
sys.path.append('..')
from GetPostsByUser.lambda_handler import lambda_handler as get_posts_by_user_lambda_handler
from CreatePost.lambda_handler import lambda_handler as create_post_lambda_handler

@mock_aws
class TestGetPostsByUser(BasePostTest):
    def test_missing_creator_name(self):
        """ Test Lambda function without creator name in event """
        event = {'queryStringParameters': {}}
        response = json.loads(get_posts_by_user_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['posts'], [])

    def test_successful_fetch_posts(self):
        """ Test successfully fetching posts and generating presigned URLs """
        # Insert a sample item into DynamoDB
        create_post_event = {
            "title": "title",
            "creator": "steve",
            "description": "is awesome",
            "image": "YXNkYXNkYXNk",
        }
        create_post_lambda_response = json.loads(create_post_lambda_handler(create_post_event, None))

        event = {'queryStringParameters': {'creatorName': 'steve'}}
        response = json.loads(get_posts_by_user_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('signed_url', response['posts'][0])

    # def test_fetch_posts_no_image(self):
    #     """ Test fetching posts without image_id field """
    #     dynamodb_resource = boto3.resource('dynamodb', region_name='us-east-1')
    #     table = dynamodb_resource.Table(self.table_name)
    #     table.put_item(Item={'id': '002', 'creator': 'Jane'})

    #     event = {'queryStringParameters': {'creatorName': 'Jane'}}
    #     response = lambda_handler(event, None)
    #     self.assertEqual(response['statusCode'], 200)
    #     self.assertNotIn('signedImageUrl', response['body']['data'][0])