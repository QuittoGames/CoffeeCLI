import argparse
from core.runtime.componets.Componets import Component

@Component
class RuntimeCLI:
    parser: argparse.ArgumentParser

    def buildParser(self) -> argparse.ArgumentParser:
        self.parser = argparse.ArgumentParser(
            prog="coffee",
            description="Coffee CLI",
            add_help=True
        )
