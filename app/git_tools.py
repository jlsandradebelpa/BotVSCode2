from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Dict, Tuple


class GitTools:
    def __init__(self, repo_path: Path) -> None:
        self._repo = repo_path

    def is_git_repo(self) -> bool:
        result = self._run("rev-parse --git-dir", check=False)
        return result.returncode == 0

    def get_current_branch(self) -> str:
        result = self._run("rev-parse --abbrev-ref HEAD", check=False)
        return result.stdout.strip() if result.returncode == 0 else ""

    def fetch(self) -> Tuple[bool, str]:
        return self._run_cmd("fetch --all --prune")

    def has_uncommitted_changes(self) -> bool:
        result = self._run("status --porcelain", check=False)
        return len(result.stdout.strip()) > 0

    def status_short(self) -> Tuple[bool, str]:
        return self._run_cmd("status --short")

    def status_full(self) -> Tuple[bool, str]:
        return self._run_cmd("status")

    def get_branch_status(self) -> Dict[str, str]:
        result = self._run(
            "rev-list --left-right --count HEAD...@{upstream}",
            check=False,
        )
        if result.returncode != 0:
            return {"ahead": "?", "behind": "?"}

        parts = result.stdout.strip().split()
        if len(parts) == 2:
            return {"ahead": parts[0], "behind": parts[1]}
        return {"ahead": "0", "behind": "0"}

    def pull(self, branch: str = "") -> Tuple[bool, str]:
        if not branch:
            branch = self.get_current_branch()
        if not branch:
            return False, "Nao foi possivel determinar a branch atual."
        return self._run_cmd(f"pull origin {branch}")

    def stage_all(self) -> Tuple[bool, str]:
        return self._run_cmd("add -A")

    def commit(self, message: str) -> Tuple[bool, str]:
        escaped = message.replace('"', '\\"')
        return self._run_cmd(f'commit -m "{escaped}"')

    def push(self, branch: str = "") -> Tuple[bool, str]:
        if not branch:
            branch = self.get_current_branch()
        if not branch:
            return False, "Nao foi possivel determinar a branch atual."
        return self._run_cmd(f"push origin {branch}")

    def shortlog(self, count: int = 5) -> Tuple[bool, str]:
        return self._run_cmd(f"log --oneline -{count}")

    def _run(
        self, cmd: str, check: bool = True
    ) -> subprocess.CompletedProcess:
        full_cmd = f"git -C \"{self._repo}\" {cmd}"
        return subprocess.run(
            full_cmd,
            capture_output=True,
            text=True,
            shell=True,
            check=check,
        )

    def _run_cmd(self, cmd: str) -> Tuple[bool, str]:
        try:
            result = self._run(cmd, check=False)
            success = result.returncode == 0
            output = (result.stdout or result.stderr).strip()
            return success, output
        except FileNotFoundError:
            return False, "Git nao encontrado. Verifique se o Git esta instalado."
        except Exception as e:
            return False, f"Erro inesperado: {e}"
