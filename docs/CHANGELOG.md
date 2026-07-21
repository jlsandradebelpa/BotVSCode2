# Changelog

## 2026-07-20

1. Correção: `push()` e `pull()` agora usam remote e branch explícitos extraídos do upstream
2. Correção: `close_vscode()` agora mata apenas o VS Code do projeto (filtro por nome da pasta)
3. Correção: `projetos.py:_load()` trata JSON corrompido silenciosamente em vez de crashar
4. Correção: `get_changed_files()` — paths de rename/copy não ficam mais invertidos
5. Correção: timestamp "Última sincronização" só atualiza em sincronização real
6. Correção: MCP server não conta arquivos novos (`??`) como modificados (dupla contagem)
7. Correção: chat `_handle_selection()` usa `lstrip("/")` — `/8` funciona
8. Correção: `preferences.py:save()` usa escrita atômica (temp + replace)
9. Correção: chat `encerrar-atividades` oferece `/commit` em vez de redirecionar para GUI (elimina dead-end)
10. Correção: `CREATE_NO_WINDOW` em todos os subprocessos (elimina janela preta do terminal)
11. Melhoria: menu `PopupMenuButton` com Configurações, Sobre (v2.0.0) e Changelog
12. Melhoria: comando `/commit <mensagem>` no chat
13. Melhoria: comando `/opencode` no chat (abre OpenCode no diretório do projeto)
14. Melhoria: `mcp_server/` expõe 6 ferramentas Git via MCP
15. Melhoria: skill `gestao-projetos` para OpenCode
16. Melhoria: diálogo "Selecionar arquivos" com espaçamento entre itens e botão Marcar/Desmarcar todas
17. Documentação: `docs/CHANGELOG.md` criado
18. Documentação: `docs/ARQUITETURA.md`, `FASE_02.md`, `FASE_03_UX_FLUXOS.md`,
   `FASE_05_CHAT_INTEGRADO.md`, `RELATORIO_ESTABILIZACAO_2026-07-15.md`,
   `ROADMAP.md` atualizados
