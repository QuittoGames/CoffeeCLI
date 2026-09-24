from dataclasses import dataclass
from core.data.Config import Config
from core.Services.module.ModuleManager import ModuleManager
from core.runtime.contener.CofeeRegistry import CoffeeRegistry

class CoffeeApplicationContainer:
    def __init__(self, config: Config):
        self.config = config

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
