import inspect

from coffee.core.data.Config import Config
from coffee.core.domain.interface.SystemModule import SystemModule
from coffee.core.runtime.contener.CofeeRegistry import CoffeeRegistry


class CoffeeApplicationContainer:
    dependencie: list[SystemModule] = []

    def __init__(self, config: Config):
        self.config = config

    def _create(self, dependency: type) -> type:
        if dependency is None:
            raise RuntimeError("Dependency cannot be None")

        signature = inspect.signature(dependency.__init__)

        for parameter in signature.parameters.values():
            if parameter.name == "self":
                continue

            print(
                f"name={parameter.name}, "
                f"type={parameter.annotation}, "
                f"default={parameter.default}"
            )
        raise NotImplementedError("_create() is not implemented yet")

    def get(self, component: type):
        implementation = CoffeeRegistry.get(component)

        if implementation is None:
            raise LookupError(f"Component not registered: {component.__name__}")

        return implementation()

    def getConfig(self) -> Config:
        return self.config

    def setConfig(self, config: Config) -> None:
        self.config = config
