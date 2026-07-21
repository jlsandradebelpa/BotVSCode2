from __future__ import annotations

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

from data_paths import DataMigrationError, prepare_user_data


class DataPathsTest(unittest.TestCase):
    def _config_dir(self, root: Path) -> Path:
        config = root / "config"
        config.mkdir()
        (config / "projetos.default.json").write_text(
            '[{"nome": "Padrão"}]', encoding="utf-8"
        )
        (config / "preferences.default.json").write_text(
            '{"theme_mode": "dark"}', encoding="utf-8"
        )
        return config

    def test_migrates_legacy_files_with_valid_backups(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._config_dir(root)
            (config / "projetos.json").write_text(
                '[{"nome": "Pessoal"}]', encoding="utf-8"
            )
            (config / "preferences.json").write_text(
                '{"theme_mode": "light"}', encoding="utf-8"
            )
            history = root / "old-history"
            history.mkdir()
            (history / "historico_atividades_2026-07-15.txt").write_text(
                "registro", encoding="utf-8"
            )
            data_dir = root / "appdata"

            with patch.dict(os.environ, {"BOTVSCODE2_DATA_DIR": str(data_dir)}):
                report = prepare_user_data(config, history)

            self.assertEqual(
                [{"nome": "Pessoal"}],
                json.loads(report.paths.projects.read_text(encoding="utf-8")),
            )
            self.assertEqual("light", json.loads(
                report.paths.preferences.read_text(encoding="utf-8")
            )["theme_mode"])
            self.assertIsNotNone(report.project_backup)
            self.assertIsNotNone(report.preferences_backup)
            self.assertEqual(1, report.history_files_copied)
            self.assertTrue((report.paths.sessions_dir / history.iterdir().__next__().name).exists())
            self.assertTrue((config / "projetos.json").exists())

    def test_uses_defaults_when_no_legacy_file_exists(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._config_dir(root)
            with patch.dict(
                os.environ, {"BOTVSCODE2_DATA_DIR": str(root / "appdata")}
            ):
                report = prepare_user_data(config)

            self.assertEqual(
                [{"nome": "Padrão"}],
                json.loads(report.paths.projects.read_text(encoding="utf-8")),
            )
            self.assertIsNone(report.project_backup)

    def test_invalid_legacy_file_cancels_without_deleting_original(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._config_dir(root)
            legacy = config / "projetos.json"
            legacy.write_text("{inválido", encoding="utf-8")
            data_dir = root / "appdata"

            with patch.dict(os.environ, {"BOTVSCODE2_DATA_DIR": str(data_dir)}):
                with self.assertRaises(DataMigrationError):
                    prepare_user_data(config)

            self.assertEqual("{inválido", legacy.read_text(encoding="utf-8"))
            self.assertFalse((data_dir / "projetos.json").exists())

    def test_failure_in_second_file_rolls_back_first_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._config_dir(root)
            (config / "projetos.json").write_text("[]", encoding="utf-8")
            preferences = config / "preferences.json"
            preferences.write_text("{inválido", encoding="utf-8")
            data_dir = root / "appdata"

            with patch.dict(os.environ, {"BOTVSCODE2_DATA_DIR": str(data_dir)}):
                with self.assertRaises(DataMigrationError):
                    prepare_user_data(config)

            self.assertFalse((data_dir / "projetos.json").exists())
            self.assertFalse((data_dir / "preferences.json").exists())
            self.assertEqual("{inválido", preferences.read_text(encoding="utf-8"))

    def test_existing_personal_file_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._config_dir(root)
            data_dir = root / "appdata"
            data_dir.mkdir()
            personal = data_dir / "projetos.json"
            personal.write_text('[{"nome": "Existente"}]', encoding="utf-8")
            (data_dir / "preferences.json").write_text("{}", encoding="utf-8")

            with patch.dict(os.environ, {"BOTVSCODE2_DATA_DIR": str(data_dir)}):
                prepare_user_data(config)

            self.assertEqual(
                [{"nome": "Existente"}],
                json.loads(personal.read_text(encoding="utf-8")),
            )


if __name__ == "__main__":
    unittest.main()
