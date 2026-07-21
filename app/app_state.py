from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path


@dataclass
class AppState:
    selected_project: str = ""

    @classmethod
    def load(cls, path: Path) -> "AppState":
        if not path.exists():
            return cls()
        try:
            with path.open(encoding="utf-8") as file:
                data = json.load(file)
            return cls(selected_project=str(data.get("selected_project", "")))
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            return cls()

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(f"{path.suffix}.tmp")
        with temporary.open("w", encoding="utf-8") as file:
            json.dump(asdict(self), file, indent=2, ensure_ascii=False)
        temporary.replace(path)
