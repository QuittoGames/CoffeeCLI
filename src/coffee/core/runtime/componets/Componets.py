from core.runtime.contener.CofeeRegistry import CoffeeRegistry

registry = CoffeeRegistry()

def Component(component: type) -> type:
    registry.register(component)
    return component
