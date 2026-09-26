from coffee.core.runtime.contener.CofeeRegistry import CoffeeRegistry
from coffee.core.runtime.componets.base.CoffeeComponent import CoffeeComponent
from typing import TypeVar

registry = CoffeeRegistry()

component = TypeVar("component", bound=CoffeeComponent)


def Component(component: type) -> type:
    registry.packageRegister(component)
    return component
