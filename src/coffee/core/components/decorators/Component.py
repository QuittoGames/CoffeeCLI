from typing import TypeVar

from coffee.core.container.registry import registry
from coffee.core.components.CoffeeComponent import CoffeeComponent

T = TypeVar("T", bound=CoffeeComponent)


def Component(component: type[T]) -> type[T]:
    registry.register(component)
    return component
