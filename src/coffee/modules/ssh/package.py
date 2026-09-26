from dataclasses import dataclass
from coffee.core.runtime.componets.ModulePackage import Module


@dataclass
@Module
class SSHModule:
    id = "ssh_module"
    name = "SSH Module"
    version = "0.1v"
