from coffee.core.runtime.container.DefaultCoffeeRegistry import DefaultCoffeeRegistry
from coffee.core.runtime.components.base.CoffeeComponent import CoffeeComponent

registry = DefaultCoffeeRegistry()


def Component(component: CoffeeComponent) -> CoffeeComponent:
    registry.register(component)
    return component
