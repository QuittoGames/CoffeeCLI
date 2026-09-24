from dataclasses import dataclass
from core.domain.interface.Module import ModuleRegistry
from core.runtime.componets.ModulePackage import Module

@dataclass
@Module
class SSHModule(Module):
    id = "ssh_module"
    name = "SSH Module"
    version = "0.1v"
