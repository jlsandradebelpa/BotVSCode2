# Relatório técnico de estabilização do BotVsCode2

**Data:** 15/07/2026

**Branch:** `devjlsa`

**Plano:** `PLANO_OFICIAL_ESTABILIZACAO_BOTVSCODE2.md`

## Resultado geral

As seis Sprints do plano foram implementadas no código local. A arquitetura preserva as funcionalidades existentes e remove a causa recorrente do bloqueio de atualização: arquivos pessoais controlados pelo Git.

## Sprint 1 — Configurações pessoais

### Alterações

- Criado `app/data_paths.py` para descobrir e preparar `%APPDATA%/BotVsCode2`.
- Projetos e preferências passaram a usar arquivos pessoais fora do repositório.
- Criados `config/projetos.default.json` e `config/preferences.default.json`.
- Os antigos JSONs pessoais foram preservados localmente e retirados do Git.
- Histórico passou a ser gravado em `sessions/`.
- Criados diretórios `logs/`, `backup/` e `sessions/`.
- Criado `state.json` para preservar o projeto selecionado.
- Migração implementada com backup, validação, arquivos temporários e rollback.

### Migração real executada

- Destino: `C:\Users\JLSAndrade\AppData\Roaming\BotVsCode2`.
- Backups de projetos e preferências criados.
- Seis arquivos históricos copiados.
- Nenhum arquivo antigo foi apagado.

### Risco conhecido

Os arquivos antigos ignorados permanecem na pasta `config/` desta máquina para recuperação. Eles não são mais lidos depois que a migração pessoal existe.

## Sprint 2 — Iniciar atividades

- Fetch com limpeza de referências remotas.
- Validação da branch configurada, branch atual e upstream.
- Comparação explícita de commits à frente e atrás.
- Pull restrito a `--ff-only`.
- Bloqueio de branch divergente, conflito e upstream ausente.
- Alterações locais são listadas; o usuário pode cancelar ou abrir sem pull.
- Nenhuma branch é trocada automaticamente.

Ao escolher “Abrir sem atualizar”, o usuário aceita trabalhar com o estado local atual. A interface registra essa condição.

## Sprint 3 — Encerrar atividades

- Fetch obrigatório no início do encerramento.
- Bloqueio quando o remoto avançou.
- Lista de arquivos com seleção individual.
- `git add` somente nos arquivos selecionados.
- Sugestão automática e edição da mensagem de commit.
- Novo fetch após o commit e antes do push.
- Push cancelado se a situação remota mudar.

Se o fetch falhar depois do commit, o commit permanece local e o push não acontece. A interface informa essa situação para evitar perda de trabalho.

## Sprint 4 — Validação de branch

A mesma validação segura é aplicada ao iniciar, encerrar e imediatamente antes do push. Diferenças mostram branch configurada, atual e upstream, sem troca automática.

## Sprint 5 — Certificados

Os subprocessos Git usam `GIT_SSL_BACKEND=schannel` no Windows. A validação SSL permanece ativa; nenhuma opção equivalente a `sslVerify=false` foi adicionada.

## Sprint 6 — Testes

Foram criados testes para estado da interface, migração, rollback, proteção da configuração pessoal, repositórios Git reais, fast-forward, alterações locais, staging seletivo, upstream inexistente, conflito real, falha SSL, branch incorreta, divergência e remoto avançado.

## Arquivos principais modificados

- `.gitignore` — impede novo rastreamento dos JSONs pessoais.
- `app/data_paths.py` — estrutura e migração de dados pessoais.
- `app/app_state.py` — estado persistente da interface.
- `app/main.py` — inicialização pela nova estrutura.
- `app/git_tools.py` — operações Git seguras.
- `app/services/git_service.py` — exposição das novas operações.
- `app/ui/app.py` — APPDATA, histórico e estado selecionado.
- `app/ui/paginas/inicio.py` — fluxos seguros de início e encerramento.
- `tests/` — testes de migração, Git real, estado e interface.

## Validações realizadas

- Suíte `unittest`: 28 testes aprovados na validação final.
- `compileall`: concluído sem erros.
- `git diff --check`: concluído sem erros de whitespace.
- Preferências reais salvas novamente em `%APPDATA%` sem criar alteração do JSON pessoal no Git.
- Inicialização real do Flet: processo aberto e responsivo, encerrado após a inspeção.

## Correções posteriores (20/07/2026)

Após o período de observação, os seguintes bugs foram corrigidos e melhorias implementadas:

### Correções

- **`git_tools.py`**: `push()` e `pull()` agora usam `git push <remote> <branch>` e `git pull --ff-only <remote> <branch>` extraindo remote do upstream — antes ignoravam branch configurada.
- **`vscode.py`**: `close_vscode()` agora mata apenas o VS Code do projeto (filtro PowerShell por `CommandLine` contendo o nome da pasta), não todas as instâncias.
- **`projetos.py`**: `_load()` trata JSON corrompido silenciosamente (lista vazia) em vez de crashar.
- **`git_tools.py`**: `get_changed_files()` — renames/copies (status R/C) agora retornam `path`=novo, `original`=antigo (estavam invertidos).
- **`inicio.py`**: Timestamp "Última sincronização" só atualiza com `sincronizado=True`.
- **`tools_git.py` (MCP)**: `arquivos_alterados` agora exclui arquivos novos/não rastreados (`??`) — antes contava dobrado.
- **`preferences.py`**: `save()` agora usa escrita atômica (temp + replace) para evitar corrupção.
- **`chat_service.py`**: `_handle_selection()` usa `.lstrip("/")` antes de `int()` — `/8` agora funciona.
- **Chat**: `encerrar_atividades` agora oferece `/commit <msg>` em vez de redirecionar para GUI; inclui re-fetch antes do push.
- **CREATE_NO_WINDOW** adicionado em todos os subprocess calls (`git_tools.py`, `vscode.py`, `github_tools.py`, `mcp_server/tools_git.py`, `app.py`) eliminando a janela preta do terminal.

### Melhorias

- **Menu suspenso**: `PopupMenuButton` na barra principal com Configurações, Sobre (v2.0.0) e Backlog (git log + GitHub issues abertas).
- **Skill `gestao-projetos`**: criada para opencode em `~/.config/opencode/skills/gestao-projetos/SKILL.md`.

### Issues criadas no GitHub

- [#20](https://github.com/jlsandradebelpa/BotVSCode2/issues/20) — bugs críticos (push/pull, close_vscode, JSON, terminal)
- [#21](https://github.com/jlsandradebelpa/BotVSCode2/issues/21) — rename, timestamp, MCP, chat /8
- [#22](https://github.com/jlsandradebelpa/BotVSCode2/issues/22) — chat /commit + re-fetch
- [#23](https://github.com/jlsandradebelpa/BotVSCode2/issues/23) — menu suspenso

Todas adicionadas ao Project 9 BotVSCode2 com status **Concluído**.

## Próximos passos operacionais

1. Usar o BotVsCode2 por alguns dias na branch `devjlsa`.
2. Registrar qualquer comportamento inesperado com projeto, branch e mensagem exibida.
3. Somente após estabilidade real, promover por Pull Request para `main`.
4. Não iniciar BotVsCode3 antes desse período de observação.
