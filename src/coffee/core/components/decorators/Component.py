from typing import TypeVar

from coffee.core.container.registry import registry
from coffee.core.components.CoffeeComponent import CoffeeComponent

T = TypeVar("T", bound=CoffeeComponent)

class ComponentDecorator:
    def __call__(self, component: type[T]) -> type[T]:
        registry.register(component)
        return component

Component = ComponentDecorator()
