import unittest
from unittest.mock import patch
import json
import bcrypt
from moto import mock_aws
import boto3

from base_auth_test import BaseAuthTest

import sys
sys.path.append('..')
from Register.register_lambda import lambda_handler

@mock_aws
class TestLambdaFunction(BaseAuthTest):
    def test_registration_success(self):
        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'password123',
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['message'], 'Registered successfully, welcome!')

    def test_missing_input(self):
        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': '',
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['message'], 'Some part of the input is missing, please check and try again')

    def test_existing_user(self):
        # Pre-populate the table with an existing user
        salt = bcrypt.gensalt(rounds=15)
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), salt).decode('utf-8')
        self.table.put_item(Item={
            'uuid': 'existing-user-uuid',
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Existing',
            'last_name': 'User',
            'password': hashed_password
        })

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'password123',
                'username': 'testuser',
                'first_name': 'Test',
                'last_name': 'User'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['message'], 'User already exists, please login')
