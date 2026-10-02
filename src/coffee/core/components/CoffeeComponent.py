from abc import ABC

class CoffeeComponent(ABC):
    registry = None

    def initialize(self) -> None:
        pass
