from dataclasses import dataclass, field
from pathlib import Path
from time import sleep
from coffee.data.Host import Host
import os
from platformdirs import user_config_dir

@dataclass
class Config:
    configPath: Path = Path(user_config_dir("Coffee"))

    hostData: Host = field(default_factory=Host)

    Debug: bool = False

    modules_local: list[str] | None = None

    def build(self) -> Config:
        if not (self.configPath.exists()):
            os.makedirs(self.configPath, exist_ok=True)

        if not os.path.isdir(self.configPath.absolute()):
            raise RuntimeError("The configuration path is not a directory.")

        if not self.hostData.platform == None:
            self.getHost()

        return self

    def getHost(self) -> Host:
        self.hostData = Host()
        return self.hostData
