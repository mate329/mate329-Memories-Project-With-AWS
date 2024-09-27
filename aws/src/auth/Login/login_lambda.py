import json
import bcrypt
import jwt
import time
import os
import boto3
from boto3.dynamodb.conditions import Attr

def get_user_by_email(email):
    dynamodb_client = boto3.resource('dynamodb')
    user_table = dynamodb_client.Table('users')
    response = user_table.scan(
        FilterExpression=Attr('email').eq(email)
    )
    return response['Items'][0] if response['Items'] else None

def verify_password(user_password, stored_password):
    return bcrypt.checkpw(user_password.encode('utf-8'), stored_password.encode('utf-8'))

def create_jwt_token(payload, secret_key):
    return jwt.encode(payload, key=secret_key, algorithm='HS256')

def lambda_handler(event, context):
    print(f'Login received event: {event}')
    event = json.loads(event.get('body')) if 'body' in event else event
    email = event.get('email')
    password = event.get('password')

    if not email or not password:
        return json.dumps({'statusCode': 400, 'message': 'Email or password missing, please check your input'})

    user = get_user_by_email(email)

    if not user or not verify_password(password, user['password']):
        return json.dumps({'statusCode': 400, 'message': 'User not found or password is incorrect, please try again'})

    jwt_payload = {
        'email': user['email'],
        'first_name': user['first_name'],
        'username': user['username'],
    }
    jwt_token = create_jwt_token(jwt_payload, os.getenv('SECRET_KEY'))

    return json.dumps({
        'statusCode': 200,
        'message': 'Logged in successfully, welcome!',
        'jwt': jwt_token
    })
