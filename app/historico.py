from __future__ import annotations

import datetime
from pathlib import Path
from typing import Optional

_DEFAULT_DIR = Path(__file__).resolve().parent.parent


def _get_historico_path(pasta: Optional[Path] = None) -> Path:
    if pasta is None:
        pasta = _DEFAULT_DIR
    hoje = datetime.datetime.now()
    return pasta / f"historico_atividades_{hoje.strftime('%Y-%m-%d')}.txt"


def registrar(tipo: str, descricao: str, pasta: Optional[Path] = None) -> None:
    path = _get_historico_path(pasta)
    path.parent.mkdir(parents=True, exist_ok=True)
    agora = datetime.datetime.now()
    timestamp = agora.strftime("%H:%M")

    if not path.exists():
        cabecalho = f"HISTORICO DE ATIVIDADES - {agora.strftime('%d/%m/%Y')}\n"
        cabecalho += "=" * 40 + "\n\n"
        with open(path, "w", encoding="utf-8") as f:
            f.write(cabecalho)

    with open(path, "r", encoding="utf-8") as f:
        linhas = [l for l in f.readlines() if "|" in l]

    seq = len(linhas) + 1

    with open(path, "a", encoding="utf-8") as f:
        f.write(f"{seq:03d} | {timestamp} | {tipo} | {descricao}\n")


def listar(pasta: Optional[Path] = None) -> list:
    path = _get_historico_path(pasta)
    if not path.exists():
        return []
    resultados = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "|" not in line:
                continue
            partes = [p.strip() for p in line.split("|")]
            if len(partes) >= 4:
                resultados.append({
                    "sequencia": partes[0],
                    "hora": partes[1],
                    "tipo": partes[2],
                    "descricao": " | ".join(partes[3:]),
                })
    return resultados


def listar_arquivos(pasta: Optional[Path] = None) -> list:
    if pasta is None:
        pasta = _DEFAULT_DIR
    if not pasta.exists():
        return []
    arquivos = sorted(pasta.glob("historico_atividades_*.txt"), reverse=True)
    return arquivos
