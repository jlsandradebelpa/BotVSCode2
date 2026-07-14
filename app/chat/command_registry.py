from __future__ import annotations

from typing import Callable, Dict, List, Optional


class CommandRegistry:
    def __init__(self) -> None:
        self._commands: Dict[str, dict] = {}

    def register(
        self, command: str, handler: Callable[[str], str], description: str = ""
    ) -> None:
        self._commands[command] = {
            "handler": handler,
            "description": description,
        }

    def get_handler(self, command: str) -> Optional[Callable[[str], str]]:
        entry = self._commands.get(command)
        return entry["handler"] if entry else None

    def list_commands(self) -> List[dict]:
        return [
            {"command": cmd, "description": info["description"]}
            for cmd, info in self._commands.items()
        ]

    def search(self, prefix: str) -> List[str]:
        return [cmd for cmd in self._commands if cmd.startswith(prefix)]

    @property
    def commands(self) -> Dict[str, dict]:
        return dict(self._commands)
