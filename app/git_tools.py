from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Dict, List, Sequence, Tuple


class GitTools:
    def __init__(self, repo_path: Path) -> None:
        self._repo = repo_path

    def is_git_repo(self) -> bool:
        result = self._run("rev-parse", "--git-dir", check=False)
        return result.returncode == 0

    def get_current_branch(self) -> str:
        result = self._run("rev-parse", "--abbrev-ref", "HEAD", check=False)
        return result.stdout.strip() if result.returncode == 0 else ""

    def fetch(self) -> Tuple[bool, str]:
        return self._run_cmd("fetch", "--all", "--prune")

    def has_uncommitted_changes(self) -> bool:
        result = self._run("status", "--porcelain", check=False)
        return len(result.stdout.strip()) > 0

    def status_short(self) -> Tuple[bool, str]:
        return self._run_cmd("status", "--short")

    def status_full(self) -> Tuple[bool, str]:
        return self._run_cmd("status")

    def get_changed_files(self) -> List[Dict[str, str]]:
        result = self._run("status", "--porcelain=v1", "-z", check=False)
        if result.returncode != 0:
            return []

        records = result.stdout.split("\0")
        files: List[Dict[str, str]] = []
        index = 0
        while index < len(records):
            record = records[index]
            index += 1
            if not record:
                continue
            status = record[:2]
            path = record[3:]
            if status[0] in ("R", "C") and index < len(records):
                novo_caminho = records[index]
                index += 1
                files.append({"status": status, "path": novo_caminho, "original": path})
            else:
                files.append({"status": status, "path": path})
        return files

    def has_conflicts(self) -> bool:
        conflict_codes = {"DD", "AU", "UD", "UA", "DU", "AA", "UU"}
        return any(
            item["status"] in conflict_codes
            for item in self.get_changed_files()
        )

    def get_upstream(self) -> str:
        result = self._run(
            "rev-parse",
            "--abbrev-ref",
            "--symbolic-full-name",
            "@{upstream}",
            check=False,
        )
        return result.stdout.strip() if result.returncode == 0 else ""

    def get_branch_status(self) -> Dict[str, str]:
        upstream = self.get_upstream()
        if not upstream:
            return {"ahead": "?", "behind": "?", "upstream": ""}
        result = self._run(
            "rev-list", "--left-right", "--count", "HEAD...@{upstream}", check=False
        )
        if result.returncode != 0:
            return {"ahead": "?", "behind": "?", "upstream": upstream}

        parts = result.stdout.strip().split()
        if len(parts) == 2:
            return {"ahead": parts[0], "behind": parts[1], "upstream": upstream}
        return {"ahead": "0", "behind": "0", "upstream": upstream}

    def pull(self, branch: str = "") -> Tuple[bool, str]:
        if not branch:
            branch = self.get_current_branch()
        if not branch:
            return False, "Nao foi possivel determinar a branch atual."
        upstream = self.get_upstream()
        if not upstream:
            return False, "Nao foi possivel determinar o upstream."
        remote = upstream.split("/", 1)[0]
        return self._run_cmd("pull", "--ff-only", remote, branch)

    def stage_files(self, paths: Sequence[str]) -> Tuple[bool, str]:
        clean_paths = [path for path in paths if path]
        if not clean_paths:
            return False, "Nenhum arquivo foi selecionado."
        return self._run_cmd("add", "--", *clean_paths)

    def stage_all(self) -> Tuple[bool, str]:
        return self._run_cmd("add", "-A")

    def commit(self, message: str) -> Tuple[bool, str]:
        return self._run_cmd("commit", "-m", message)

    def push(self, branch: str = "") -> Tuple[bool, str]:
        if not branch:
            branch = self.get_current_branch()
        if not branch:
            return False, "Nao foi possivel determinar a branch atual."
        upstream = self.get_upstream()
        if not upstream:
            return False, "Nao foi possivel determinar o upstream."
        remote = upstream.split("/", 1)[0]
        return self._run_cmd("push", remote, branch)

    def shortlog(self, count: int = 5) -> Tuple[bool, str]:
        return self._run_cmd("log", "--oneline", f"-{count}")

    def _run(
        self, *args: str, check: bool = True
    ) -> subprocess.CompletedProcess:
        environment = os.environ.copy()
        kwargs = {}
        if os.name == "nt":
            environment["GIT_SSL_BACKEND"] = "schannel"
            kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
        return subprocess.run(
            ["git", "-C", str(self._repo), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=environment,
            check=check,
            **kwargs,
        )

    def _run_cmd(self, *args: str) -> Tuple[bool, str]:
        try:
            result = self._run(*args, check=False)
            success = result.returncode == 0
            output = (result.stdout or result.stderr).strip()
            return success, output
        except FileNotFoundError:
            return False, "Git nao encontrado. Verifique se o Git esta instalado."
        except Exception as e:
            return False, f"Erro inesperado: {e}"
