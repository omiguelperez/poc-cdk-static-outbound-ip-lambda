import aws_cdk as cdk

from stacks.cdk_first_cdkv2_serverless_python_stack import (
    CdkFirstCdkv2ServerlessPythonStack,
)

app = cdk.App()
CdkFirstCdkv2ServerlessPythonStack(app, "CdkFirstCdkv2ServerlessPythonStack")

app.synth()
