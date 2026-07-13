# Roadmap — BotVSCode / JA WorkStart

## Fase 0 — Infraestrutura *(Concluída)*

- [x] Repositório GitHub (`jlsandradebelpa/botvscode`)
- [x] GitHub Project com Board (Pendente → Em andamento → Concluído)
- [x] 15 issues iniciais com labels
- [x] Estrutura de diretórios (`app/`, `config/`, `docs/`, `tests/`, `assets/`)
- [x] Documentação base (README, ROADMAP, ARQUITETURA, PROJECT_GITHUB)
- [x] Diretrizes de desenvolvimento documentadas

## Fase 1 — Núcleo *(Concluída)*

- [x] Leitura de configuração (`config.json`)
- [x] Cadastro e listagem de projetos (`projetos.json`)
- [x] Detecção automática de unidade (D: / E:)
- [x] Módulos stub preparados (git, vscode, speech)

## Fase 2 — Ciclo de Sincronização *(Concluída)*

- [x] Menu principal com dois modos: Iniciar Trabalho / Encerrar Trabalho
- [x] Fluxo **Iniciar Trabalho**: fetch → compara branch → pull → abrir VS Code
- [x] Fluxo **Encerrar Trabalho**: status → commit → push
- [x] Validação de repositório Git
- [x] Detecção de alterações locais
- [x] Confirmação do usuário antes de ações destrutivas
- [x] Abertura automática do VS Code
- [x] Tratamento de erros (Git não instalado, VS Code não instalado)

## Fase 3 — Self-Hosting: BotVSCode gerencia o próprio desenvolvimento *(Concluída)*

- [x] BotVSCode adicionado à lista de projetos gerenciados
- [x] Suporte genérico a caminhos absolutos em `resolve_full_path`
- [x] Fluxos Iniciar/Encerrar Trabalho funcionando para o próprio projeto
- [x] Documentação da atualização (FASE_03.md)

## Fase 4 — Tarefas Pendentes e Histórico *(Concluída)*

- [x] Campo `github_repo` no cadastro de projetos
- [x] Consulta de GitHub Issues via API REST (`github_tools.py`)
- [x] Listagem de tarefas pendentes ao final do fluxo "Iniciar Trabalho"
- [x] Registro de histórico diário de atividades (`historico.py`)
- [x] Tratamento de ausência de conexão ou token
- [x] Documentação da atualização (FASE_04.md)

## Fase 5 — Voz *(Não iniciada)*

- [ ] Síntese de voz (confirmação falada, notificações)

## Fase 6 — Assistente Inteligente *(Não iniciada)*

- [ ] Execução em lote (sincronizar vários projetos)
- [ ] Favoritar projetos mais usados
- [ ] Sugestão de próximo projeto com base no histórico
- [ ] Resumo automatizado de alterações (git log)

## Fase 7 — IA *(Não iniciada)*

- [ ] Assistente contextual via LLM local
- [ ] Análise de diff com linguagem natural

## Fase 6 — Distribuição *(Não iniciada)*

- [ ] Atalho na Área de Trabalho ("BotVSCode")
- [ ] Atalho no Menu Iniciar ("BotVSCode")
- [ ] Instalador do sistema
- [ ] Empacotamento (PyInstaller ou similar)

---

*Este roadmap é um guia de evolução e pode ser ajustado conforme necessidades do projeto.*
