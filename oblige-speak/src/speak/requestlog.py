import os
import sys
import json
import boto3
import uuid

client = boto3.client(
  'dynamodb', aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'), region_name = os.getenv('AWS_REGION')
)

dynamodb = boto3.resource(
  'dynamodb', aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'), region_name = os.getenv('AWS_REGION')
)

def log_request(request):
  id = str(uuid.uuid4());
  dynamodb.Table('oblige_speak_request').put_item(Item = {'topic': 'main', 'uuid': id, 'text': request});
  return id;

def log_response(response, requestid):
  dynamodb.Table('oblige_speak_request').update_item(Key = {'topic': 'main', 'uuid': requestid}, UpdateExpression = "set response_text = :r", ExpressionAttributeValues={':r': response})
