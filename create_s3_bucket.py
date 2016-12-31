import boto3
import botocore
import boto3.s3.transfer
import os

#BUCKET_NAME = 'test-kick-the-bucket2345'

def lookup(s3, bucket_name):
  try:
    s3.meta.client.head_bucket(Bucket=bucket_name)
  except botocore.exceptions.ClientError as e:
    error_code = int(e.response['Error']['Code'])

    if error_code == 404:
      return False

    return True

def create_bucket(bucket_name):
    s3 = boto3.resource('s3')
    response = ''
    if not lookup(s3, bucket_name):
       response = s3.create_bucket(Bucket=bucket_name)

    return response

def lambda_handler(event, context):
    response = create_bucket(event['exec_name'])
    return event

if __name__ == "__main__":
    lambda_handler("","")
