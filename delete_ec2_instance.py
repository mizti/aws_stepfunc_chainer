#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import logging
import os

#INSTANCE_ID = 'i-03e3025afff08936b'
REGION = 'ap-northeast-1'

def delete_ec2_instance(instance_id):
    ec2 = boto3.resource('ec2',
        region_name = REGION
    )
    instance = ec2.Instance(instance_id)
    response = instance.terminate()
    return response


def lambda_handler(event, context):
    instance_id = event["instance_id"]
    response = delete_ec2_instance(instance_id)
    return event

if __name__ == "__main__":
    lambda_handler("","")
