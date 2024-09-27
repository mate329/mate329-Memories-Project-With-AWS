import json
import boto3
import os

dynamodb_client = boto3.resource('dynamodb')
posts_table = dynamodb_client.Table(os.getenv('POSTS_TABLE'))
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    print(f'Received event: {event}')
    
    # Get pagination parameters from the query string
    query_params = event.get('queryStringParameters', {})
    limit = int(query_params.get('limit', 10))
    exclusive_start_key = query_params.get('start_key', None)

    # Initialize the scan parameters
    scan_kwargs = {
        'Limit': limit
    }

    if exclusive_start_key:
        scan_kwargs['ExclusiveStartKey'] = { 'id': exclusive_start_key }

    response = posts_table.scan(**scan_kwargs)
    items = response.get('Items', [])
    last_evaluated_key = response.get('LastEvaluatedKey', None)

    # Generate signed URLs for each image
    for item in items:
        image_id = item['image_id']
        signed_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': os.getenv('IMAGES_BUCKET'), 'Key': image_id},
            ExpiresIn=3600
        )
        item['signed_url'] = signed_url

    return json.dumps({
        'statusCode': 200,
        'posts': items,
        'last_evaluated_key': last_evaluated_key
    })
