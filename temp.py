from boto import ec2
import os
REGION = 'ap-northeast-1'
EC2_KEY_NAME = 'miz_private_key'
INSTANCE_TYPE = 'c4.large'
SECURITY_GROUPS = ['sg-6bd2780c']

INSTANCE_BID = 0.1
AMI_ID= 'ami-be4a24d9'

def _get_cloudconfig():
    base_path = os.path.dirname(os.path.realpath(__file__))
    cloud_config = open(os.path.join(base_path, 'cloud_config.yml'))
    return cloud_config.read()

conn = ec2.connect_to_region(REGION,
         aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
         aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'))

instance_params = {
    'count': 1,
    'key_name': EC2_KEY_NAME,
    'user_data': _get_cloudconfig(),
    'instance_type': INSTANCE_TYPE,
    'security_group_ids': SECURITY_GROUPS
}

spot_reqs = conn.request_spot_instances(INSTANCE_BID, AMI_ID, **instance_params)
print(spot_reqs)
