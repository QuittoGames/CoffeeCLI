from coffee.core.runtime.container.DefaultCoffeeRegistry import DefaultCoffeeRegistry

registry = DefaultCoffeeRegistry()


def Module(module: type) -> type:
    registry.register(module)
    return module
