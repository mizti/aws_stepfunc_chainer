import boto3
import botocore
import boto3.s3.transfer
import os

def lookup(s3, bucket_name):
	try:
		s3.meta.client.head_bucket(Bucket=bucket_name)
	except botocore.exceptions.ClientError as e:
		error_code = int(e.response['Error']['Code'])

		if error_code == 404:
			return False

		return True

def create_bucket():
	s3 = boto3.resource('s3')
	bucket_name = 'test-kick-the-bucket23'
	bucket = s3.Bucket(bucket_name)

	if not lookup(s3, bucket_name):
		s3.create_bucket(Bucket=bucket_name)
	else:
		print("Already exists!")

if __name__ == '__main__':
	create_bucket()
