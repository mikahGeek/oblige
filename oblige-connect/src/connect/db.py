import os
import sys
import json
import boto3
from boto3.dynamodb.conditions import Key
import uuid

client = boto3.client(
  'dynamodb', aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'), region_name = os.getenv('AWS_REGION')
)

dynamodb = boto3.resource(
  'dynamodb', aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'), aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'), region_name = os.getenv('AWS_REGION')
)

def log_connect_request(platform, source, dest):
  id = str(uuid.uuid4());
  # TODO: remember to follow CQRS. this should write to oblige-connect-requests, and let
  # another service ensure eventual consistency by updating oblige-connections
  dynamodb.Table('oblige-connections').put_item(Item = {'platform': platform, 'uuid': id, 'endpoint1': source, 'endpoint2': dest});
  return id;

def get_connected(platform, source, dest):
  return dynamodb.Table('oblige-connections').query(
    KeyConditionExpression=(
        Key('platform').eq(platform)
    ),
    FilterExpression=(
      Key('endpoint1').eq(source) & Key('endpoint2').eq(dest)
    )
  )

