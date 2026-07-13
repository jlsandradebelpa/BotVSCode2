# Fase 1 — Núcleo

## Objetivo

Entregar a base sólida do projeto: estrutura de diretórios, sistema de configuração, cadastro de projetos e menu interativo.

## Funcionalidades Implementadas

- [x] Estrutura de diretórios completa (`app/`, `config/`, `docs/`, `tests/`, `assets/`).
- [x] Leitura da configuração (`config.json`) com dataclass tipada.
- [x] Cadastro de projetos em `projetos.json`.
- [x] Menu interativo com listagem dos projetos.
- [x] Seleção do projeto pelo usuário.
- [x] Detecção automática da unidade (D: ou E:) quando `workspace_drive = "AUTO"`.
- [x] Exibição dos detalhes do projeto selecionado.
- [x] Saudação personalizada conforme horário.
- [x] Documentação inicial (README, ROADMAP, arquitetura, fases).
- [x] Módulos stub preparados para fases futuras.

## Não Implementado (fases futuras)

- Git Pull / Push (Fase 2).
- Abertura do VS Code (Fase 3).
- Síntese de voz (Fase 4).
- Integração com GitHub (Fase 4).
- Inteligência Artificial (Fase 5).
- Distribuição e atalhos (Fase 6).

## Como Executar

```bash
cd C:\Projetos\botvscode
python app/main.py
```

## Estrutura Criada

```
botvscode/
├── app/
│   ├── __init__.py
│   ├── main.py          # Orquestrador principal
│   ├── menu.py          # Interface de menu
│   ├── config.py        # Leitura da configuração
│   ├── projetos.py      # Gerenciamento de projetos
│   ├── git_tools.py     # Stub para Git
│   ├── vscode.py        # Stub para VS Code
│   ├── speech.py        # Stub para voz
│   └── utils.py         # Utilitários (drive, saudação)
├── config/
│   ├── config.json      # Configuração do ambiente
│   └── projetos.json    # Cadastro de projetos
├── docs/
│   ├── ROADMAP.md
│   ├── FASE_00.md
│   ├── FASE_01.md
│   ├── FASE_02.md
│   ├── ARQUITETURA.md
│   └── PROJECT_GITHUB.md
├── scripts/
│   └── install_shortcuts.ps1
├── tests/
├── assets/
│   ├── audio/
│   └── icons/
├── requirements.txt
├── README.md
├── .gitignore
└── pyproject.toml
```

## Critérios de Aceitação

1. `python app/main.py` exibe o menu corretamente.
2. Os projetos são listados conforme `projetos.json`.
3. A opção 0 encerra o programa.
4. Uma opção válida exibe os detalhes do projeto.
5. Uma opção inválida exibe mensagem de erro e retorna ao menu.
6. A unidade D: ou E: é detectada automaticamente quando a pasta existe.
