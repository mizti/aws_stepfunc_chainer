#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import logging
import base64
import os
from pathlib import Path

SPOT_PRICE = '0.2'
REGION = 'ap-northeast-1'
AMI_ID = 'ami-5860093f'
KEY_NAME = 'miz_private_key'
INSTANCE_TYPE = 'c4.large'
SECURITY_GRUOP_ID = ['sg-6bd2780c']

REPOSITORY_URL  = 'https://github.com/mattya/chainer-pix2pix.git'
REPOSITORY_NAME = 'chainer-pix2pix'
BUCKET_NAME = 'test-kick-the-bucket23'

f = open('user_data_shell.sh')
shell_code = f.read().format(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'), BUCKET_NAME ,REPOSITORY_URL, REPOSITORY_NAME)
f.close()

user_data = base64.encodestring(shell_code.encode('utf-8')).decode('ascii')

def request_spot_instance(access_key, secret_key):
    ec2_client = boto3.client('ec2',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = REGION
    )
    response = ec2_client.request_spot_instances(
        SpotPrice = SPOT_PRICE,
        Type = 'one-time',
        LaunchSpecification = {
            'ImageId': AMI_ID,
            'KeyName': KEY_NAME,
            'InstanceType': INSTANCE_TYPE,
            'UserData': user_data,
            'Placement':{},
            'SecurityGroupIds': SECURITY_GRUOP_ID
        }
    )
    return response


def lambda_handler(event, context):
    response = request_spot_instance(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    print(response)
    return event, context

if __name__ == "__main__":
    lambda_handler("","")
