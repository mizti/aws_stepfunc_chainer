#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import logging
import base64
import os
from pathlib import Path

INSTANCE_ID = 'i-03e3025afff08936b'
REGION = 'ap-northeast-1'
def delete_ec2_instance(access_key, secret_key):
    ec2 = boto3.resource('ec2',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = REGION
    )
    instance = ec2.Instance(INSTANCE_ID)
    response = instance.terminate()
    return response


def lambda_handler(event, context):
    response = delete_ec2_instance(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    print(response)
    return event, context

if __name__ == "__main__":
    lambda_handler("","")
