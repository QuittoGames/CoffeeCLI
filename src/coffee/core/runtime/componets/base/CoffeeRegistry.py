from typing import TypeVar
from dataclasses import dataclass
from abc import ABC, abstractmethod

from coffee.core.runtime.componets.base.CoffeeComponent import CoffeeComponent


@dataclass
class CoffeeRegistry(ABC):
    domain = TypeVar("domain", bound=CoffeeComponent)

    def register(self) -> None: ...
