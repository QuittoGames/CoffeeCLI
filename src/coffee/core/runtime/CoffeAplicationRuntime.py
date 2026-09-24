from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable

from core.data.Config import Config
from core.runtime.contener.CoffeeApplicationContainer import CoffeeApplicationContainer
from core.runtime.contener.CofeeRegistry import CoffeeRegistry

@dataclass
class CoffeeApplicationRuntime:

    def __init__(self):
        self.container: CoffeeApplicationContainer | None = None

    def init(self) -> None:
        config = Config().build()

        self.container = CoffeeApplicationContainer(
            config=config,
        )

    def getContainer(self) -> CoffeeApplicationContainer:
        if self.container is None:
            raise RuntimeError(
                "CoffeeApplicationRuntime is not initialized"
            )

        return self.container

    def setConfig(self,config:Config) -> None:
        self.container.setConfig(config=config)

    def stop(self) -> bool:
        self.container = None
        return True
