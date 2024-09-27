import boto3
from moto import mock_aws

import unittest
from unittest.mock import patch
import json
import bcrypt
import os
import base64

from base_post_test import BasePostTest

import sys
sys.path.append('..')
from CreatePost.lambda_handler import lambda_handler

@mock_aws
class TestCreatePost(BasePostTest):
    def test_create_post_success(self):
        # Patch environment variables
        event = {
            "title": "title",
            "creator": "steve",
            "description": "is awesome",
            "image": "YXNkYXNkYXNk",
        }
        
        # Call the lambda handler
        response = json.loads(lambda_handler(event, None))
        print(f'Received response from the Create Post Lamdba: {response}')
        
        # Get the image id from the response
        image_id = response['image_id']
        
        # Check the S3 bucket for the uploaded image
        body = self.s3_client.Object(self.bucket_name, image_id).get()["Body"].read().decode('utf-8')
        
        print('Body and event[image]: ', body, event["image"])
        
        # Verify that the image data matches the input
        assert body == base64.b64decode(event['image']).decode('utf-8')

    def test_missing_required_fields(self):
        event = {'body': json.dumps({"title": "Only Title"})}  # Missing 'creator', 'description', 'image'
        
        response = json.loads(lambda_handler(event, None))
        self.assertIn('Invalid input, please check and try again', response['message'])

    def test_image_upload_failure(self):
        event = {"title": "New Post", "creator": "Alice", "description": "A great post", "image": "invalidbase64"}
        response = json.loads(lambda_handler(event, None))
        self.assertIn('Failed to upload image', response['message'])

    def test_post_already_exists(self):
        # Simulate existing post
        self.dynamodb_table.put_item(Item={"id": "unique_id", "title": "New Post", "description": "A great post", "creator": "Alice"})
        event = {"title": "New Post", "description": "A great post", "creator": "Alice", "image": "YXNkYXNkYXNk"}

        response = json.loads(lambda_handler(event, None))
        self.assertIn('Post already exists', response['message'])
