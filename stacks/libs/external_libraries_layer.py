from constructs import Construct
from stacks.libs.constants import COMPATIBLE_RUNTIMES

from stacks.libs.python_layer import PythonLayer


class ExternalLibrariesLayer(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        self.__layer = PythonLayer(
            self,
            id,
            description="Layer for external libraries",
            code="/src/layers/external",
            compatible_runtimes=COMPATIBLE_RUNTIMES,
        )

    @property
    def layer(self):
        return self.__layer
