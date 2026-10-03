from contextvars import ContextVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from coffee.core.runtime.CoffeeApplicationRuntime import (
        CoffeeApplicationRuntime,
    )

_current_app: ContextVar["CoffeeApplicationRuntime | None"] = ContextVar(
    "coffee_current_app",
    default=None,
)

class CoffeeApplicationContext:
    @staticmethod
    def setApp(app: "CoffeeApplicationRuntime"):
        return _current_app.set(app)

    @staticmethod
    def getApp() -> "CoffeeApplicationRuntime":
        app = _current_app.get()

        if app is None:
            raise RuntimeError(
                "CoffeeApplicationRuntime is not running"
            )

        return app

    @staticmethod
    def resetApp(token) -> None:
        _current_app.reset(token)
