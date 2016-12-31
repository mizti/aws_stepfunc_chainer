#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import os

REGION = 'ap-northeast-1'
#REQUEST_ID = 'sir-xser8nwg'

def check_bidding_result(spot_instance_request_id):
    ec2_client = boto3.client('ec2',
        region_name = REGION
    )
    response = ec2_client.describe_spot_instance_requests(
      SpotInstanceRequestIds = [spot_instance_request_id]
    )
    return response

def lambda_handler(event, context):
    response = check_bidding_result(event["spot_instance_request_id"])
    event["request_result"] = (response['SpotInstanceRequests'][0]['Status']['Code']==u'fulfilled')
    
    if event["request_result"]:
        event["instance_id"] = response['SpotInstanceRequests'][0]['InstanceId']
    
    return event

if __name__ == "__main__":
    lambda_handler("","")
