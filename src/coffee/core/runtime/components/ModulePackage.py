from coffee.core.runtime.container.DefaultCoffeeRegistry import DefaultCoffeeRegistry

registry = DefaultCoffeeRegistry()


def Module(module: type) -> type:
    registry.packageRegister(module)
    return module
