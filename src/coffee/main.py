from coffee.config.Config import Config
from coffee.core.services.tool import tool
import asyncio
from coffee.core.runtime.CoffeeApplicationRuntime import CoffeeApplicationRuntime
from coffee.core.domain.exceptions.InvalidCoffeeApplicationException import (
    InvalidCoffeeApplicationException,
)

def Start():
    tool.clear_screen()
    print("coffe")

@CoffeeApplicationRuntime
async def main(app: CoffeeApplicationRuntime):
    try:
        contener = app.getContainer()
        if contener.config.Debug:
            asyncio.create_task(tool.verify_modules())

        if not (app or app.getContainer()):
            raise InvalidCoffeeApplicationException(
                "The application runtime or container is unavailable."
            )

    except (StopAsyncIteration, InvalidCoffeeApplicationException) as E:
        print(f"[ERROR] Erro StopAsyncIteration, Erro: {E}")


if __name__ == "__main__":
    asyncio.run(main())
    Start()
