from dataclasses import dataclass
from platform import system
import os


@dataclass
class Host:
    username: str = os.getlogin()
    platform: str = system()
