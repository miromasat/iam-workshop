
from constructs import Construct

from aws_cdk import (
    Duration,
    Stack,
    aws_iam as iam,
    aws_dynamodb as dynamodb
)

from aws_cdk.aws_dynamodb import Attribute


class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        table = dynamodb.Table(self, "MyGranularTable",
            partition_key=Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            sort_key=Attribute(name="accessible", type=dynamodb.AttributeType.STRING),
            table_name="granular"
        )

        role = iam.Role(self, "MyGranularRole", 
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com'),
            role_name="ddb-ro-granular-access"
        )

        ec2Runnerinstanceprofile = iam.CfnInstanceProfile(
            self, "MyInstanceProfile",
            instance_profile_name="ddb-ro-granular-access",
            roles=["ddb-ro-granular-access"]
        )
        
        table.grant_read_data(role)

        