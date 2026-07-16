from __future__ import annotations

import sys
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from chat.command_context import CommandContext
from chat.command_executor import CommandExecutor
from projetos import Projeto


class FakeGit:
    def __init__(self) -> None:
        self.branch = "main"
        self.upstream = "origin/main"
        self.status = {"ahead": "0", "behind": "0", "upstream": "origin/main"}
        self.files = []
        self.pull_calls = 0
        self.push_calls = 0

    def is_git_repo(self, pasta): return True
    def fetch(self, pasta): return True, "ok"
    def get_current_branch(self, pasta): return self.branch
    def get_upstream(self, pasta): return self.upstream
    def has_conflicts(self, pasta): return False
    def get_branch_status(self, pasta): return dict(self.status)
    def get_changed_files(self, pasta): return list(self.files)
    def pull(self, pasta, branch):
        self.pull_calls += 1
        return True, "ok"
    def push(self, pasta, branch):
        self.push_calls += 1
        return True, "ok"


class FakeHistory:
    def registrar(self, tipo, descricao): pass


class ChatGitWorkflowTest(unittest.TestCase):
    def _executor(self, git: FakeGit) -> CommandExecutor:
        context = CommandContext()
        context.current_project = Projeto("Teste", ".", "main", "Python")
        return CommandExecutor(
            object(), git, object(), FakeHistory(), object(), context
        )

    def test_chat_blocks_push_on_wrong_branch(self) -> None:
        git = FakeGit()
        git.branch = "master"
        git.upstream = "origin/master"

        result = self._executor(git).encerrar_atividades("")

        self.assertIn("branch incorreta", result)
        self.assertEqual(0, git.push_calls)

    def test_chat_blocks_pull_when_local_files_exist(self) -> None:
        git = FakeGit()
        git.status["behind"] = "1"
        git.files = [{"status": " M", "path": "documento.md"}]

        result = self._executor(git).atualizar_documentacao_local("")

        self.assertIn("Pull bloqueado", result)
        self.assertEqual(0, git.pull_calls)

    def test_chat_uses_safe_pull_when_remote_is_ahead(self) -> None:
        git = FakeGit()
        git.status["behind"] = "1"

        result = self._executor(git).atualizar_documentacao_local("")

        self.assertIn("atualizada com sucesso", result)
        self.assertEqual(1, git.pull_calls)


if __name__ == "__main__":
    unittest.main()
