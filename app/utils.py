from __future__ import annotations

import datetime
from pathlib import Path
from typing import Optional

DRIVES = ["D:", "E:"]


def detect_workspace_drive(relative_path: str) -> Optional[str]:
    for drive in DRIVES:
        full_path = Path(f"{drive}\\{relative_path}")
        if full_path.exists():
            return drive
    return None


def resolve_full_path(workspace_drive: str, caminho: str) -> Path:
    caminho_path = Path(caminho)
    if caminho_path.is_absolute():
        return caminho_path
    if workspace_drive == "AUTO":
        detected = detect_workspace_drive(caminho)
        if detected:
            return Path(f"{detected}\\{caminho}")
        raise FileNotFoundError(
            f"Não foi possível detectar a unidade para: {caminho}"
        )
    return Path(f"{workspace_drive}\\{caminho}")


def saudacao() -> str:
    hora = datetime.datetime.now().hour
    if hora < 12:
        return "Bom dia!"
    if hora < 18:
        return "Boa tarde!"
    return "Boa noite!"
