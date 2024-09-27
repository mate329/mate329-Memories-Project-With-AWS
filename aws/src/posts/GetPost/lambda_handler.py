import boto3
import json
import os

def lambda_handler(event, context):
    print(f'Received event: {event}')

    s3_client = boto3.client('s3')
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('POSTS_TABLE'))
    bucket_name = os.getenv('IMAGES_BUCKET')

    post_id = event.get('queryStringParameters', {}).get('postId', None)

    if not post_id:
        return json.dumps({'statusCode': 400, 'message': 'Missing post ID'})

    # Fetch post from DynamoDB
    response = table.get_item(Key={'id': post_id})
    if 'Item' in response:
        post = response['Item']
        # Generate a presigned URL if image key is available
        if 'image_id' in post:
            presigned_url = s3_client.generate_presigned_url('get_object',
                                                             Params={'Bucket': bucket_name, 'Key': post['image_id']},
                                                             ExpiresIn=1800)  # 30 minutes
            post['signed_url'] = presigned_url

        return json.dumps({'statusCode': 200, "post": post})
    else:
        return json.dumps({'statusCode': 404, 'message': 'Post not found'})
