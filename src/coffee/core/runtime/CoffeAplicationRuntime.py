from core.data.Config import Config
from core.runtime.contener.CoffeeApplicationContainer import CoffeeApplicationContainer


class CoffeeApplicationRuntime:
    _container: CoffeeApplicationContainer | None = None

    @classmethod
    def init(cls) -> None:
        if cls._container is not None:
            return

        config = Config().build()

        cls._container = CoffeeApplicationContainer(
            config=config,
        )

    @classmethod
    def getContainer(cls) -> CoffeeApplicationContainer:
        if cls._container is None:
            raise RuntimeError(
                "CoffeeApplicationRuntime is not initialized"
            )

        return cls._container

    @classmethod
    def setConfig(cls, config: Config) -> None:
        cls.getContainer().setConfig(config)

    @classmethod
    def stop(cls) -> bool:
        cls._container = None
        return True
