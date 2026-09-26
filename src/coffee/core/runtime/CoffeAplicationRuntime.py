import inspect
from collections.abc import Callable

from coffee.core.data.Config import Config
from coffee.core.runtime.contener.CoffeeApplicationContainer import (
    CoffeeApplicationContainer,
)


class CoffeeApplicationRuntime:
    _container: CoffeeApplicationContainer | None = None

    def __init__(self, func: Callable[..., object] | None = None) -> None:
        self._func = func

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
            raise RuntimeError("CoffeeApplicationRuntime is not initialized")

        return cls._container

    @classmethod
    def setConfig(cls, config: Config) -> None:
        cls.getContainer().setConfig(config)

    @classmethod
    def stop(cls) -> bool:
        cls._container = None
        return True

    def __call__(self, *args: object, **kwargs: object) -> object:
        """Decorator de lifecycle — init → ponto de entrada → stop (em finally).

        Aceita as duas formas previstas em runtime.md §12.3:

            @CoffeeApplicationRuntime
            @CoffeeApplicationRuntime()

        Em ambas o ponto de entrada recebe o runtime como argumento.
        """
        func = self._func

        if func is None:
            # @CoffeeApplicationRuntime() — ainda estamos na fase de factory.
            if len(args) == 1 and not kwargs and callable(args[0]):
                self._func = args[0]
                return self
            raise TypeError("CoffeeApplicationRuntime() requires a target function")

        if args or kwargs:
            raise TypeError(
                "the decorated entry point receives only the runtime context"
            )

        if inspect.iscoroutinefunction(func):
            return self._invokeAsync(func)

        self.init()
        try:
            return func(self)
        finally:
            self.stop()

    async def _invokeAsync(self, func: Callable[..., object]) -> object:
        self.init()
        try:
            result = func(self)
            if inspect.isawaitable(result):
                return await result
            return result
        finally:
            self.stop()
