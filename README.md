# AWS IAM (IAM) Workshop 2021
A short workshop demonstrating multiple ways of accessing DynamoDB table.
The goal here, is to explain ways of letting two AWS resources interact with each other. One resource will be
Amazon EC2 (EC2) instance and the other will be Amazon DynamoDB (DDB) Table (alternatively with row-level security).

## Architectural Diagram:
![Architectural Diagram](/img/iam-workshop.jpg)

## Prerequisites
* be logged into AWS
* be consistently in one AWS region, preferably in us-east-1
* generate a EC2 KeyPair in the EC2 Console and call it `iamworkshop2021key`

## Steps
1. Execute AWS CloudFormation (CF) template attached in this repository named `setup.yaml`. This CF template creates one EC2 instance and one DDB Table. EC2 instance will be utilizing basic Amazon Linux2 OS and AWS CDK preinstalled.
    * you can execute this CF template in two different ways:
    * Through AWS CLI: `aws cloudformation create-stack --stack-name iamworkshop2021setup --template-body file:///home/ec2-user/environment/iam-workshop-2021/template.yaml --parameters ParameterKey=KeyName,ParameterValue=iamworkshop2021key`
    * Through AWS Console. Navigate to CF Console and follow the wizard, attach the setup.yaml file as part of the configuration.
2. Log-in into EC2 instance that was created.
    * Use the keypair, you have created as a prerequisite and Public IP Address of the newly created EC2 instance, example of the command: `chmod 400 ./iamworkshop2021key.pem && ssh -i iamworkshop2021key.pem ec2-user@PublicIPAddress`
    * Verify, that these commands work:
        * `cdk --version`, which ensure cdk binary is installed
        * `aws --version`, which ensures aws binary is installed
    * take a look at `~/iamworkshop/granular-testt.py` file and spend a minute understanding it.
    * run `python3 ~/iam-workshop/granular-test.py` and discuss results and see eveything fail :) why?
3. Start by going into IAM and create an IAM Role with attached managed AdministratorAccess Policy. Name this role `pu-access`
    * AdministratorAccess Policy document is very powerfull and will initially let us access not only DDB (and all its content) but all other services.
    * More about managed policies [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies)
4. Attach this newly created role `pu-access` to the instance you are logged into from `Step 2`. To verify, that instance can now access other services.
    * Notice, that the instance did not need to be restarted.
    * Notice, that by querying the metaservice `curl http://169.254.169.254/latest/meta-data/iam/security-credentials/<role-name>` and `curl http://169.254.169.254/latest/meta-data/iam/info` you get temporary credetials that in turn let you execute commands.
    * rerun `python3 ~/iam-workshop/granularity_test.py` and discuss results
5. Let's now create another IAM Role, this time, using AWS IAM Policy Wizard. After going into IAM Console, we navigate into Policies Submenu and we follow the wizard and call the role `ddb-ro-access-policy`:
    * pick `DynamoDB` as a `Service` 
    * pick `Read` as an `Action`
6. After we create the policy, we create the Role, that we call `ddb-ro-access` and use Policy `ddb-ro-access-policy`, which we created in the `Step 5`
7. Go back to instance from `Step 2` and `Step 4` and try to use this newly created role `ddb-ro-access`. We can do this by:
    * Attach this role onto EC2 instance.
    * Alternatively, you can sssume this new role by AWS SimpleTokenService (STS) via this shortcut command: 
    `eval $(aws sts assume-role --role-arn arn:aws:iam::123456789123:role/ddb-ro-access --role-session-name test | jq -r '.Credentials | "export AWS_ACCESS_KEY_ID=\(.AccessKeyId)\nexport AWS_SECRET_ACCESS_KEY=\(.SecretAccessKey)\nexport AWS_SESSION_TOKEN=\(.SessionToken)\n"')`
    Inspired by this [StackOverFlow post](https://stackoverflow.com/questions/63241009/aws-sts-assume-role-in-one-command)
    * Did this succeed? If not, why?
    * rerun `python3 ~/iam-workshop/granularity_test.py` and discuss results
8. (Consider doing this step in AWS Cloud9 environment) Create a new folder called `cdk`, enter it `cd cdk` and innitiate a new project via `cdk init sample-app --language python` 
    * Take a look into the folder called `cdk`, this folder contains a simple CDK construct with some AWS SNS and AWS SQS constructs.
    * CDK serves a deployment mechanism for AWS, similarly to cloudformation and/or terraform, we could learn from ways it works and inner functioning how to enable granular policy generation. 
    * learn more about CDK, [here](https://aws.amazon.com/cdk/)
    * create a new folder and enter it `mkdir ~/cdk && cd ~/cdk`
    * run `cdk init sample-app --language python`
    * activate virtualenv via `source .venv/bin/activate` 
    * install project dependencies using `pip install -r requirements.txt`
    * replace `cdk/cdk_stack.py` for a file that you can find in this repo. Explore the file.
    * run `cdk bootstrap`
9. By running `cd synth`, we generate the AWS Clouformation template for Role, that goes like `ddb-ro-granular-access` and use very granular Policy. We also generate a new DynamoDB table called `granular`
    * we can look at this template under `~/cdk/cdk.out/cdk.template.json`
    * repeat `Step 4`
10. By running `cd deploy`, we deploy these new resources, we mark a newly created role, wich allows for very granular scan only access to newly created DynamoDB Table
11. Attach this newly created role to the same EC2 similarly to `Step 7`, rerun `python3 ~/iam-workshop/granularity_test.py` and discuss results
