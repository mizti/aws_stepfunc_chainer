import boto3
import json
import logging
import os

REGION = 'ap-northeast-1'

def request_spot_instance(access_key, secret_key):
    print(access_key)
    print(secret_key)
    ec2_client = boto3.client('ec2',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = REGION
    )
    #ec2_client.create_instances(ImageId='ami-5860093f', MinCount=1, MaxCount=5)
    response = ec2_client.request_spot_instances(
        SpotPrice = '0.2',
        Type='one-time',
        LaunchSpecification = {
            'ImageId': 'ami-5860093f',
            'KeyName': 'miz_private_key',
            #'SecurityGroups': [
            #    'sg-6bd2780c'
            #],
            'UserData':'',
            'InstanceType':'c4.large',
            'Placement':{},
            'SecurityGroupIds':[
                'sg-6bd2780c'         
            ]
        }
    )


def lambda_handler(event, context):
    print(os.environ['AWS_ACCESS_KEY_ID'])
    request_spot_instance(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'))
    return event, context

if __name__ == "__main__":
    lambda_handler("","")
