from datetime import datetime
import json
import boto3
import os

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('POSTS_TABLE'))

    print(f"Received event: {json.dumps(event)}")
    event = json.loads(event.get('body')) if 'body' in event else event
    if 'post_id' not in event or not event['post_id']:
        return json.dumps({
            'statusCode': 400,
            'message': 'Missing post ID'
        })

    post_id = event['post_id']
    updates = []
    expression_attribute_values = {}

    if 'title' in event and event['title']:
        updates.append('title = :title')
        expression_attribute_values[':title'] = event['title']

    if 'description' in event and event['description']:
        updates.append('description = :description')
        expression_attribute_values[':description'] = event['description']

    if not updates:
        return json.dumps({
            'statusCode': 400,
            'message': 'No updates provided'
        })

    update_expression = 'SET ' + ', '.join(updates)

    try:
        response = table.update_item(
            Key={'id': post_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )
        return json.dumps({
            'statusCode': 200,
            'message': response['Attributes']
        })
    except Exception as e:
        return json.dumps({
            'statusCode': 500,
            'message': f"An error occurred: {str(e)}"
        })
