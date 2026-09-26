from coffee.core.runtime.contener.CofeeRegistry import CoffeeRegistry

registry = CoffeeRegistry()


def Module(module: type) -> type:
    registry.register(module)
    return module
