import boto3
import json
import os
from boto3.dynamodb.conditions import Or, Attr

def lambda_handler(event, context):
    print(f'Received event: {event}')

    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('POSTS_TABLE'))
    bucket_name = os.getenv('IMAGES_BUCKET')

    inquiry = event.get('queryStringParameters', {}).get('inquiry', None)

    if not inquiry:
        return json.dumps({'statusCode': 400, 'message': 'Missing search inquiry'})

    # Fetch post from DynamoDB
    response = table.scan(
        FilterExpression=Or(
            Attr('title').contains(inquiry),
            Attr('description').contains(inquiry)
        )
    )

    if 'Items' in response:
        posts = response['Items']
        # Generate a presigned URL for each post if image key is available
        for post in posts:
            if 'image_id' in post:
                presigned_url = s3_client.generate_presigned_url('get_object',
                                                                Params={'Bucket': bucket_name, 'Key': post['image_id']})
                                                                # ExpiresIn=1800)  # 30 minutes
                post['signed_url'] = presigned_url

        return json.dumps({'statusCode': 200, "posts": posts})
    else:
        return json.dumps({'statusCode': 404, 'message': 'Posts not found'})
