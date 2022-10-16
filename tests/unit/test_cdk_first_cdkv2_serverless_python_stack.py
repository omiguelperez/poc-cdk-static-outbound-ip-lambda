import aws_cdk as core
import aws_cdk.assertions as assertions

from stacks.cdk_first_cdkv2_serverless_python_stack import (
    CdkFirstCdkv2ServerlessPythonStack,
)

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_first_cdkv2_serverless_python/cdk_first_cdkv2_serverless_python_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkFirstCdkv2ServerlessPythonStack(app, "cdk-first-cdkv2-serverless-python")
    template = assertions.Template.from_stack(stack)


#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
