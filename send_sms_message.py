#!/usr/bin/env python
# -*- coding: utf-8 -*-
import boto3
import json
import os

#TOPIC_ARN = 'arn:aws:sns:ap-northeast-1:517180089186:training_ended' # SMS
TOPIC_ARN = 'arn:aws:sns:ap-northeast-1:517180089186:training_end_notification_mail' # Mail
REGION = 'ap-northeast-1'


def send_sms_message(event, context):
    sns = boto3.client('sns',
        region_name = REGION
    )

    message = ''
    subject = ''
    if "completed" in event:
        subject = 'Training ended'
        message = '''task completed!
        result: https://console.aws.amazon.com/s3/home?bucket={0}
        
        -----
        {1}
        '''.format(event["exec_name"], event)
    else:
        if event["request_result"]:
            subject = 'request fulfilled'
            message = '''
            Spot Request Fulfilled! {0}
            '''.format(event["exec_name"])
        else:
            subject = 'request failed'
            message = '''
            Spot Request Fails! {0}
            '''.format(event["exec_name"])
    
        response = sns.publish(
            TopicArn = TOPIC_ARN,
            Subject = subject,
            Message = message
        )
    
    return response

def lambda_handler(event, context):
    response = send_sms_message(event, context)
    return event

if __name__ == "__main__":
    lambda_handler("","")
