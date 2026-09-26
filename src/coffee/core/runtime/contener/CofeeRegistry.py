from coffee.core.domain.interface.SystemModule import SystemModule
from coffee.core.runtime.componets.base.CoffeeComponent import CoffeeComponent
from typing import TypeVar

T = TypeVar("T", bound=SystemModule)


class CoffeeRegistry:
    components: dict[type, type] = {}
    moduleRegestry: dict[str, SystemModule] = {}

    @classmethod
    def register(cls, component: type) -> type:
        cls.components[component] = component
        return component

    @classmethod
    def packageRegister(cls, module: T) -> T:
        cls.moduleRegestry[module.id] = module
        return module

    @classmethod
    def contains(cls, component: type) -> bool:
        return component in cls.components

    @classmethod
    def get(cls, component: type) -> type | None:
        return cls.components.get(component)

    @classmethod
    def getModule(cls, module: type) -> type | None:
        return cls.components.get(module)

    @classmethod
    def all(cls) -> tuple[type, ...]:
        return tuple(cls.components.keys())
