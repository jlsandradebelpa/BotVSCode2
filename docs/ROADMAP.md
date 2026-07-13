# Roadmap — BotVSCode2

## Fase 2 — Interface Gráfica Flet *(Concluída)*

- [x] Cópia integral do BotVSCode original (baseline congelada)
- [x] Repositório GitHub (`jlsandradebelpa/BotVSCode2`)
- [x] GitHub Project com Board (BotVSCode2)
- [x] 7 issues iniciais
- [x] Atalho na Área de Trabalho
- [x] **Tela Início**: projeto atual, status Git/VSCode, botões Iniciar/Encerrar
- [x] **Tela Projetos**: CRUD completo (lista + formulário)
- [x] **Tela Atividades**: histórico diário em tabela (somente leitura)
- [x] **Tela Configurações**: placeholder para Fase 3
- [x] **ProjetosManager**: CRUD completo (`save`, `adicionar`, `editar`, `remover`, `existe_nome`)
- [x] **Camada Services**: 5 services desacoplados (Project, Git, GitHub, Historico, VSCode)
- [x] **Histórico**: funções `listar()` e `listar_arquivos()`
- [x] **VSCode**: função `close_vscode()`
- [x] **Tema escuro** com componentes Flet nativos
- [x] Persistência em `config/projetos.json` com `json.dump(indent=2, ensure_ascii=False)`
- [x] Nenhuma regra de negócio alterada
- [x] BotVSCode original intacto

## Fase 3 — Assistente IA *(Prevista)*

- [ ] Integração com IA (OpenAI, Gemini, Claude)
- [ ] Chatbot embutido na interface
- [ ] Automação RPO Protheus
- [ ] MCP Server
- [ ] LangChain / RAG
- [ ] Sugestão inteligente de projetos

## Fase 4 — Distribuição *(Prevista)*

- [ ] Instalador do sistema
- [ ] Empacotamento (PyInstaller)

---

*Este roadmap é um guia de evolução e pode ser ajustado conforme necessidades do projeto.*
