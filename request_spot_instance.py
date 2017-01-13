#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import logging
import base64
import os

SPOT_PRICE = '0.8'
REGION = 'ap-northeast-1'
AMI_ID = 'ami-5860093f'
KEY_NAME = 'miz_private_key'
INSTANCE_TYPE = 'g2.2xlarge'
SECURITY_GRUOP_ID = ['sg-6bd2780c']

def request_spot_instance(user_data):
    ec2_client = boto3.client('ec2',
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
    REPOSITORY_URL  = event["repository_url"]
    REPOSITORY_NAME = event["repository_name"]
    BUCKET_NAME = event["exec_name"]

    shell='''#!/bin/sh
    sudo -s ubuntu
    cd /home/ubuntu
    sudo -u ubuntu mkdir /home/ubuntu/.aws
    sudo -u ubuntu mkdir /home/ubuntu/completed
    sudo -u ubuntu git clone {5}
    sudo -u ubuntu mkdir {0}
    sudo -u ubuntu mkdir {1}
    
    sudo -u ubuntu echo "[default]" >> /home/ubuntu/.aws/credentials
    sudo -u ubuntu echo "aws_access_key_id={2}" >> /home/ubuntu/.aws/credentials
    sudo -u ubuntu echo "aws_secret_access_key={3}" >> /home/ubuntu/.aws/credentials

    sudo -u ubuntu echo "*/5 * * * * /home/ubuntu/.pyenv/shims/aws s3 sync {1} s3://{4} > /dev/null 2>&1" >> mycron
    sudo -u ubuntu echo "*/1 * * * * /home/ubuntu/.pyenv/shims/aws s3 cp {1}/log s3://{4} > /dev/null 2>&1" >> mycron
    sudo -u ubuntu echo "*/1 * * * * /home/ubuntu/.pyenv/shims/aws s3 cp /home/ubuntu/trace.log s3://{4} > /dev/null 2>&1" >> mycron
    sudo -u ubuntu echo "*/1 * * * * /home/ubuntu/.pyenv/shims/aws s3 sync /home/ubuntu/completed s3://{4} > /dev/null 2>&1" >> mycron

    sudo -u ubuntu /usr/bin/crontab mycron
    sudo -u ubuntu /bin/rm /home/ubuntu/mycron

    PATH="/usr/local/cuda/bin:$PATH"
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"

    sudo -u ubuntu cd /home/ubuntu/{6}
    
    sudo -u ubuntu touch trace.log
    sudo -u ubuntu echo `pwd` >> trace.log  2>&1
    sudo -u ubuntu echo `which python` >> trace.log  2>&1
    sudo -u ubuntu echo 'repository_name: {6}' >> trace.log 2>&1
    sudo -u ubuntu echo 'dataget_command: {7}' >> trace.log 2>&1
    sudo -u ubuntu echo 'exec_command: {8}' >> trace.log 2>&1
    sudo -u ubuntu {7}  > /dev/null 2>> trace.log
    sudo -u ubuntu echo `ls /home/ubuntu/data | wc` >> trace.log 

    PATH="/usr/local/cuda/bin:$PATH"
    LD_LIBRARY_PATH="/usr/local/cuda/lib64:$LD_LIBRARY_PATH"
    sudo -u ubuntu -i {8}  >> trace.log 2>&1
    sudo -u ubuntu touch /home/ubuntu/completed/completed.log
    '''

    shell_code = shell.format(
        event["data_dir"],
        event["output_dir"],
        os.environ.get('S3_ACCESS_KEY_ID'), 
        os.environ.get('S3_SECRET_ACCESS_KEY'), 
        event["exec_name"],
        event["repository_url"], 
        event["repository_name"],
        event["data_get_command"],
        event["exec_command"]
        )
    user_data = base64.encodestring(shell_code.encode('utf-8')).decode('ascii')
    response = request_spot_instance(user_data)
    event["spot_instance_request_id"] = response["SpotInstanceRequests"][0]["SpotInstanceRequestId"]
    return event

if __name__ == "__main__":
    lambda_handler("","")
