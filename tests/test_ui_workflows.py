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
        self.commit_calls = 0
        self.has_changes = False

    def get_caminho(self, pasta):
        return Path(pasta)

    def is_git_repo(self, pasta):
        return True

    def get_current_branch(self, pasta):
        return "main"

    def get_branch_status(self, pasta):
        return {"ahead": "0", "behind": "0"}

    def fetch(self, pasta):
        self.fetch_calls += 1
        return True, "ok"

    def has_uncommitted_changes(self, pasta):
        return self.has_changes

    def pull(self, pasta, branch):
        return True, "ok"

    def push(self, pasta, branch):
        self.push_calls += 1
        return True, "ok"

    def stage_all(self, pasta):
        self.stage_calls += 1
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

        self.assertEqual(1, git.fetch_calls)
        self.assertEqual(1, git.push_calls)
        self.assertEqual(1, vscode.open_calls)
        self.assertEqual(1, vscode.close_calls)
        self.assertEqual(2, len(history.entries))
        self.assertIn("Atividade encerrada", messages[-1])

    def test_end_with_changes_confirms_commit_and_push(self) -> None:
        git = FakeGitService()
        git.has_changes = True
        vscode = FakeVSCodeService()
        history = FakeHistoricoService()
        inicio = InicioPage(git, vscode, history, object(), "AUTO")
        inicio.definir_on_mensagem(lambda message: None)
        inicio.construir()
        inicio.definir_projeto(Projeto("Teste", ".", "main", "Python"))
        page = FakePage()

        inicio.encerrar_atividade(SimpleNamespace(page=page))
        self.assertEqual(1, len(page.dialogs))

        inicio._confirmar_commit(SimpleNamespace(page=page))
        inicio._commit_field.value = "Teste automatizado"
        inicio._executar_commit(SimpleNamespace(page=page))

        self.assertEqual(1, git.stage_calls)
        self.assertEqual(1, git.commit_calls)
        self.assertEqual(1, git.push_calls)
        self.assertEqual(1, len(history.entries))


if __name__ == "__main__":
    unittest.main()
