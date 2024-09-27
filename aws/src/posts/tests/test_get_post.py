import unittest
from unittest.mock import patch
import boto3
from moto import mock_aws
import os
import json

from base_post_test import BasePostTest

import sys
sys.path.append('..')
from GetPost.lambda_handler import lambda_handler as get_post_lambda_handler
from CreatePost.lambda_handler import lambda_handler as create_post_lambda_handler

@mock_aws
class TestGetPost(BasePostTest):
    def test_missing_post_id(self):
        event = {"queryStringParameters": {}}
        response = json.loads(get_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 400)
        self.assertIn('Missing post ID', response['message'])

    def test_post_not_found(self):
        event = {"queryStringParameters": {"postId": "123"}}
        response = json.loads(get_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 404)

    def test_post_found_with_image(self):
        create_post_event = {
            "title": "title",
            "creator": "steve",
            "description": "is awesome",
            "image": "YXNkYXNkYXNk",
        }
        create_post_lambda_response = json.loads(create_post_lambda_handler(create_post_event, None))

        event = {"queryStringParameters": {"postId": create_post_lambda_response['post_id']}}
        response = json.loads(get_post_lambda_handler(event, None))
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('signed_url', response['post'])
