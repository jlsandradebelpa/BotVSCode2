# BotVSCode - MCP Server

## Sobre

MCP Server local para o BotVSCode, permitindo que agentes de IA executem ações controladas em projetos Git do usuário via protocolo MCP (Model Context Protocol).

## Estrutura

```
mcp_server/
  server.py        # Servidor JSON-RPC via stdio (MCP compatível)
  tools_git.py     # Implementação das 6 ferramentas Git
  projetos.json    # Registro de projetos monitorados
logs/
  log_atividades.txt  # Histórico de operações realizadas
README_MCP.md      # Este arquivo
```

## Ferramentas MCP

| Ferramenta | Descrição |
|---|---|
| `listar_projetos` | Lista projetos configurados |
| `status_git` | Verifica status Git (branch, alterações, remote) |
| `preparar_commit_push` | `git add .` + `git commit -m` com validações |
| `confirmar_push` | `git push` no remote e branch configurados (requer confirmação) |
| `git_pull_projeto` | `git pull` no remote e branch configurados |
| `registrar_log_atividade` | Registra operação no log |

## Como usar

### Iniciar o servidor

```bash
cd C:\projetos\botvscode
python mcp_server\server.py
```

O servidor escuta JSON-RPC via stdin/stdout.

### Testar manualmente

```bash
echo "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"list_tools\"}" | python mcp_server\server.py
```

### Fluxo típico (voz do usuário)

```
"Suba o projeto intprotheussoc para o GitHub remoto."
```

1. `listar_projetos` → confirma que o projeto existe
2. `status_git(projeto="intprotheussoc")` → verifica branch e alterações
3. Agente pergunta a mensagem do commit
4. `preparar_commit_push(projeto="intprotheussoc", mensagem_commit="...")` → add + commit
5. Agente pergunta se pode enviar ao remoto
6. `confirmar_push(projeto="intprotheussoc")` → push para a branch configurada

## Segurança

- Apenas comandos Git pré-aprovados são executados
- `push` exige confirmação explícita do usuário via agente
- Comandos destrutivos são bloqueados (`rm`, `git reset --hard`, `git push --force`, etc.)
- Nenhum comando livre de terminal é aceito

## Projetos monitorados

Configurados em `mcp_server/projetos.json`. Atualmente:

- `intprotheussoc` (`devjlsa`)
- `cbaa_asfaltos_empresa` (`devjlsa`)
- `botvscode` (`devjlsa`)
- `botvscode2` (`devjlsa`)
- `OpenCodeSessionExplorer`

O projeto `candidato_cbaa` não deve receber operações automatizadas nesta
estação enquanto o clone local não estiver disponível e validado.
