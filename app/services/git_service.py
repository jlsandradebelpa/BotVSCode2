from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from git_tools import GitTools
from utils import resolve_full_path


class GitService:
    def __init__(self, workspace_drive: str) -> None:
        self._workspace_drive = workspace_drive

    def _get_git(self, pasta: str) -> Optional[GitTools]:
        try:
            caminho = resolve_full_path(self._workspace_drive, pasta)
            if not caminho.exists():
                return None
            return GitTools(caminho)
        except Exception:
            return None

    def get_caminho(self, pasta: str) -> Optional[Path]:
        try:
            caminho = resolve_full_path(self._workspace_drive, pasta)
            if caminho.exists():
                return caminho
            return None
        except Exception:
            return None

    def is_git_repo(self, pasta: str) -> bool:
        git = self._get_git(pasta)
        return git is not None and git.is_git_repo()

    def get_current_branch(self, pasta: str) -> str:
        git = self._get_git(pasta)
        if git is None:
            return ""
        return git.get_current_branch()

    def fetch(self, pasta: str) -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.fetch()

    def has_uncommitted_changes(self, pasta: str) -> bool:
        git = self._get_git(pasta)
        if git is None:
            return False
        return git.has_uncommitted_changes()

    def status_short(self, pasta: str) -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.status_short()

    def get_changed_files(self, pasta: str) -> List[Dict[str, str]]:
        git = self._get_git(pasta)
        return git.get_changed_files() if git is not None else []

    def has_conflicts(self, pasta: str) -> bool:
        git = self._get_git(pasta)
        return git is not None and git.has_conflicts()

    def get_upstream(self, pasta: str) -> str:
        git = self._get_git(pasta)
        return git.get_upstream() if git is not None else ""

    def get_branch_status(self, pasta: str) -> Dict[str, str]:
        git = self._get_git(pasta)
        if git is None:
            return {"ahead": "?", "behind": "?"}
        return git.get_branch_status()

    def pull(self, pasta: str, branch: str = "") -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.pull(branch)

    def stage_files(self, pasta: str, paths: Sequence[str]) -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.stage_files(paths)

    def stage_all(self, pasta: str) -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.stage_all()

    def commit(self, pasta: str, message: str) -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.commit(message)

    def push(self, pasta: str, branch: str = "") -> Tuple[bool, str]:
        git = self._get_git(pasta)
        if git is None:
            return False, "Caminho não encontrado."
        return git.push(branch)
