from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import flet as ft

from config import Config
from projetos import ProjetosManager
from ui.app import BotVSCode2App

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "config.json"
PROJETOS_FILE = CONFIG_DIR / "projetos.json"


def main() -> None:
    config = Config.load(CONFIG_FILE)
    projetos_manager = ProjetosManager(PROJETOS_FILE)

    app = BotVSCode2App(config, projetos_manager)
    ft.run(main=app.run)


if __name__ == "__main__":
    main()
