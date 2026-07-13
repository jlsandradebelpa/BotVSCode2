from __future__ import annotations

from pathlib import Path
from typing import Optional

from vscode import is_vscode_installed, open_vscode, close_vscode
from utils import resolve_full_path


class VSCodeService:
    def __init__(self, workspace_drive: str) -> None:
        self._workspace_drive = workspace_drive

    def installed(self) -> bool:
        return is_vscode_installed()

    def abrir(self, pasta: str) -> bool:
        try:
            caminho = resolve_full_path(self._workspace_drive, pasta)
            if not caminho.exists():
                return False
            return open_vscode(caminho)
        except Exception:
            return False

    def fechar(self, pasta: str) -> bool:
        try:
            caminho = resolve_full_path(self._workspace_drive, pasta)
            return close_vscode(caminho)
        except Exception:
            return False