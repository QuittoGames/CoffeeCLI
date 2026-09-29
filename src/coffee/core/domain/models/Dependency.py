from dataclasses import dataclass,field
from uuid import UUID, uuid4

@dataclass
class Dependency:
    id:UUID = uuid4()
    name:str = field(default_factory=str)
    classImpl: type | None = None
