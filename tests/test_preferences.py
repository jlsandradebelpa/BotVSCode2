from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from preferences import Preferences
from services.preferences_service import PreferencesService


class PreferencesTest(unittest.TestCase):
    def test_defaults_are_created_and_can_be_persisted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "preferences.json"
            service = PreferencesService(path)

            self.assertEqual("dark", service.preferences.theme_mode)
            self.assertTrue(path.exists())

            service.salvar("light", "teal", "Consolas")
            loaded = Preferences.load(path)

            self.assertEqual("light", loaded.theme_mode)
            self.assertEqual("teal", loaded.color_seed)
            self.assertEqual("Consolas", loaded.font_family)

    def test_restore_returns_defaults(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            service = PreferencesService(Path(directory) / "preferences.json")
            service.salvar("light", "purple", "Arial")

            restored = service.restaurar()

            self.assertEqual(Preferences(), restored)


if __name__ == "__main__":
    unittest.main()
