# AWS IAM (IAM) Workshop 2021
A short workshop demonstrating multiple ways of accessing DynamoDB table.
The goal here, is to explain ways of letting two AWS resources interact with each other. One resource will be
Amazon EC2 (EC2) instance and the other will be Amazon DynamoDB (DDB) Table (alternatively with row-level security).

## Prerequisites
1. Execute AWS CloudFormation (CF) template attached in this repository named `setup.yaml`. This CF template creates one EC2 instance and one DDB Table. EC2 instance will be utilizing basic Amazon Linux2 OS and AWS CDK preinstalled.
    * you can execute this CF template in two different ways:
    * Through AWS CLI: `aws cloudformation   create-stack --stack-name iamworkshop2021setup --template-url mybucket/setup.yaml`
    * Through AWS Console. Navigate to CF Console and follow the wizard, attach the setup.yaml file as part of the configuration.
2. Log-in into EC2 instance that was created. Verify, that these commands work:
    * `cdk --version`, which ensure aws binary is installed
    * `aws --version`, which ensures cdk binary is installed
    * `aws ec2 describe-instances`, this call should fail with unauthorised message 
3. Start by going into IAM and create an IAM Role with attached managed PowerUser Policy. Name this role `pu-access`
    * PowerUser Policy document is very powerfull and will initially let us access not only DDB (and all its content) but all other services with the exception of IAM itself.
    * More about managed policies [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_managed-vs-inline.html#aws-managed-policies)
4. Attach this newly created role `pu-access` to the instance you are logged into from `Step 2`. To verify, that instance can now access other services, rerun command `aws ec2 describe-instances` from before.
    * Notice, that the instance did not need to be restarted.
    * Notice, that by querying the metaservice `curl 169.254.169.254` you get temporary credetials that in turn let you execute commands.
5. Let's now create another IAM Role, this time, using AWS IAM Policy Wizard. After going into IAM Console, we navigate into Policies Submenu and we follow the wizard and call the role `ddb-ro-access-policy`:
    * pick `DynamoDB` as a `Service` 
    * pick `Read` as an `Action`
6. After we create the policy, we create the Role, that we call `ddb-ro-access` and use Policy `ddb-ro-access-policy`, which we created in the `Step 5`
7. Go back to instance from `Step 2` and `Step 4` and try to use this newly created role `ddb-ro-access`. We can do this in two ways:
    * Attach this new role `ddb-ro-access` replacing the old role `pu-access`
    * Assume this new role by AWS SimpleTokenService (STS) via this shortcut command: 
    `eval $(aws sts assume-role --role-arn arn:aws:iam::123456789123:role/ddb-ro-access --role-session-name test | jq -r '.Credentials | "export AWS_ACCESS_KEY_ID=\(.AccessKeyId)\nexport AWS_SECRET_ACCESS_KEY=\(.SecretAccessKey)\nexport AWS_SESSION_TOKEN=\(.SessionToken)\n"')`
    Inspired by this [StackOverFlow post](https://stackoverflow.com/questions/63241009/aws-sts-assume-role-in-one-command)
