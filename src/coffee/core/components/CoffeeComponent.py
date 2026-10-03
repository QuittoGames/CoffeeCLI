from abc import ABC
from typing import Any


class CoffeeComponent(ABC):
    def __init__(self) -> None:
        self.container = None

    def initialize(self, container: Any | None = None) -> None:
        self.container = container

    def get(self, key: str) -> Any:
        return self.container
