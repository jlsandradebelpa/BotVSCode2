from __future__ import annotations

import os
import shutil
import subprocess
from pathlib import Path


def is_vscode_installed() -> bool:
    return shutil.which("code") is not None


def open_vscode(project_path: Path) -> bool:
    if not is_vscode_installed():
        return False
    try:
        kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        subprocess.Popen(
            ["code", "."],
            cwd=str(project_path),
            **kwargs,
        )
        return True
    except FileNotFoundError:
        return False
    except Exception:
        return False


def close_vscode(project_path: Path) -> bool:
    import platform

    sistema = platform.system()
    try:
        nome_pasta = project_path.resolve().name
        kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
        if sistema == "Windows":
            cmd = [
                "powershell", "-NoProfile", "-Command",
                f"Get-CimInstance Win32_Process -Filter \"Name='Code.exe'\" | "
                f"Where-Object {{ $_.CommandLine -like '*{nome_pasta}*' }} | "
                f"ForEach-Object {{ Stop-Process -Id $_.ProcessId -Force }}",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, **kwargs)
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
