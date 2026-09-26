from coffee.core.data.Config import Config
from coffee.core.Services.tool import tool
import asyncio
from coffee.core.runtime.CoffeAplicationRuntime import CoffeeApplicationRuntime
from coffee.core.domain.exepiton.InvalidCoffeeAplicationException import (
    InvalidCoffeeApplicationException,
)

config_local = Config()


def Start():
    tool.menu()


@CoffeeApplicationRuntime
async def main(app: CoffeeApplicationRuntime):
    try:
        if config_local.Debug:
            tool.verify_modules()

        if not (app or app.getContainer()):
            raise InvalidCoffeeApplicationException(
                "The application runtime or container is unavailable."
            )

    except (StopAsyncIteration, InvalidCoffeeApplicationException) as E:
        print(f"[ERROR] Erro StopAsycnInteration, Erro: {E}")


if __name__ == "__main__":
    asyncio.run(main())
    Start()
