from abc import ABC
from coffee.core.runtime.componets.base.CoffeeComponent import CoffeeComponent


class SystemModule(CoffeeComponent, ABC):
    __slots__ = ("_id", "_name", "_version")

    def __init__(self, id: str, name: str, version: str) -> None:
        self._id = id
        self._name = name
        self._version = version

    @property
    def id(self) -> str:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, value: str) -> None:
        self._version = value
