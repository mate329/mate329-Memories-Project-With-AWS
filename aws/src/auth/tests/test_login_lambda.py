import unittest
from unittest.mock import patch
import json
import bcrypt
import jwt
from moto import mock_aws
import boto3
import os

from base_auth_test import BaseAuthTest

import sys
sys.path.append('..')
from Login.login_lambda import lambda_handler

@mock_aws
class TestLoginLambdaFunction(BaseAuthTest):
    def test_login_success(self):
        # Add a test user to the mock table
        salt = bcrypt.gensalt(rounds=15)
        hashed_password = bcrypt.hashpw('password123'.encode('utf-8'), salt).decode('utf-8')
        self.table.put_item(Item={
            'uuid': 'existing-user-uuid',
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'password': hashed_password
        })

        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'password123'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['message'], 'Logged in successfully, welcome!')
        self.assertIn('jwt', response)

        # Verify JWT
        decoded_jwt = jwt.decode(response['jwt'], os.environ['SECRET_KEY'], algorithms=["HS256"])
        self.assertEqual(decoded_jwt['email'], 'test@example.com')
        self.assertEqual(decoded_jwt['first_name'], 'Test')
        self.assertEqual(decoded_jwt['username'], 'testuser')

    def test_missing_input(self):
        event = {
            'body': json.dumps({
                'email': '',
                'password': 'password123'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['message'], 'Email or password missing, please check your input')

    def test_incorrect_password(self):
        event = {
            'body': json.dumps({
                'email': 'test@example.com',
                'password': 'wrong_password'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['message'], 'User not found or password is incorrect, please try again')

    def test_user_not_found(self):
        event = {
            'body': json.dumps({
                'email': 'nonexistent@example.com',
                'password': 'password123'
            })
        }
        context = {}
        response = json.loads(lambda_handler(event, context))
        self.assertEqual(response['statusCode'], 400)
        self.assertEqual(response['message'], 'User not found or password is incorrect, please try again')

