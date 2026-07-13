# BotVSCode

> Assistente para preparação automática do ambiente de desenvolvimento.

## Descrição

O BotVSCode é um assistente de produtividade que automatiza a preparação do ambiente de desenvolvimento no Visual Studio Code. Com um menu interativo no terminal, você seleciona o projeto desejado e o BotVSCode cuida do resto: abrir o VS Code, executar git pull, verificar status e muito mais.

## Funcionalidades

### Fase 1 — Núcleo (atual)
- Menu interativo com listagem de projetos
- Seleção de projeto por número
- Detecção automática da unidade de disco (D: ou E:)
- Exibição de detalhes do projeto selecionado

### Futuras
- Git pull / status (Fase 2)
- Abertura automática do VS Code (Fase 3)
- Síntese de voz, múltiplos projetos, GitHub (Fase 4)
- Sugestões com IA (Fase 5)
- Distribuição com atalhos e instalador (Fase 6)

## Requisitos

- Python 3.13 ou superior
- Windows (devido à detecção de unidades D: e E:)

## Instalação

```bash
cd C:\Projetos\botvscode
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

## Uso

```bash
python app/main.py
```

## Estrutura do Projeto

```
botvscode/
├── app/           # Código fonte
├── config/        # Arquivos de configuração
├── docs/          # Documentação
├── scripts/       # Scripts de instalação e utilitários
├── tests/         # Testes automatizados
├── assets/        # Recursos (áudio, ícones)
├── requirements.txt
├── pyproject.toml
├── README.md
└── .gitignore
```

## Documentação

- [Roadmap](docs/ROADMAP.md)
- [Arquitetura](docs/ARQUITETURA.md)
- [Configuração do GitHub](docs/PROJECT_GITHUB.md)
- [Fase 0 — Infraestrutura](docs/FASE_00.md)
- [Fase 1 — Núcleo](docs/FASE_01.md)
- [Fase 2 — Git e VS Code](docs/FASE_02.md)

## Licença

MIT
