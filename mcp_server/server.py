from __future__ import annotations

import json
import sys
from typing import Any

from tools_git import (
    tool_listar_projetos,
    tool_status_git,
    tool_preparar_commit_push,
    tool_confirmar_push,
    tool_git_pull_projeto,
    tool_registrar_log_atividade,
)

_FERRAMENTAS: dict[str, dict[str, Any]] = {
    "listar_projetos": {
        "descricao": "Lista os projetos configurados no BotVSCode",
        "parametros": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    "status_git": {
        "descricao": "Verifica o status Git de um projeto (branch, alteracoes, remote)",
        "parametros": {
            "type": "object",
            "properties": {
                "projeto": {
                    "type": "string",
                    "description": "Nome do projeto",
                }
            },
            "required": ["projeto"],
        },
    },
    "preparar_commit_push": {
        "descricao": "Prepara commit (git add . + git commit -m). Valida projeto, branch e remote.",
        "parametros": {
            "type": "object",
            "properties": {
                "projeto": {
                    "type": "string",
                    "description": "Nome do projeto",
                },
                "mensagem_commit": {
                    "type": "string",
                    "description": "Mensagem do commit",
                },
            },
            "required": ["projeto", "mensagem_commit"],
        },
    },
    "confirmar_push": {
        "descricao": "Executa git push origin main. Exige confirmacao explicita do usuario.",
        "parametros": {
            "type": "object",
            "properties": {
                "projeto": {
                    "type": "string",
                    "description": "Nome do projeto",
                },
            },
            "required": ["projeto"],
        },
    },
    "git_pull_projeto": {
        "descricao": "Executa git pull origin main no projeto. Valida branch e remote.",
        "parametros": {
            "type": "object",
            "properties": {
                "projeto": {
                    "type": "string",
                    "description": "Nome do projeto",
                },
            },
            "required": ["projeto"],
        },
    },
    "registrar_log_atividade": {
        "descricao": "Registra uma entrada no log de atividades do projeto",
        "parametros": {
            "type": "object",
            "properties": {
                "projeto": {
                    "type": "string",
                    "description": "Nome do projeto",
                },
                "acao": {
                    "type": "string",
                    "description": "Acao realizada (git push, git commit, etc.)",
                },
                "resultado": {
                    "type": "string",
                    "description": "Resultado (sucesso, erro, etc.)",
                },
                "mensagem": {
                    "type": "string",
                    "description": "Mensagem complementar (opcional)",
                },
            },
            "required": ["projeto", "acao", "resultado"],
        },
    },
}

_HANDLERS: dict[str, Any] = {
    "listar_projetos": lambda args: tool_listar_projetos(),
    "status_git": lambda args: tool_status_git(args["projeto"]),
    "preparar_commit_push": lambda args: tool_preparar_commit_push(args["projeto"], args["mensagem_commit"]),
    "confirmar_push": lambda args: tool_confirmar_push(args["projeto"]),
    "git_pull_projeto": lambda args: tool_git_pull_projeto(args["projeto"]),
    "registrar_log_atividade": lambda args: tool_registrar_log_atividade(
        args["projeto"], args["acao"], args["resultado"], args.get("mensagem", "")
    ),
}


def _handle_request(request: dict) -> str:
    req_id = request.get("id", 0)
    method = request.get("method", "")

    if method == "list_tools":
        tools_list = []
        for name, info in _FERRAMENTAS.items():
            tools_list.append({
                "name": name,
                "description": info["descricao"],
                "inputSchema": info["parametros"],
            })
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {"tools": tools_list},
        })

    elif method == "call_tool":
        params = request.get("params", {})
        tool_name = params.get("name", "")
        tool_args = params.get("arguments", {})

        if tool_name not in _HANDLERS:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Ferramenta '{tool_name}' nao encontrada"},
            })

        try:
            resultado = _HANDLERS[tool_name](tool_args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": resultado,
                        }
                    ],
                },
            }, ensure_ascii=False)
        except Exception as e:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32603, "message": str(e)},
            }, ensure_ascii=False)

    else:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": -32601, "message": f"Metodo '{method}' nao suportado"},
        })


def main() -> None:
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            request = json.loads(line)
        except json.JSONDecodeError:
            continue
        response = _handle_request(request)
        print(response, flush=True)


if __name__ == "__main__":
    main()