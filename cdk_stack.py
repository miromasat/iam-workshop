from aws_cdk import (
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    core
)

from aws_cdk.aws_dynamodb import Attribute


class CdkStack(core.Stack):

    def __init__(self, scope: core.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        table = dynamodb.Table(self, "MyGranularTable",
            partition_key=Attribute(name="id", type=dynamodb.AttributeType.NUMBER),
            sort_key=Attribute(name="accessible", type=dynamodb.AttributeType.STRING)
        )

        role = iam.Role(self, "MyGranularRole", 
            assumed_by=iam.ServicePrincipal('ec2.amazonaws.com')
        )
        
        table.grant_read_data(role)
