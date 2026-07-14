from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Preferences:
    theme_mode: str = "dark"
    color_seed: str = "indigo"
    font_family: str = "Segoe UI"

    @classmethod
    def load(cls, path: Path) -> Preferences:
        if not path.exists():
            preferences = cls()
            preferences.save(path)
            return preferences

        try:
            with open(path, encoding="utf-8") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return cls()

        return cls(
            theme_mode=data.get("theme_mode", "dark"),
            color_seed=data.get("color_seed", "indigo"),
            font_family=data.get("font_family", "Segoe UI"),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as file:
            json.dump(asdict(self), file, indent=2, ensure_ascii=False)
