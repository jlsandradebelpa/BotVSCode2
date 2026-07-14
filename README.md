# BotVSCode2

> Assistente para preparação automática do ambiente de desenvolvimento — Interface Gráfica.

## Descrição

O BotVSCode2 é a evolução do BotVSCode com **interface gráfica moderna** utilizando **Flet**. Automatiza a preparação do ambiente de desenvolvimento: abrir VS Code, git pull/push/commit, registro de atividades e gerenciamento de projetos — tudo por uma interface visual intuitiva.

## Funcionalidades

### Fase 3 — UX, Preferências e Fluxos (atual)
- Interface Flet iniciada maximizada
- Ações **Iniciar/Encerrar Atividade** integradas à barra principal
- Tela **Início**: projeto atual e status em layout expansível
- Tela **Projetos**: CRUD, lista com rolagem e seleção explícita do projeto de trabalho
- Tela **Atividades**: histórico diário em tabela (somente leitura)
- Tela **Configurações**: informações técnicas do ambiente
- Tela **Preferências**: tema, cor de destaque e fonte com persistência em JSON
- Fluxos Git de início e encerramento com validação e mensagens de falha
- Serviços desacoplados (camada Service entre UI e regras de negócio)
- Backward compatible com `config/projetos.json` do BotVSCode original

### Legado (Fase 1 — Núcleo)
- Leitura de configuração (`config.json`)
- Cadastro e listagem de projetos
- Detecção automática de unidade (D: / E:)
- Operações Git (fetch, pull, commit, push, status)
- Abertura automática do VS Code
- Consulta de GitHub Issues
- Registro de histórico diário

## Requisitos

- Python 3.13 ou superior
- Windows
- Git instalado e acessível via PATH
- VS Code com `code` no PATH (opcional)
- Flet 0.85.x

## Instalação

```bash
cd C:\projetos\botvscode2
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

## Uso

```bash
python app/main.py
```

Ou clique no atalho **BotVSCode2** na Área de Trabalho.

## Estrutura do Projeto

```
botvscode2/
├── app/
│   ├── main.py              # Entry point Flet
│   ├── config.py             # Configuração do ambiente
│   ├── preferences.py        # Preferências visuais
│   ├── projetos.py           # ProjetosManager com CRUD
│   ├── menu.py               # Menu terminal (legado)
│   ├── git_tools.py          # Operações Git
│   ├── github_tools.py       # Consulta GitHub Issues
│   ├── historico.py          # Histórico de atividades
│   ├── vscode.py             # Controle do VS Code
│   ├── utils.py              # Utilitários
│   ├── services/             # Camada de serviços
│   │   ├── project_service.py
│   │   ├── git_service.py
│   │   ├── github_service.py
│   │   ├── historico_service.py
│   │   ├── preferences_service.py
│   │   └── vscode_service.py
│   └── ui/                   # Interface gráfica Flet
│       ├── app.py            # Orquestrador
│       ├── tema.py           # Tema escuro
│       ├── helpers.py        # Utilitários de UI
│       ├── componentes/
│       └── paginas/
│           ├── inicio.py
│           ├── projetos.py
│           ├── atividades.py
│           ├── configuracoes.py
│           └── preferencias.py
├── config/                   # Configurações JSON
├── docs/                     # Documentação
├── logs/                     # Logs
└── pyproject.toml
```

## Documentação

- [Roadmap](docs/ROADMAP.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Configuração do GitHub](docs/PROJECT_GITHUB.md)
- [Fase 2 — Interface Gráfica](docs/FASE_02.md)
- [Fase 3 — UX, Preferências e Fluxos](docs/FASE_03_UX_FLUXOS.md)

## Licença

MIT
