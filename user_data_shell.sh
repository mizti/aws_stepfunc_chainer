#!/bin/sh
sudo -s ubuntu
cd /home/ubuntu
mkdir /home/ubuntu/.aws
echo "[default]" >> /home/ubuntu/.aws/credentials
echo "aws_access_key_id={0}" >> /home/ubuntu/.aws/credentials
echo "aws_secret_access_key={1}" >> /home/ubuntu/.aws/credentials
(crontab -l; echo "*/10 * * * * /home/ubuntu/.pyenv/shims/aws s3 sync /home/ubuntu/result s3://{2} > /dev/null 2>&1") | crontab -
git clone {3}
cd {4}
# exec train && touch home/ubuntu/completed.txt

