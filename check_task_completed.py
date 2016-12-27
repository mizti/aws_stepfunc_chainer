#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import os
import botocore

BUCKET_NAME = 'test-kick-the-bucket23'
FILENAME = 'completed.log'
REGION = 'ap-northeast-1'

def check_task_completed(access_key, secret_key):
    s3 = boto3.resource('s3',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = REGION
    )
    exists = False
    try:
        s3.Object(BUCKET_NAME, FILENAME).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            raise
    else:
        exists = True
    return exists


def lambda_handler(event, context):
    response = check_task_completed(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    print(response)
    return event, context

if __name__ == "__main__":
    lambda_handler("","")
