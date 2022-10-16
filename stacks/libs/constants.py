from typing_extensions import runtime
from aws_cdk.aws_lambda import Runtime
from aws_cdk import Duration

DEFAULT_RUNTIME = Runtime.PYTHON_3_9
COMPATIBLE_RUNTIMES = [
    Runtime.PYTHON_3_8,
    Runtime.PYTHON_3_9,
]
DEAFULT_LAMBDA_TIMEOUT_IN_SECONDS = Duration.seconds(15)
