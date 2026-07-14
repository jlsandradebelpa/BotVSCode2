from __future__ import annotations

from typing import List, Optional, Tuple


class CommandParser:
    COMMAND_PREFIX = "/"

    @classmethod
    def is_command(cls, text: str) -> bool:
        return text.strip().startswith(cls.COMMAND_PREFIX)

    @classmethod
    def parse(cls, text: str) -> Tuple[Optional[str], str]:
        stripped = text.strip()
        if not cls.is_command(stripped):
            return None, stripped
        parts = stripped[len(cls.COMMAND_PREFIX):].split(maxsplit=1)
        command = parts[0].lower() if parts else None
        args = parts[1] if len(parts) > 1 else ""
        return command, args

    @classmethod
    def get_suggestions(
        cls, text: str, available_commands: List[str]
    ) -> List[str]:
        stripped = text.strip()
        if not cls.is_command(stripped):
            return []
        partial = stripped[len(cls.COMMAND_PREFIX):].lower()
        if not partial:
            return sorted(available_commands)
        return sorted([cmd for cmd in available_commands if cmd.startswith(partial)])
