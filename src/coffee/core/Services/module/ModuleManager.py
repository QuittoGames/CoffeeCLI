from dataclasses import dataclass, field
from coffee.core.runtime.componets.Componet import Component
from coffee.core.domain.interface.SystemModule import SystemModule


@dataclass
@Component
class ModuleManager:
    _modulesRegistry: list[SystemModule] = field(default_factory=list)

    def loadModules(self) -> list[SystemModule]:
        return self._modulesRegistry
