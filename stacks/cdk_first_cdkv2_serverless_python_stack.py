from aws_cdk import (
    Stack,
)
from json import dumps
import aws_cdk.aws_lambda as lambda_
import aws_cdk.aws_dynamodb as dynamo_
import aws_cdk.aws_apigateway as apigateway_
from constructs import Construct

from stacks.libs.external_libraries_layer import ExternalLibrariesLayer


class CdkFirstCdkv2ServerlessPythonStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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
        )

        db_table.grant_read_write_data(lambda_func)

        # API Gateway
        api_gw = apigateway_.RestApi(self, "MyDemoAPIGateway")

        lambda_func_api_gw_integration = apigateway_.LambdaIntegration(
            lambda_func,
            request_templates={"application/json": dumps({"status_code": 200})},
        )
        api_gw.root.add_method("GET", lambda_func_api_gw_integration)
