from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class Projeto:
    nome: str
    pasta: str
    branch: str
    linguagem: str
    github_repo: Optional[str] = None
    historico_pasta: Optional[str] = None


class ProjetosManager:
    def __init__(self, path: Path) -> None:
        self._path = path
        self._projetos: List[Projeto] = []
        self._load()

    def _load(self) -> None:
        try:
            with open(self._path, encoding="utf-8") as f:
                data = json.load(f)
            self._projetos = [Projeto(**item) for item in data]
        except (OSError, json.JSONDecodeError, TypeError, KeyError):
            self._projetos = []

    def save(self) -> None:
        data = []
        for p in self._projetos:
            item = {
                "nome": p.nome,
                "pasta": p.pasta,
                "branch": p.branch,
                "linguagem": p.linguagem,
            }
            if p.github_repo:
                item["github_repo"] = p.github_repo
            if p.historico_pasta:
                item["historico_pasta"] = p.historico_pasta
            data.append(item)
        with open(self._path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def carregar(self) -> None:
        self._load()

    def adicionar(self, projeto: Projeto) -> None:
        self._projetos.append(projeto)
        self.save()

    def editar(self, index: int, projeto: Projeto) -> None:
        self._projetos[index] = projeto
        self.save()

    def remover(self, index: int) -> None:
        self._projetos.pop(index)
        self.save()

    def existe_nome(self, nome: str) -> bool:
        return any(p.nome.lower() == nome.lower() for p in self._projetos)

    @property
    def projetos(self) -> List[Projeto]:
        return list(self._projetos)

    def get_by_index(self, index: int) -> Projeto:
        return self._projetos[index]

    @property
    def count(self) -> int:
        return len(self._projetos)
