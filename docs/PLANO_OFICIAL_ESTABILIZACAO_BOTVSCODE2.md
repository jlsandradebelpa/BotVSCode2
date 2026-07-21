# BotVSCode2 — Plano oficial de estabilização

**Versão:** 2.x

**Autor do plano:** ChatGPT (Orquestrador)

**Executor:** Codex / OpenCode

## Objetivo

Antes do desenvolvimento do BotVsCode3, estabilizar completamente o BotVsCode2 sem reescrever o projeto, preservando as funcionalidades existentes e eliminando os problemas encontrados durante o uso diário.

O BotVsCode2 é um assistente de produtividade, não um cliente Git. Deve orientar, diagnosticar, automatizar somente operações seguras e nunca tomar decisões destrutivas automaticamente.

## Regras gerais

- Não remover funcionalidades existentes.
- Manter compatibilidade com a versão atual.
- Não adicionar funcionalidades fora deste plano.
- Cada Sprint deve terminar com aplicação funcional e testes executados.
- Nunca executar automaticamente `git reset --hard`, `git clean -fd` ou `git push --force`.
- Nunca apagar arquivos, sobrescrever configurações pessoais ou descartar alterações locais.

## Sprint 1 — Separação das configurações pessoais

Mover projetos, preferências, histórico, estado da interface, logs e backups para:

```text
%APPDATA%/BotVsCode2/
  projetos.json
  preferences.json
  state.json
  logs/
  backup/
  sessions/
```

Manter no repositório apenas `config/projetos.default.json` e `config/preferences.default.json`. A migração deve detectar arquivos antigos, criar backup, copiar, validar e cancelar sem perda se qualquer etapa falhar.

## Sprint 2 — Iniciar atividades

Fluxo obrigatório: selecionar projeto, verificar Git, executar `git fetch --prune`, validar branch e upstream, comparar commits, executar `git pull --ff-only` apenas quando seguro e abrir a sessão.

- Repositório atualizado: abrir normalmente.
- Atrás do remoto: atualizar automaticamente por fast-forward only.
- Alterações locais: não executar pull; listar arquivos e permitir decisão do usuário.
- Branch incorreta: mostrar configurada, atual e upstream; nunca trocar automaticamente.
- Branch divergente ou com conflitos: bloquear.

## Sprint 3 — Encerrar atividades

Executar fetch, verificar remoto, listar e selecionar arquivos, executar `git add <arquivo>`, confirmar commit e push. A mensagem de commit deve ser sugerida e editável. Um novo fetch é obrigatório antes do push; se o remoto avançar, o push deve ser cancelado.

## Sprint 4 — Validação de branch

Sempre validar branch configurada, branch local, branch remota e upstream, apresentando divergências de forma clara.

## Sprint 5 — Certificados

Usar o backend de certificados Windows `schannel`. Nunca desabilitar a validação SSL.

## Sprint 6 — Testes

Cobrir repositório limpo, atrasado, alteração local, branch incorreta, upstream inexistente, conflito, falha SSL, migração e interrupção da migração.

## Critérios de aceite

- aplicação compilando;
- testes executados;
- nenhuma regressão identificada;
- alterações pessoais não sujam o Git;
- relatório técnico entregue;
- BotVsCode3 somente após alguns dias de operação estável.

Este plano substitui os planejamentos anteriores relacionados à estabilização do BotVsCode2.
