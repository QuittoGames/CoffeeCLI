from dataclasses import dataclass,field
from coffee.core.runtime.componets.Componet import Component
from coffee.core.domain.interface.Module import Module

@dataclass
@Component
class ModuleManager:
    _modulesRegistry:list[Module] = field(default_factory=list)

    def loadModules(self) -> list[Module]:
        try:
            self
        except RuntimeError as E:
            raise RuntimeError()
