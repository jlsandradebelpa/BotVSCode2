from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class Config:
    workspace_drive: str
    usuario: str
    empresa: str
    historico_pasta: Optional[str] = None

    @classmethod
    def load(cls, path: Path) -> Config:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        historico_pasta = data.get("historico_pasta")
        if historico_pasta is not None and not historico_pasta.strip():
            historico_pasta = None
        return cls(
            workspace_drive=data["workspace_drive"],
            usuario=data["usuario"],
            empresa=data["empresa"],
            historico_pasta=historico_pasta,
        )
