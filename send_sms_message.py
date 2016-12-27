#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import os

TOPIC_ARN = 'arn:aws:sns:ap-northeast-1:517180089186:training_ended'
REGION = 'ap-northeast-1'

def send_sms_message(access_key, secret_key, event):
    sns = boto3.client('sns',
        aws_access_key_id = access_key,
        aws_secret_access_key = secret_key,
        region_name = REGION
    )
    sns_body={}
    sns_body["default"] = "Your Training Ended!!"
    topic = TOPIC_ARN
    response = sns.publish(
        TopicArn = topic,
        Subject = 'Training ended',
        Message = json.dumps(sns_body, ensure_ascii=False),
        MessageStructure = 'json'
    )
    return response


def lambda_handler(event, context):
    response = send_sms_message(os.environ.get('AWS_ACCESS_KEY_ID'), os.environ.get('AWS_SECRET_ACCESS_KEY'), event)
    print(response)
    return event, context

if __name__ == "__main__":
    lambda_handler("","")
