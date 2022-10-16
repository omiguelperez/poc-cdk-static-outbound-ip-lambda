import os
from typing import Optional, Sequence
from aws_cdk.aws_lambda import LayerVersion, Code, Architecture, Runtime
from aws_cdk import RemovalPolicy
from constructs import Construct


class PythonLayer(LayerVersion):
    def __init__(
        self,
        scope: Construct,
        id: str,
        *,
        code: Code,
        compatible_architectures: Optional[Sequence[Architecture]] = None,
        compatible_runtimes: Optional[Sequence[Runtime]] = None,
        description: Optional[str] = None,
        layer_version_name: Optional[str] = None,
        license: Optional[str] = None,
        removal_policy: Optional[RemovalPolicy] = None,
    ):
        _code = Code.from_docker_build(f"{os.getcwd()}{code}")

        super().__init__(
            scope,
            id,
            code=_code,
            compatible_architectures=compatible_architectures,
            compatible_runtimes=compatible_runtimes,
            description=description,
            layer_version_name=layer_version_name,
            license=license,
            removal_policy=removal_policy,
        )
