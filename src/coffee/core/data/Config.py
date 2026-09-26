from dataclasses import dataclass, field
from pathlib import Path
from coffee.core.data.Host import Host
import os
from platformdirs import user_config_dir


@dataclass
class Config:
    configPath: Path = Path(user_config_dir("Coffee"))

    hostData: Host = field(default_factory=Host)

    Debug: bool = False

    modules_local: list[str] | None = None

    def build(self) -> Config:
        if not (self.configPath.exists() and os.path.isdir(self.configPath.absolute())):
            raise RuntimeError()

        if not self.hostData.platform == None:
            raise RuntimeError()

        return self
