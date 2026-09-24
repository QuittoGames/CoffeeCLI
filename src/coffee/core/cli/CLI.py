import argparse
from coffee.core.runtime.componets.Componet import Component
from core.runtime.CoffeAplicationRuntime import CoffeeApplicationRuntime
from core.Services.module.ModuleManager import ModuleManager
from core.data.Config import Config

@Component
class RuntimeCLI(Component):
    parser: argparse.ArgumentParser

    def __init__(self,moduleManager: ModuleManager,config: Config):
        self.moduleManager = moduleManager
        self.config = config

    def buildParser(self) -> argparse.ArgumentParser:
        self.parser = argparse.ArgumentParser(
            prog="coffee",
            description="Coffee CLI",
            add_help=True
        )

    def _addSubparsers(self) -> None:
        for module in self.moduleManager.loadModules():
            pass
