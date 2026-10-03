from abc import ABC
from typing import TypeVar

from coffee.core.domain.interface.ApplicationContainer import ApplicationContainer
from coffee.core.runtime.CoffeeApplicationContext import CoffeeApplicationContext

T = TypeVar("T")

class CoffeeComponent(ABC):
    @property
    def container(self) -> ApplicationContainer:
        return CoffeeApplicationContext.getApp().getContainer()

    def get(self, component: type[T]) -> T:
        return self.container.get(component)
