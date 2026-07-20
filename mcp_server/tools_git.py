from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

_BASE_DIR = Path(__file__).resolve().parent
_PROJETOS_FILE = _BASE_DIR / "projetos.json"
_LOGS_DIR = _BASE_DIR.parent / "logs"
_LOG_FILE = _LOGS_DIR / "log_atividades.txt"

_COMANDOS_PERMITIDOS = {
    "git status",
    "git branch --show-current",
    "git remote -v",
    "git pull",
    "git add .",
    "git commit -m",
    "git push",
}

_COMANDOS_BLOQUEADOS = [
    "rm", "del", "format",
    "git reset --hard", "git clean",
    "git push --force", "git push -f",
    "git rebase", "git checkout",
]


def _carregar_projetos() -> list[dict]:
    with open(_PROJETOS_FILE, encoding="utf-8") as f:
        data = json.load(f)
    return data["projetos"]


def _localizar_projeto(nome: str) -> dict | None:
    projetos = _carregar_projetos()
    for p in projetos:
        if p["nome"].lower() == nome.lower():
            for caminho in p["caminhos_possiveis"]:
                if Path(caminho).exists():
                    return {
                        "nome": p["nome"],
                        "caminho": caminho,
                        "branch_padrao": p["branch_padrao"],
                        "remote": p["remote"],
                    }
            return {
                "nome": p["nome"],
                "caminho": None,
                "branch_padrao": p["branch_padrao"],
                "remote": p["remote"],
                "erro": f"Nenhum caminho encontrado para o projeto {nome}. Verifique os caminhos em projetos.json.",
            }
    return None


def _executar_git(caminho: str, *args: str) -> tuple[int, str, str]:
    cmd = ["git", "-C", caminho, *args]
    kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", **kwargs)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def _validar_seguranca(comando: str) -> str | None:
    cmd_lower = comando.lower().strip()
    for bloqueado in _COMANDOS_BLOQUEADOS:
        if cmd_lower.startswith(bloqueado):
            return f"Comando bloqueado por seguranca: {bloqueado}"
    return None


def _registrar_log(projeto: str, acao: str, resultado: str, mensagem: str = "") -> None:
    _LOGS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    linha = f"{timestamp} | {projeto} | {acao} | {resultado}"
    if mensagem:
        linha += f" | {mensagem}"
    with open(_LOG_FILE, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


def tool_listar_projetos() -> str:
    projetos = _carregar_projetos()
    resultado = []
    for p in projetos:
        caminho_encontrado = None
        for c in p["caminhos_possiveis"]:
            if Path(c).exists():
                caminho_encontrado = c
                break
        resultado.append({
            "nome": p["nome"],
            "caminho": caminho_encontrado,
            "branch_padrao": p["branch_padrao"],
            "remote": p["remote"],
        })
    return json.dumps({"projetos": resultado}, ensure_ascii=False, indent=2)


def tool_status_git(projeto: str) -> str:
    proj = _localizar_projeto(projeto)
    if not proj:
        return json.dumps({"erro": f"Projeto '{projeto}' nao encontrado."}, ensure_ascii=False, indent=2)
    if proj.get("erro"):
        return json.dumps({"erro": proj["erro"]}, ensure_ascii=False, indent=2)
    caminho = proj["caminho"]
    if not Path(caminho).exists():
        return json.dumps({"erro": f"Caminho {caminho} nao existe."}, ensure_ascii=False, indent=2)

    _, branch, _ = _executar_git(caminho, "branch", "--show-current")
    _, status, _ = _executar_git(caminho, "status", "--short")
    _, remotes, _ = _executar_git(caminho, "remote", "-v")

    linhas_status = [s for s in status.split("\n") if s.strip()]
    modificados = [s[3:] for s in linhas_status if not s.startswith("??") and s.strip()]
    novos = [s[3:] for s in linhas_status if s.startswith("??")]

    return json.dumps({
        "projeto": proj["nome"],
        "caminho": caminho,
        "branch": branch,
        "remote": remotes,
        "arquivos_alterados": len(modificados),
        "arquivos_alterados_lista": modificados,
        "arquivos_novos": len(novos),
        "arquivos_novos_lista": novos,
    }, ensure_ascii=False, indent=2)


def tool_preparar_commit_push(projeto: str, mensagem_commit: str) -> str:
    proj = _localizar_projeto(projeto)
    if not proj:
        return json.dumps({"erro": f"Projeto '{projeto}' nao encontrado."}, ensure_ascii=False, indent=2)
    if proj.get("erro"):
        return json.dumps({"erro": proj["erro"]}, ensure_ascii=False, indent=2)

    caminho = proj["caminho"]

    if not Path(caminho).exists():
        return json.dumps({"erro": f"Caminho {caminho} nao existe."}, ensure_ascii=False, indent=2)

    _, branch, _ = _executar_git(caminho, "branch", "--show-current")
    if branch != proj["branch_padrao"]:
        return json.dumps({"erro": f"Branch atual '{branch}' diverge da branch padrao '{proj['branch_padrao']}'."}, ensure_ascii=False, indent=2)

    _, remotes, _ = _executar_git(caminho, "remote", "-v")
    if proj["remote"] not in remotes:
        return json.dumps({"erro": f"Remote '{proj['remote']}' nao configurado."}, ensure_ascii=False, indent=2)

    _, status, _ = _executar_git(caminho, "status", "--short")
    if not status.strip():
        return json.dumps({"erro": "Nao ha arquivos alterados para commit."}, ensure_ascii=False, indent=2)

    code_add, out_add, err_add = _executar_git(caminho, "add", ".")
    if code_add != 0:
        return json.dumps({"erro": f"Erro ao preparar add: {err_add}"}, ensure_ascii=False, indent=2)

    code_commit, out_commit, err_commit = _executar_git(caminho, "commit", "-m", mensagem_commit)
    if code_commit != 0:
        return json.dumps({"erro": f"Erro ao criar commit: {err_commit}"}, ensure_ascii=False, indent=2)

    _registrar_log(projeto, "git commit", "sucesso", mensagem_commit)

    return json.dumps({
        "status": "commit_preparado",
        "projeto": projeto,
        "branch": branch,
        "mensagem": mensagem_commit,
        "saida_commit": out_commit,
    }, ensure_ascii=False, indent=2)


def tool_confirmar_push(projeto: str) -> str:
    proj = _localizar_projeto(projeto)
    if not proj:
        return json.dumps({"erro": f"Projeto '{projeto}' nao encontrado."}, ensure_ascii=False, indent=2)
    if proj.get("erro"):
        return json.dumps({"erro": proj["erro"]}, ensure_ascii=False, indent=2)

    caminho = proj["caminho"]
    branch = proj["branch_padrao"]
    remote = proj["remote"]

    code_push, out_push, err_push = _executar_git(caminho, "push", remote, branch)
    if code_push != 0:
        return json.dumps({"erro": f"Erro ao enviar push: {err_push}"}, ensure_ascii=False, indent=2)

    _registrar_log(projeto, "git push", "sucesso", f"push {remote}/{branch}")

    return json.dumps({
        "status": "push_realizado",
        "projeto": projeto,
        "remote": remote,
        "branch": branch,
        "resultado": out_push,
    }, ensure_ascii=False, indent=2)


def tool_git_pull_projeto(projeto: str) -> str:
    proj = _localizar_projeto(projeto)
    if not proj:
        return json.dumps({"erro": f"Projeto '{projeto}' nao encontrado."}, ensure_ascii=False, indent=2)
    if proj.get("erro"):
        return json.dumps({"erro": proj["erro"]}, ensure_ascii=False, indent=2)

    caminho = proj["caminho"]

    if not Path(caminho).exists():
        return json.dumps({"erro": f"Caminho {caminho} nao existe."}, ensure_ascii=False, indent=2)

    _, branch, _ = _executar_git(caminho, "branch", "--show-current")
    if branch != proj["branch_padrao"]:
        return json.dumps({"erro": f"Branch atual '{branch}' diverge da branch padrao '{proj['branch_padrao']}'."}, ensure_ascii=False, indent=2)

    _, remotes, _ = _executar_git(caminho, "remote", "-v")
    if proj["remote"] not in remotes:
        return json.dumps({"erro": f"Remote '{proj['remote']}' nao configurado."}, ensure_ascii=False, indent=2)

    code, out, err = _executar_git(caminho, "pull", proj["remote"], branch)
    if code != 0:
        return json.dumps({"erro": f"Erro ao executar pull: {err}"}, ensure_ascii=False, indent=2)

    _registrar_log(projeto, "git pull", "sucesso", f"pull {proj['remote']}/{branch}")

    return json.dumps({
        "status": "pull_realizado",
        "projeto": projeto,
        "remote": proj["remote"],
        "branch": branch,
        "resultado": out,
    }, ensure_ascii=False, indent=2)


def tool_registrar_log_atividade(projeto: str, acao: str, resultado: str, mensagem: str = "") -> str:
    _registrar_log(projeto, acao, resultado, mensagem)
    return json.dumps({"status": "log_registrado"}, ensure_ascii=False, indent=2)
