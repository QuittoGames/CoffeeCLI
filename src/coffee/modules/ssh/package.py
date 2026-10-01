from coffee.core.components.decorators.Module import Module
from coffee.core.domain.interface.SystemModule import SystemModule


@Module
class SSHModule(SystemModule):

    @property
    def id(self) -> str:
        return "ssh_module"

    @property
    def name(self) -> str:
        return getattr(self, "_name", "SSH Module")

    @name.setter
    def name(self, value: str) -> None:
        self._name = value

    @property
    def version(self) -> str:
        return "0.1v"

    @version.setter
    def version(self, value: str) -> None:
        self._version = value
