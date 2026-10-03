from ast import Not
from dataclasses import dataclass, field
from logging import config
from pathlib import Path
import sys
from coffee.core.components.decorators.Component import Component
from coffee.core.components.CoffeeComponent import CoffeeComponent
from coffee.core.domain.interface.SystemModule import SystemModule

@dataclass
@Component
class ModuleManager(CoffeeComponent):
    _modulesRegistry: list[SystemModule] = field(default_factory=list)

    def __post_init__(self):
        super().__init__()

    def loadModules(self) -> list[SystemModule]:
        try:
            assert self.container is not None

            config = self.container.getConfig()

            dataPath: Path = config.configPath / "coffee"

            print(dataPath)
            return self._modulesRegistry
        except AssertionError as error:
            raise AssertionError("Module manager container must be initialized.") from error
