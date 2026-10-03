from typing import TypeVar
from dataclasses import dataclass
from abc import ABC, abstractmethod

from coffee.core.components.CoffeeComponent import CoffeeComponent
from coffee.core.domain.interface.SystemModule import SystemModule
from coffee.core.domain.models.Dependency import Dependency

moduleType = TypeVar("moduleType", bound=SystemModule)


@dataclass
class CoffeeRegistry(ABC):
    domain = TypeVar("domain", bound=CoffeeComponent)

    @classmethod
    @abstractmethod
    def register(cls, component: type) -> type: ...

    @classmethod
    @abstractmethod
    def packageRegister(cls, module: type[moduleType]) -> type[moduleType]: ...

    @classmethod
    @abstractmethod
    def contains(cls, component: type) -> bool: ...

    @classmethod
    @abstractmethod
    def get(cls, component: type) -> type | None: ...

    @classmethod
    @abstractmethod
    def getModule(cls, module: type) -> type[SystemModule] | None: ...

    @classmethod
    @abstractmethod
    def all(cls) -> tuple[Dependency, ...]: ...
