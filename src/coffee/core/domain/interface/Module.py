from dataclasses import dataclass
from abc import abstractmethod,ABC

@dataclass(frozen=True, slots=True)
class ModuleRegistry(ABC):
    id:str
    name:str
    version:str
