from ..data.data import data
from tool import tool
import asyncio
from core.runtime.CoffeAplicationRuntime import CoffeeApplicationRuntime
from core.domain.exepiton.InvalidCoffeeAplicationException import InvalidCoffeeApplicationException

data_local = data()


def Start():
    tool.menu()

@CoffeeApplicationRuntime
async def main(app: CoffeeApplicationRuntime):
    try:
        if data_local.Debug:
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
