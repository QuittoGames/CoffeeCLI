from typing import TypeVar
from dataclasses import dataclass
from abc import ABC, abstractmethod

from coffee.core.runtime.components.base.CoffeeComponent import CoffeeComponent
from coffee.core.domain.interface.SystemModule import SystemModule


T = TypeVar("T", bound=SystemModule)

@dataclass
class CoffeeRegistry(ABC):
    domain = TypeVar("domain", bound=CoffeeComponent)

    @classmethod
    def register(cls, component: type) -> type: ...

    @classmethod
    def contains(cls, component: type) -> bool: ...
