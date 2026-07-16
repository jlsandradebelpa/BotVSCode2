from __future__ import annotations

import json
import os
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional


class DataMigrationError(RuntimeError):
    """Raised when personal data cannot be migrated safely."""


@dataclass(frozen=True)
class AppDataPaths:
    root: Path
    projects: Path
    preferences: Path
    state: Path
    logs_dir: Path
    backup_dir: Path
    sessions_dir: Path

    @classmethod
    def discover(cls) -> "AppDataPaths":
        override = os.environ.get("BOTVSCODE2_DATA_DIR")
        if override:
            root = Path(override).expanduser()
        else:
            appdata = os.environ.get("APPDATA")
            root = (
                Path(appdata) / "BotVsCode2"
                if appdata
                else Path.home() / "AppData" / "Roaming" / "BotVsCode2"
            )
        return cls(
            root=root,
            projects=root / "projetos.json",
            preferences=root / "preferences.json",
            state=root / "state.json",
            logs_dir=root / "logs",
            backup_dir=root / "backup",
            sessions_dir=root / "sessions",
        )

    def ensure_directories(self) -> None:
        for directory in (
            self.root,
            self.logs_dir,
            self.backup_dir,
            self.sessions_dir,
        ):
            directory.mkdir(parents=True, exist_ok=True)


def _validate_json(path: Path) -> None:
    with path.open(encoding="utf-8") as file:
        json.load(file)


def _timestamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S-%f")


def _initialize_personal_file(
    *, legacy: Path, default: Path, target: Path, backup_dir: Path
) -> Optional[Path]:
    if target.exists():
        _validate_json(target)
        return None

    source = legacy if legacy.exists() else default
    if not source.exists():
        raise DataMigrationError(f"Arquivo de configuração não encontrado: {source}")

    backup: Optional[Path] = None
    temporary = target.with_suffix(f"{target.suffix}.tmp")
    try:
        _validate_json(source)
        if legacy.exists():
            backup = backup_dir / f"{legacy.stem}-{_timestamp()}{legacy.suffix}"
            shutil.copy2(legacy, backup)
            _validate_json(backup)

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, temporary)
        _validate_json(temporary)
        temporary.replace(target)
        _validate_json(target)
        return backup
    except Exception as exc:
        temporary.unlink(missing_ok=True)
        target.unlink(missing_ok=True)
        raise DataMigrationError(
            f"Migração cancelada para {target.name}. O arquivo original foi preservado: {exc}"
        ) from exc


def _copy_legacy_history(source: Optional[Path], target: Path) -> list[Path]:
    if source is None or not source.exists() or source.resolve() == target.resolve():
        return []

    copied: list[Path] = []
    for item in source.glob("historico_atividades_*.txt"):
        destination = target / item.name
        if not destination.exists():
            shutil.copy2(item, destination)
            copied.append(destination)
    return copied


@dataclass(frozen=True)
class MigrationReport:
    paths: AppDataPaths
    project_backup: Optional[Path]
    preferences_backup: Optional[Path]
    history_files_copied: int


def prepare_user_data(
    config_dir: Path, legacy_history_dir: Optional[Path] = None
) -> MigrationReport:
    paths = AppDataPaths.discover()
    projects_existed = paths.projects.exists()
    preferences_existed = paths.preferences.exists()
    copied_history: list[Path] = []
    try:
        paths.ensure_directories()
        project_backup = _initialize_personal_file(
            legacy=config_dir / "projetos.json",
            default=config_dir / "projetos.default.json",
            target=paths.projects,
            backup_dir=paths.backup_dir,
        )
        preferences_backup = _initialize_personal_file(
            legacy=config_dir / "preferences.json",
            default=config_dir / "preferences.default.json",
            target=paths.preferences,
            backup_dir=paths.backup_dir,
        )
        copied_history = _copy_legacy_history(legacy_history_dir, paths.sessions_dir)
    except DataMigrationError:
        if not projects_existed:
            paths.projects.unlink(missing_ok=True)
        if not preferences_existed:
            paths.preferences.unlink(missing_ok=True)
        for item in copied_history:
            item.unlink(missing_ok=True)
        raise
    except Exception as exc:
        if not projects_existed:
            paths.projects.unlink(missing_ok=True)
        if not preferences_existed:
            paths.preferences.unlink(missing_ok=True)
        for item in copied_history:
            item.unlink(missing_ok=True)
        raise DataMigrationError(
            f"Não foi possível preparar os dados pessoais. Nenhum arquivo original foi apagado: {exc}"
        ) from exc

    return MigrationReport(
        paths=paths,
        project_backup=project_backup,
        preferences_backup=preferences_backup,
        history_files_copied=len(copied_history),
    )
