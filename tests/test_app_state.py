from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from app_state import AppState


class AppStateTest(unittest.TestCase):
    def test_selected_project_is_persisted_outside_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            AppState(selected_project="BotVsCode2").save(path)

            loaded = AppState.load(path)

            self.assertEqual("BotVsCode2", loaded.selected_project)

    def test_invalid_state_does_not_prevent_startup(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "state.json"
            path.write_text("inválido", encoding="utf-8")

            self.assertEqual(AppState(), AppState.load(path))


if __name__ == "__main__":
    unittest.main()
