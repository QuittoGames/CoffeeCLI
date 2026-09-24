from dataclasses import dataclass
from core.data.Config import Config
from core.Services.module.ModuleManager import ModuleManager
from core.runtime.contener.CofeeRegistry import CoffeeRegistry
import inspect

class CoffeeApplicationContainer:
    depencies: dict[inspect.Signature , type]

    def __init__(self, config: Config):
        self.config = config

    def _create(dependecy:type) -> type:
        if dependecy is None: raise RuntimeError()
        signature: inspect.Signature = inspect.signature(dependecy.__init__)

        if signature is None or signature.empty(): raise RuntimeError()

        for parameters in signature.parameters.values():
            if parameters == "self": continue


    def get(self, component: type):
        implementation = CoffeeRegistry.get(component)

        if implementation is None:
            raise LookupError(
                f"Component not registered: {component.__name__}"
            )

        return implementation()

    def getConfig(self) -> Config:
        return self.config

    def setConfig(self, config: Config) -> None:
        self.config = config
