import json
import bcrypt
import jwt
import uuid
import boto3
from boto3.dynamodb.conditions import Attr

def check_required_fields(event, required_fields):
    return all(event.get(field) for field in required_fields)

def lambda_handler(event, context):
    print(f'Registration received event: {event}')
    event = json.loads(event.get('body')) if 'body' in event else event
    
    required_fields = ['email', 'password', 'first_name', 'last_name']
    if not check_required_fields(event, required_fields):
        return json.dumps({
            'statusCode': 400,
            'message': 'Some part of the input is missing, please check and try again'
        })
    
    email = event['email']
    password = event['password']
    first_name = event['first_name']
    last_name = event['last_name']
    username = event['username']
    user_profile_picture = event.get('user_profile_picture', None)
    
    dynamodb_client = boto3.resource('dynamodb')
    user_table = dynamodb_client.Table('users')
    
    # Check if user already exists
    existing_users = user_table.scan(
        FilterExpression=Attr('email').eq(email)
    )['Items']
    
    if existing_users:
        return json.dumps({
            'statusCode': 400,
            'message': 'User already exists, please login'
        })
    
    # Attempt to register the user
    try:
        salt = bcrypt.gensalt(rounds=5)
        new_user = {
            'uuid': str(uuid.uuid4()),
            'username': username,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'password': bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        }
            
        new_user['user_profile_picture'] = user_profile_picture if user_profile_picture else None
        user_table.put_item(Item=new_user)
    except Exception as e:
        print(f'Error: {e}')
        return json.dumps({
            'statusCode': 400,
            'message': 'Registration unsuccessful, please try again'
        })
    
    return json.dumps({
        'statusCode': 200,
        'message': 'Registered successfully, welcome!'
    })
