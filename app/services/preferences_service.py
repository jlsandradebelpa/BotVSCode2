from __future__ import annotations

from pathlib import Path

from preferences import Preferences


class PreferencesService:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._preferences = Preferences.load(path)

    @property
    def preferences(self) -> Preferences:
        return Preferences(**vars(self._preferences))

    def salvar(self, theme_mode: str, color_seed: str, font_family: str) -> Preferences:
        self._preferences = Preferences(
            theme_mode=theme_mode,
            color_seed=color_seed,
            font_family=font_family,
        )
        self._preferences.save(self._path)
        return self.preferences
    def restaurar(self) -> Preferences:
        self._preferences = Preferences()
        self._preferences.save(self._path)
        return self.preferences
