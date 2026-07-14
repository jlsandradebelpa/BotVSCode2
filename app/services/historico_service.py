from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from historico import registrar as registrar_historico, listar as listar_historico


class HistoricoService:
    def __init__(self, pasta_padrao: Optional[Path] = None) -> None:
        self._pasta_padrao = pasta_padrao

    def registrar(self, tipo: str, descricao: str, pasta: Optional[Path] = None) -> None:
        registrar_historico(tipo, descricao, pasta or self._pasta_padrao)

    def listar(self, pasta: Optional[Path] = None) -> List[dict]:
        return listar_historico(pasta or self._pasta_padrao)
