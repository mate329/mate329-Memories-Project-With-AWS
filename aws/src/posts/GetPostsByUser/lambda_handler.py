import boto3
import json
import os
from boto3.dynamodb.conditions import Attr

def lambda_handler(event, context):
    print(f'Received event: {event}')

    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('POSTS_TABLE'))
    bucket_name = os.getenv('IMAGES_BUCKET')

    creator_name = event.get('queryStringParameters', {}).get('creatorName')

    # Fetch posts from DynamoDB
    response = table.scan(
        FilterExpression=Attr('creator').eq(creator_name)
    )
    posts = response['Items']

    # Generate presigned URLs for each post image
    for post in posts:
        if 'image_id' in post:
            presigned_url = s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': bucket_name, 'Key': post['image_id']},
                                                             ExpiresIn=1800)  # 30 minutes
            post['signed_url'] = presigned_url

    return json.dumps({
        'statusCode': 200,
        'posts': posts
    })
