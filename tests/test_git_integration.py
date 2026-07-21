from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from git_tools import GitTools


def run(*args: str, cwd: Path) -> str:
    result = subprocess.run(
        list(args), cwd=cwd, capture_output=True, text=True, check=True
    )
    return result.stdout.strip()


class GitIntegrationTest(unittest.TestCase):
    def _repositories(self, root: Path) -> tuple[Path, Path, Path]:
        remote = root / "remote.git"
        run("git", "init", "--bare", str(remote), cwd=root)
        first = root / "first"
        run("git", "clone", str(remote), str(first), cwd=root)
        run("git", "switch", "-c", "main", cwd=first)
        run("git", "config", "user.name", "Bot Test", cwd=first)
        run("git", "config", "user.email", "bot@example.invalid", cwd=first)
        (first / "arquivo.txt").write_text("inicial\n", encoding="utf-8")
        run("git", "add", "arquivo.txt", cwd=first)
        run("git", "commit", "-m", "inicial", cwd=first)
        run("git", "push", "-u", "origin", "main", cwd=first)

        second = root / "second"
        run("git", "clone", "--branch", "main", str(remote), str(second), cwd=root)
        run("git", "config", "user.name", "Bot Test", cwd=second)
        run("git", "config", "user.email", "bot@example.invalid", cwd=second)
        return remote, first, second

    def test_clean_repository_behind_remote_can_fast_forward_only(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, first, second = self._repositories(root)
            (second / "remoto.txt").write_text("novo\n", encoding="utf-8")
            run("git", "add", "remoto.txt", cwd=second)
            run("git", "commit", "-m", "remoto", cwd=second)
            run("git", "push", cwd=second)

            git = GitTools(first)
            self.assertTrue(git.fetch()[0])
            self.assertEqual("1", git.get_branch_status()["behind"])
            ok, _ = git.pull()

            self.assertTrue(ok)
            self.assertEqual("0", git.get_branch_status()["behind"])
            self.assertTrue((first / "remoto.txt").exists())

    def test_local_changes_are_listed_without_being_discarded(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, first, _ = self._repositories(root)
            original = first / "arquivo.txt"
            original.write_text("alteração local\n", encoding="utf-8")

            files = GitTools(first).get_changed_files()

            self.assertEqual("arquivo.txt", files[0]["path"])
            self.assertEqual("alteração local\n", original.read_text(encoding="utf-8"))

    def test_selected_stage_does_not_add_other_files(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, first, _ = self._repositories(root)
            (first / "um.txt").write_text("um", encoding="utf-8")
            (first / "dois.txt").write_text("dois", encoding="utf-8")

            ok, _ = GitTools(first).stage_files(["um.txt"])

            self.assertTrue(ok)
            staged = run("git", "diff", "--cached", "--name-only", cwd=first)
            self.assertEqual("um.txt", staged)

    def test_repository_without_upstream_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            run("git", "init", "-b", "main", cwd=repo)
            git = GitTools(repo)

            self.assertEqual("", git.get_upstream())
            self.assertEqual("?", git.get_branch_status()["behind"])

    def test_unmerged_files_are_detected_as_conflicts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            _, first, second = self._repositories(root)
            (first / "arquivo.txt").write_text("local\n", encoding="utf-8")
            run("git", "add", "arquivo.txt", cwd=first)
            run("git", "commit", "-m", "local", cwd=first)
            (second / "arquivo.txt").write_text("remoto\n", encoding="utf-8")
            run("git", "add", "arquivo.txt", cwd=second)
            run("git", "commit", "-m", "remoto", cwd=second)
            run("git", "push", cwd=second)
            run("git", "fetch", cwd=first)
            subprocess.run(
                ["git", "merge", "origin/main"],
                cwd=first,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertTrue(GitTools(first).has_conflicts())

    def test_windows_git_process_uses_schannel(self) -> None:
        completed = subprocess.CompletedProcess([], 1, "", "falha SSL")
        with patch("git_tools.subprocess.run", return_value=completed) as mocked:
            ok, output = GitTools(Path("C:/repo")).fetch()

        environment = mocked.call_args.kwargs["env"]
        if sys.platform == "win32":
            self.assertEqual("schannel", environment.get("GIT_SSL_BACKEND"))
        self.assertNotIn("GIT_SSL_NO_VERIFY", environment)
        self.assertFalse(ok)
        self.assertEqual("falha SSL", output)


if __name__ == "__main__":
    unittest.main()
