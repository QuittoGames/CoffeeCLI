from coffee.core.runtime.contener.CofeeRegistry import DefaultCoffeeRegistry

registry = DefaultCoffeeRegistry()


def Module(module: type) -> type:
    registry.register(module)
    return module
