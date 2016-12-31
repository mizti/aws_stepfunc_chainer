#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import os
import botocore

#BUCKET_NAME = 'test-kick-the-bucket23'
FILENAME = 'completed.log'
REGION = 'ap-northeast-1'

def check_task_completed(bucket_name):
    s3 = boto3.resource('s3',
        region_name = REGION
    )
    exists = False
    try:
        s3.Object(bucket_name, FILENAME).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            exists = False
        else:
            raise
    else:
        exists = True
    return exists

def lambda_handler(event, context):
    bucket_name = event["exec_name"]
    event["task_completed"] = check_task_completed(bucket_name)
    return event

if __name__ == "__main__":
    lambda_handler("","")
