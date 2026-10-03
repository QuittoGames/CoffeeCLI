from dataclasses import dataclass, field
from pathlib import Path
import sys
from coffee.core.components.decorators.Component import Component
from coffee.core.components.CoffeeComponent import CoffeeComponent
from coffee.core.domain.interface.SystemModule import SystemModule

@dataclass
@Component
class ModuleManager(CoffeeComponent):
    _modulesRegistry: list[SystemModule] = field(default_factory=list)

    def loadModules(self) -> list[SystemModule]:
        # dataPath: Path = self.configPath / "coffee"
        return self._modulesRegistry
