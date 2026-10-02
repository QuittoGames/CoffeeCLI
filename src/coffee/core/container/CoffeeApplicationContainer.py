import inspect

from coffee.config.Config import Config
from coffee.data.Host import Host
from coffee.core.domain.models.Dependency import Dependency
from coffee.core.domain.interface.SystemModule import SystemModule
from coffee.core.container.DefaultCoffeeRegistry import DefaultCoffeeRegistry

class CoffeeApplicationContainer:
    def __init__(self, config: Config):
        self.config = config
        self.dependencies: list[Dependency] = []
        self.systemModules: list[SystemModule] = []

    def _create(self, dependency: type) -> None:
        if dependency is None:
            raise RuntimeError("Dependency cannot be None")

        signature = inspect.signature(dependency.__init__)

        for parameter in signature.parameters.values():
            if parameter.name == "self":
                continue

            if self.config.Debug:
                print(
                    f"name={parameter.name}, "
                    f"type={parameter.annotation}, "
                    f"default={parameter.default}"
                )
            dep = Dependency(
                name=parameter.name,
                classImpl=parameter.annotation,
            )

            if dep not in self.dependencies:
                self.dependencies.append(dep)

    def get(self, component: type):
        implementation = DefaultCoffeeRegistry.get(component)

        if implementation is None:
            raise LookupError(f"Component not registered: {component.__name__}")

        return implementation()

    def getConfig(self) -> Config:
        return self.config

    def setConfig(self, config: Config) -> None:
        self.config = config
