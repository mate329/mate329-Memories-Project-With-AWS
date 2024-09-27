import json
import uuid
import boto3
import os
import base64
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    print(f'Received event: {event}')

    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('POSTS_TABLE'))
    bucket_name = os.getenv('IMAGES_BUCKET')

    try:
        event_body = json.loads(event.get('body')) if 'body' in event else event
        print(f'Received event: {event_body}')
    except json.JSONDecodeError as e:
        print(f'JSON decode error: {e}')
        return json.dumps({'statusCode': 400, 'message': 'Request body must be valid JSON.'})
    
    title = event_body.get('title')
    description = event_body.get('description')
    creator = event_body.get('creator')
    image_base64 = event_body.get('image')

    if not title or not description or not creator or not image_base64:
        print('Invalid input detected')
        return json.dumps({'statusCode': 400, 'message': 'Invalid input, please check and try again'})

    # Decode base64 image
    try:
        image_data = base64.b64decode(image_base64)
        image_id = f'{uuid.uuid4()}.jpg'
        s3_client.put_object(Bucket=bucket_name, Key=image_id, Body=image_data)
        print(f'Image uploaded successfully to S3: {image_id}')
    except Exception as e:
        print(f'Error uploading image to S3: {e}')
        return json.dumps({'statusCode': 500, 'message': 'Failed to upload image'})

    # Generate unique ID for the post and attempt to create the post
    post_id = str(uuid.uuid4())
    try:
        response = table.scan(
            FilterExpression=Attr('title').eq(title) & Attr('description').eq(description)
        )['Items']
        if not response:
            print('Creating new post')
            table.put_item(Item={
                'id': post_id,
                'title': title,
                'description': description,
                'creator': creator,
                'image_id': image_id
            })
            print(f'Post added successfully: {post_id}')
            return json.dumps({
                'statusCode': 200,
                'message': 'Post added successfully',
                'post_id': post_id,
                'image_id': image_id
            })
        else:
            print('Post already exists')
            return json.dumps({'statusCode': 400, 'message': 'Post already exists'})
    except Exception as e:
        print(f'Error handling the post creation: {e}')
        return json.dumps({'statusCode': 500, 'message': "Something's wrong, please try again"})
