#!/bin/sh
sudo -s ubuntu
cd /home/ubuntu
sudo -u ubuntu mkdir /home/ubuntu/.aws
sudo -u ubuntu echo "[default]" >> /home/ubuntu/.aws/credentials
sudo -u ubuntu echo "aws_access_key_id={0}" >> /home/ubuntu/.aws/credentials
sudo -u ubuntu echo "aws_secret_access_key={1}" >> /home/ubuntu/.aws/credentials

sudo -u ubuntu echo "*/10 * * * * /home/ubuntu/.pyenv/shims/aws s3 sync /home/ubuntu/result s3://{2} > /dev/null 2>&1" >> mycron
sudo -u ubuntu /usr/bin/crontab mycron
sudo -u rm mycron

sudo -u ubuntu git clone {3}
sudo -u ubuntu cd {4}
# exec train && touch home/ubuntu/completed.txt

