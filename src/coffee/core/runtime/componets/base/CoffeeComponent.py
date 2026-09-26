from abc import ABC, abstractmethod

class CoffeeComponent(ABC):
    regitry = None

    def initialize(self) -> None:
        pass
