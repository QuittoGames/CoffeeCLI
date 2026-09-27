from coffee.core.runtime.contener.CofeeRegistry import DefaultCoffeeRegistry
from coffee.core.domain.interface.SystemModule import SystemModule
from typing import TypeVar

registry = DefaultCoffeeRegistry()

component = TypeVar("component", bound=SystemModule)


def Component(component: SystemModule) -> SystemModule:
    registry.packageRegister(component)
    return component
