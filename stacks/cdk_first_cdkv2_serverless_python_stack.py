from unicodedata import name
from aws_cdk import (
    Stack,
)
from json import dumps
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_dynamodb as dynamo_
import aws_cdk.aws_apigateway as apigateway_
import aws_cdk.aws_ec2 as ec2_
from constructs import Construct

from stacks.libs.external_libraries_layer import ExternalLibrariesLayer


class CdkFirstCdkv2ServerlessPythonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        vpc = ec2_.Vpc(
            self,
            "Static-Outbound-IP-VPC",
            cidr="10.0.0.0/16",
            nat_gateways=1,
            max_azs=3,
            subnet_configuration=[
                ec2_.SubnetConfiguration(
                    name="private-subnet-1",
                    subnet_type=ec2_.SubnetType.PRIVATE_WITH_NAT,
                    cidr_mask=24,
                ),
                ec2_.SubnetConfiguration(
                    name="public-subnet-1",
                    subnet_type=ec2_.SubnetType.PUBLIC,
                    cidr_mask=24,
                ),
            ],
        )

        # DynamoDB table
        db_table = dynamo_.Table(
            self,
            "MyDemoTable",
            billing_mode=dynamo_.BillingMode.PAY_PER_REQUEST,
            table_name="MyDemoTable",
            partition_key=dynamo_.Attribute(
                name="id", type=dynamo_.AttributeType.STRING
            ),
        )

        # Layers
        external_layer = ExternalLibrariesLayer(self, "external-libs-layer").layer
        self.__layers = [
            external_layer,
        ]

        # Lambda function
        lambda_func = lambda_.Function(
            self,
            "MyDemoFunction",
            runtime=lambda_.Runtime.PYTHON_3_9,
            code=lambda_.Code.from_asset("src/items"),
            handler="app.handler",
            environment={
                "MY_TABLE": db_table.table_name,
            },
            layers=self.__layers,
            vpc=vpc,
            vpc_subnets=ec2_.SubnetSelection(
                subnet_type=ec2_.SubnetType.PRIVATE_WITH_NAT,
            ),
        )

        db_table.grant_read_write_data(lambda_func)

        # API Gateway
        api_gw = apigateway_.RestApi(self, "MyDemoAPIGateway")

        lambda_func_api_gw_integration = apigateway_.LambdaIntegration(
            lambda_func,
            request_templates={"application/json": dumps({"status_code": 200})},
        )
        api_gw.root.add_method("GET", lambda_func_api_gw_integration)
