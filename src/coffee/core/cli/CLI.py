import argparse
from coffee.core.runtime.componets.Componet import Component
from coffee.core.Services.module.ModuleManager import ModuleManager
from coffee.core.data.Config import Config


@Component
class RuntimeCLI:
    parser: argparse.ArgumentParser

    def __init__(self, moduleManager: ModuleManager, config: Config):
        self.moduleManager = moduleManager
        self.config = config

    def buildParser(self) -> argparse.ArgumentParser:
        self.parser = argparse.ArgumentParser(
            prog="coffee", description="Coffee CLI", add_help=True
        )
        return self.parser

    def _addSubparsers(self) -> None:
        for module in self.moduleManager.loadModules():
            pass
