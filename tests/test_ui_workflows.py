from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from config import Config
from projetos import Projeto, ProjetosManager
from services.preferences_service import PreferencesService
from services.project_service import ProjectService
from ui.app import BotVSCode2App
from ui.paginas.inicio import InicioPage
from ui.paginas.projetos import ProjetosPage


class FakeWindow:
    maximized = False


class FakePage:
    def __init__(self) -> None:
        self.window = FakeWindow()
        self.controls = []
        self.dialogs = []

    def add(self, *controls) -> None:
        self.controls.extend(controls)

    def update(self) -> None:
        pass

    def show_dialog(self, dialog) -> None:
        self.dialogs.append(dialog)

    def pop_dialog(self) -> None:
        if self.dialogs:
            self.dialogs.pop()


class FakeGitService:
    def __init__(self) -> None:
        self.push_calls = 0
        self.fetch_calls = 0
        self.stage_calls = 0
        self.staged_paths = []
        self.commit_calls = 0
        self.current_branch = "main"
        self.upstream = "origin/main"
        self.branch_status = {"ahead": "0", "behind": "0", "upstream": "origin/main"}
        self.changed_files = []
        self.conflicts = False

    def get_caminho(self, pasta):
        return Path(pasta)

    def is_git_repo(self, pasta):
        return True

    def get_current_branch(self, pasta):
        return self.current_branch

    def get_upstream(self, pasta):
        return self.upstream

    def get_branch_status(self, pasta):
        return dict(self.branch_status)

    def fetch(self, pasta):
        self.fetch_calls += 1
        return True, "ok"

    def has_uncommitted_changes(self, pasta):
        return bool(self.changed_files)

    def get_changed_files(self, pasta):
        return list(self.changed_files)

    def has_conflicts(self, pasta):
        return self.conflicts

    def pull(self, pasta, branch):
        return True, "ok"

    def push(self, pasta, branch):
        self.push_calls += 1
        return True, "ok"

    def stage_all(self, pasta):
        self.stage_calls += 1
        return True, "ok"

    def stage_files(self, pasta, paths):
        self.stage_calls += 1
        self.staged_paths = list(paths)
        return True, "ok"

    def commit(self, pasta, message):
        self.commit_calls += 1
        return True, "ok"


class FakeVSCodeService:
    def __init__(self) -> None:
        self.open_calls = 0
        self.close_calls = 0

    def installed(self):
        return True

    def abrir(self, pasta):
        self.open_calls += 1
        return True

    def fechar(self, pasta):
        self.close_calls += 1
        return True


class FakeHistoricoService:
    def __init__(self) -> None:
        self.entries = []

    def listar(self):
        return []

    def registrar(self, tipo, descricao):
        self.entries.append((tipo, descricao))


class UiWorkflowTest(unittest.TestCase):
    def _manager(self, directory: str) -> ProjetosManager:
        path = Path(directory) / "projetos.json"
        path.write_text(json.dumps([
            {"nome": "Um", "pasta": directory, "branch": "main", "linguagem": "Python"},
            {"nome": "Dois", "pasta": directory, "branch": "main", "linguagem": "Python"},
        ]), encoding="utf-8")
        return ProjetosManager(path)

    def test_application_starts_maximized_without_default_project(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manager = self._manager(directory)
            preferences = PreferencesService(Path(directory) / "preferences.json")
            app = BotVSCode2App(
                Config("AUTO", "Teste", "Teste"), manager, preferences
            )
            page = FakePage()

            app.run(page)

            self.assertTrue(page.window.maximized)
            self.assertIsNone(app._projeto_atual)
            self.assertEqual(1, len(page.controls))

    def test_project_is_only_confirmed_by_select_button(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = ProjetosPage(ProjectService(self._manager(directory)))
            selected = []
            page.definir_on_projeto_selecionado(selected.append)
            page.construir()
            self.assertEqual("always", page._lista_container.scroll.value)

            page._selecionar(1)
            self.assertEqual([], selected)

            page._ao_selecionar(SimpleNamespace())
            self.assertEqual("Dois", selected[-1].nome)

    def test_start_and_end_success_paths(self) -> None:
        git = FakeGitService()
        vscode = FakeVSCodeService()
        history = FakeHistoricoService()
        inicio = InicioPage(git, vscode, history, object(), "AUTO")
        messages = []
        inicio.definir_on_mensagem(messages.append)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))
        event = SimpleNamespace(page=FakePage())

        inicio.iniciar_atividade(event)
        inicio.encerrar_atividade(event)

        self.assertEqual(2, git.fetch_calls)
        self.assertEqual(0, git.push_calls)
        self.assertEqual(1, vscode.open_calls)
        self.assertEqual(1, vscode.close_calls)
        self.assertEqual(2, len(history.entries))
        self.assertIn("Atividade encerrada", messages[-1])

    def test_end_with_changes_confirms_commit_and_push(self) -> None:
        git = FakeGitService()
        git.changed_files = [{"status": " M", "path": "app/main.py"}]
        vscode = FakeVSCodeService()
        history = FakeHistoricoService()
        inicio = InicioPage(git, vscode, history, object(), "AUTO")
        inicio.definir_on_mensagem(lambda message: None)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))
        page = FakePage()

        inicio.encerrar_atividade(SimpleNamespace(page=page))
        self.assertEqual(1, len(page.dialogs))

        inicio._file_checkboxes[0].value = True
        inicio._confirmar_selecao(SimpleNamespace(page=page))
        inicio._commit_field.value = "Teste automatizado"
        inicio._executar_commit(SimpleNamespace(page=page))

        self.assertEqual(1, git.stage_calls)
        self.assertEqual(["app/main.py"], git.staged_paths)
        self.assertEqual(1, git.commit_calls)
        self.assertEqual(1, git.push_calls)
        self.assertEqual(2, git.fetch_calls)
        self.assertEqual(1, len(history.entries))

    def test_start_pulls_with_ff_only_when_remote_is_ahead(self) -> None:
        git = FakeGitService()
        git.branch_status = {"ahead": "0", "behind": "2", "upstream": "origin/main"}
        vscode = FakeVSCodeService()
        inicio = InicioPage(git, vscode, FakeHistoricoService(), object(), "AUTO")
        messages = []
        inicio.definir_on_mensagem(messages.append)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))

        inicio.iniciar_atividade(SimpleNamespace(page=FakePage()))

        self.assertEqual(1, vscode.open_calls)
        self.assertIn("Atividade iniciada", messages[-1])

    def test_start_blocks_wrong_branch_and_shows_context(self) -> None:
        git = FakeGitService()
        git.current_branch = "master"
        git.upstream = "origin/master"
        inicio = InicioPage(git, FakeVSCodeService(), FakeHistoricoService(), object(), "AUTO")
        messages = []
        inicio.definir_on_mensagem(messages.append)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))

        inicio.iniciar_atividade(SimpleNamespace(page=FakePage()))

        self.assertIn("branch incorreta", messages[-1])
        self.assertIn("Configurada: main", messages[-1])
        self.assertIn("Atual: master", messages[-1])

    def test_start_blocks_missing_upstream(self) -> None:
        git = FakeGitService()
        git.upstream = ""
        inicio = InicioPage(git, FakeVSCodeService(), FakeHistoricoService(), object(), "AUTO")
        messages = []
        inicio.definir_on_mensagem(messages.append)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))

        inicio.iniciar_atividade(SimpleNamespace(page=FakePage()))

        self.assertIn("sem upstream", messages[-1])

    def test_start_with_local_changes_requires_explicit_decision(self) -> None:
        git = FakeGitService()
        git.changed_files = [{"status": " M", "path": "arquivo.py"}]
        vscode = FakeVSCodeService()
        inicio = InicioPage(git, vscode, FakeHistoricoService(), object(), "AUTO")
        inicio.definir_on_mensagem(lambda message: None)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))
        page = FakePage()

        inicio.iniciar_atividade(SimpleNamespace(page=page))

        self.assertEqual(1, len(page.dialogs))
        self.assertEqual(0, vscode.open_calls)
        inicio._confirmar_abertura_sem_pull(SimpleNamespace(page=page), inicio._projeto_atual)
        self.assertEqual(1, vscode.open_calls)

    def test_divergent_branch_is_blocked(self) -> None:
        git = FakeGitService()
        git.branch_status = {"ahead": "1", "behind": "1", "upstream": "origin/main"}
        inicio = InicioPage(git, FakeVSCodeService(), FakeHistoricoService(), object(), "AUTO")
        messages = []
        inicio.definir_on_mensagem(messages.append)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))

        inicio.iniciar_atividade(SimpleNamespace(page=FakePage()))

        self.assertIn("branch divergente", messages[-1])

    def test_end_blocks_when_remote_advanced(self) -> None:
        git = FakeGitService()
        git.branch_status = {"ahead": "0", "behind": "1", "upstream": "origin/main"}
        inicio = InicioPage(git, FakeVSCodeService(), FakeHistoricoService(), object(), "AUTO")
        messages = []
        inicio.definir_on_mensagem(messages.append)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))

        inicio.encerrar_atividade(SimpleNamespace(page=FakePage()))

        self.assertIn("remoto avançou", messages[-1])
        self.assertEqual(0, git.push_calls)


if __name__ == "__main__":
    unittest.main()
