#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import os

SPOT_PRICE = '0.2'
REGION = 'ap-northeast-1'
REQUEST_ID = 'sir-6a2r8fjj'

def check_bidding_result(access_key, secret_key):
    ec2_client = boto3.client('ec2',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = REGION
    )
    requested_instance = ec2_client.describe_spot_instance_requests(
      SpotInstanceRequestIds = [REQUEST_ID]
    )
    return (requested_instance['SpotInstanceRequests'][0]['Status']['Code']==u'fulfilled')


def lambda_handler(event, context):
    response = check_bidding_result(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'), REGION)
    print(response)
    return event, context

if __name__ == "__main__":
    lambda_handler("","")
