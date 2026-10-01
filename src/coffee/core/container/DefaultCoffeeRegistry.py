from typing import TypeVar
from uuid import uuid4

from coffee.core.domain.models.Dependency import Dependency
from coffee.core.domain.interface.SystemModule import SystemModule
from coffee.core.components.CoffeeComponent import CoffeeComponent
from coffee.core.container.CoffeeRegistry import CoffeeRegistry

moduleType = TypeVar("moduleType", bound=SystemModule)


class DefaultCoffeeRegistry(CoffeeRegistry):
    dependencies: list[Dependency] = []
    systemModules: list[type[SystemModule]] = []

    @classmethod
    def register(cls, component: type[CoffeeComponent]) -> type[CoffeeComponent]:
        cls.dependencies.append(
            Dependency(id=uuid4(), name=component.__name__, classImpl=component)
        )
        return component

    @classmethod
    def packageRegister(cls, module: type[moduleType]) -> type[moduleType]:
        cls.systemModules.append(module)
        return module

    @classmethod
    def contains(cls, component: type) -> bool:
        return cls.get(component) is not None

    @classmethod
    def get(cls, component: type) -> type | None:
        for dependency in cls.dependencies:
            if dependency.classImpl is component:
                return dependency.classImpl
        return None

    @classmethod
    def getModule(cls, module: type) -> type[SystemModule] | None:
        for registered in cls.systemModules:
            if registered is module:
                return registered
        return None

    @classmethod
    def all(cls) -> tuple[Dependency, ...]:
        return tuple(cls.dependencies)
