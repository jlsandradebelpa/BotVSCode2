from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Tuple

from projetos import Projeto, ProjetosManager


class ProjectService:
    def __init__(self, projetos_manager: ProjetosManager) -> None:
        self._manager = projetos_manager

    @property
    def projetos(self) -> List[Projeto]:
        return self._manager.projetos

    @property
    def count(self) -> int:
        return self._manager.count

    def get_by_index(self, index: int) -> Optional[Projeto]:
        if 0 <= index < self._manager.count:
            return self._manager.get_by_index(index)
        return None

    def adicionar(self, nome: str, pasta: str, branch: str, linguagem: str,
                  github_repo: str = "", historico_pasta: str = "") -> Tuple[bool, str]:
        if self._manager.existe_nome(nome):
            return False, f"Já existe um projeto com o nome '{nome}'."
        repo = github_repo if github_repo.strip() else None
        hist = historico_pasta if historico_pasta.strip() else None
        projeto = Projeto(nome=nome, pasta=pasta, branch=branch,
                          linguagem=linguagem, github_repo=repo,
                          historico_pasta=hist)
        self._manager.adicionar(projeto)
        return True, "Projeto adicionado com sucesso."

    def editar(self, index: int, nome: str, pasta: str, branch: str,
               linguagem: str, github_repo: str = "",
               historico_pasta: str = "") -> Tuple[bool, str]:
        if not (0 <= index < self._manager.count):
            return False, "Índice inválido."
        repo = github_repo if github_repo.strip() else None
        hist = historico_pasta if historico_pasta.strip() else None
        projeto = Projeto(nome=nome, pasta=pasta, branch=branch,
                          linguagem=linguagem, github_repo=repo,
                          historico_pasta=hist)
        self._manager.editar(index, projeto)
        return True, "Projeto atualizado com sucesso."

    def remover(self, index: int) -> Tuple[bool, str]:
        if not (0 <= index < self._manager.count):
            return False, "Índice inválido."
        nome = self._manager.get_by_index(index).nome
        self._manager.remover(index)
        return True, f"Projeto '{nome}' removido com sucesso."

    def existe_nome(self, nome: str) -> bool:
        return self._manager.existe_nome(nome)