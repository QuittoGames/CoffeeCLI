from abc import ABC, abstractmethod
from typing import Any
from coffee.config.Config import Config

class ApplicationContainer(ABC):
    @abstractmethod
    def __init__(self, config: Config) -> None: ...

    @abstractmethod
    def get(self, component: type) -> Any: ...

    @abstractmethod
    def getConfig(self) -> Config: ...

    @abstractmethod
    def setConfig(self, config: Config) -> None: ...
