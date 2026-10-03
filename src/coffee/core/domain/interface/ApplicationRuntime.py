from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from coffee.config.Config import Config
from coffee.core.domain.interface.ApplicationContainer import ApplicationContainer


class ApplicationRuntime(ABC):
    @abstractmethod
    def __init__(self, func: Callable[..., object] | None = None) -> None: ...

    @classmethod
    @abstractmethod
    def init(cls) -> None: ...

    @classmethod
    @abstractmethod
    def getContainer(cls) -> ApplicationContainer: ...

    @classmethod
    @abstractmethod
    def setConfig(cls, config: Config) -> None: ...

    @classmethod
    @abstractmethod
    def stop(cls) -> bool: ...

    @abstractmethod
    def __call__(self, *args: object, **kwargs: object) -> Any: ...
