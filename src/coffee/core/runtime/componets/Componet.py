from core.runtime.contener.CofeeRegistry import CoffeeRegistry

registry = CoffeeRegistry()

def Component(component: type) -> type:
    registry.packageRegister(component)
    return component
