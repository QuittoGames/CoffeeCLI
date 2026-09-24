from dataclasses import dataclass,field
from pathlib import Path
from Host import Host
import os
from platformdirs import user_config_dir, user_data_dir, user_cache_dir

@dataclass
class Config:
    configPath:Path = Path(user_config_dir("Coffee"))

    hostData:Host = field(default_factory=Host)

    Debug:bool = False

    def build(self) -> None:
        if not (self.configPath.exists() and os.path.isdir()):
            raise RuntimeError()

        if not self.hostData.platform == None:
            raise RuntimeError()
