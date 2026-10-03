import os
import platform
from dataclasses import dataclass
from coffee.config.Config import Config
import subprocess
import sys
from pathlib import Path

@dataclass
class tool:
    @staticmethod
    def clear_screen():
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    async def verify_modules():
        try:
            runner = Path(".venv") / ("Scripts/python.exe" if sys.platform == "win32" else "bin/python")

            if not os.path.exists(".venv"):
                subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)

            req_path = os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__), "requirements", "requirements.txt"
                )
            )
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", req_path], check=True
            )
        except Exception as E:
            print(f"Erro Na Verificacao De Modulos, Erro: {E}")
            return

    @staticmethod
    async def add_path_modules(config_local: Config):
        if config_local.modules_local is None:
            return
        try:
            for i in config_local.modules_local:
                sys.path.append(
                    os.path.abspath(os.path.join(os.path.dirname(__file__), i))
                )
                if config_local.Debug:
                    print(f"Module_local: {i}")
            return
        except Exception as E:
            print(f"Erro Al Adicionar Os Caminhos Brutos, Erro: {E}")
            return
