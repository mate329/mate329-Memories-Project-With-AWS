import json
import boto3
import os

def lambda_handler(event, context):
    """
    Lambda function to delete a post and its associated image.
    It retrieves the post details from a DynamoDB table and then deletes the image from an S3 bucket.
    
    Parameters:
    event (dict): The event dictionary containing details like the body of the request.
    context (LambdaContext): Provides runtime information about the Lambda function execution.
    
    Returns:
    dict: A dictionary with the status code and a message indicating the result of the operation.
    """
    print(f'Received event: {event}')

    # Initialize AWS clients for DynamoDB and S3
    dynamodb = boto3.resource('dynamodb')
    s3_client = boto3.client('s3')

    # Retrieve table and bucket names from environment variables
    table = dynamodb.Table(os.getenv('POSTS_TABLE'))
    bucket_name = os.getenv('IMAGES_BUCKET')

    # Attempt to parse the event body to get post data
    try:
        event_body = json.loads(event.get('body')) if 'body' in event else event
        print(f'Received event: {event_body}')
    except json.JSONDecodeError:
        return json.dumps({'statusCode': 400, 'message': 'Request body must be valid JSON.'})

    # Retrieve the post ID from the request body
    post_id = event_body.get('post_id')
    if not post_id:
        return json.dumps({'statusCode': 400, 'message': 'Missing post ID'})

    # Fetch the post from DynamoDB to get associated image_id before deletion
    try:
        response = table.get_item(Key={'id': post_id})
        post = response.get('Item')
        if not post:
            return json.dumps({'statusCode': 404, 'message': 'Post not found'})
    except Exception as e:
        print(f'Error fetching post: {str(e)}')
        return json.dumps({'statusCode': 500, 'message': "Failed to fetch post"})

    # Delete the post from the DynamoDB table
    try:
        table.delete_item(Key={'id': post_id})
        print(f'Post deleted successfully from DynamoDB: {post_id}')
    except Exception as e:
        print(f'Error deleting post from DynamoDB: {str(e)}')
        return {'statusCode': 500, 'message': "Failed to delete post from DynamoDB"}

    # If the post contained an image, delete it from S3
    image_id = post.get('image_id')
    if image_id:
        try:
            s3_client.delete_object(Bucket=bucket_name, Key=image_id)
            print(f'Image deleted successfully from S3: {image_id}')
        except Exception as e:
            print(f'Error deleting image from S3: {str(e)}')
            return json.dumps({'statusCode': 500, 'message': "Failed to delete image from S3"})

    # Return success response if everything was successful
    return json.dumps({'statusCode': 200, 'message': 'Post and associated image deleted successfully'})
