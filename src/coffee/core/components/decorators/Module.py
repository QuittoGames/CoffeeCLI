from typing import TypeVar

from coffee.core.domain.interface.SystemModule import SystemModule
from coffee.core.container.registry import registry

T = TypeVar("T", bound=SystemModule)


def Module(module: type[T]) -> type[T]:
    registry.packageRegister(module=module)
    return module
