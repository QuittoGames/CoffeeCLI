from abc import ABC, abstractmethod

class CoffeeComponent(ABC):
    registry = None

    def initialize(self) -> None:
        pass
