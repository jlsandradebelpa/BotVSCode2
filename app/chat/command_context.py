from __future__ import annotations

from typing import Optional

from projetos import Projeto


class CommandContext:
    def __init__(self) -> None:
        self._current_project: Optional[Projeto] = None
        self._awaiting_selection: bool = False

    @property
    def current_project(self) -> Optional[Projeto]:
        return self._current_project

    @current_project.setter
    def current_project(self, projeto: Optional[Projeto]) -> None:
        self._current_project = projeto

    @property
    def awaiting_selection(self) -> bool:
        return self._awaiting_selection

    @awaiting_selection.setter
    def awaiting_selection(self, value: bool) -> None:
        self._awaiting_selection = value

    def clear(self) -> None:
        self._current_project = None
        self._awaiting_selection = False
