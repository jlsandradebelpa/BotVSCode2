from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def is_vscode_installed() -> bool:
    return shutil.which("code") is not None


def open_vscode(project_path: Path) -> bool:
    if not is_vscode_installed():
        return False
    try:
        result = subprocess.run(
            ["code", "."],
            cwd=str(project_path),
            capture_output=True,
            text=True,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False
    except Exception:
        return False


def close_vscode(project_path: Path) -> bool:
    import platform
    import signal

    sistema = platform.system()
    try:
        nome_pasta = project_path.resolve().name
        if sistema == "Windows":
            result = subprocess.run(
                ["taskkill", "/F", "/IM", "Code.exe"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        else:
            result = subprocess.run(
                ["pkill", "-f", f"code .*{nome_pasta}"],
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
    except Exception:
        return False
