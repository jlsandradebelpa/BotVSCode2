from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import flet as ft

from config import Config
from data_paths import DataMigrationError, prepare_user_data
from services.preferences_service import PreferencesService
from projetos import ProjetosManager
from ui.app import BotVSCode2App

CONFIG_DIR = Path(__file__).resolve().parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "config.json"


def main() -> None:
    config = Config.load(CONFIG_FILE)
    legacy_history = Path(config.historico_pasta) if config.historico_pasta else None
    try:
        migration = prepare_user_data(CONFIG_DIR, legacy_history)
    except DataMigrationError as exc:
        raise SystemExit(f"ERRO: {exc}") from exc

    projetos_manager = ProjetosManager(migration.paths.projects)
    preferences_service = PreferencesService(migration.paths.preferences)

    app = BotVSCode2App(
        config,
        projetos_manager,
        preferences_service,
        data_paths=migration.paths,
    )
    ft.run(main=app.run)


if __name__ == "__main__":
    main()
