#!/bin/bash -xe

curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.34.0/install.sh | bash
. ~/.nvm/nvm.sh
nvm install node
npm install -g aws-cdk
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py
pip install boto3
