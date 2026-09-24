from dataclasses import dataclass,field
from core.runtime.componets.Componets import Component
from core.domain.models.Module import Module

@dataclass
@Component
class ModuleManager:

    def loadModules(self) -> list[Module]:
        try:
            pass
        except RuntimeError as E:
            raise RuntimeError()
