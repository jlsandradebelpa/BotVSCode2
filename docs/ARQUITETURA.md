# Arquitetura do BotVSCode2

## Visão Geral

O BotVSCode2 segue uma arquitetura em **três camadas**:

```
┌─────────────────────────────────┐
│       UI (Flet)                 │  ← Apresentação
│  páginas/inicio.py              │
│  páginas/projetos.py            │
│  páginas/atividades.py          │
│  páginas/configuracoes.py       │
├─────────────────────────────────┤
│     Services                    │  ← Integração
│  project_service.py             │
│  git_service.py                 │
│  github_service.py              │
│  historico_service.py           │
│  vscode_service.py              │
├─────────────────────────────────┤
│     Core (Regras de Negócio)    │  ← Domínio
│  projetos.py (ProjetosManager)  │
│  git_tools.py (GitTools)        │
│  github_tools.py                │
│  historico.py                   │
│  vscode.py                      │
│  config.py / utils.py           │
└─────────────────────────────────┘
```

**Regra fundamental**: A camada UI **nunca** acessa diretamente as classes Core. Toda comunicação passa pelos Services.

## Diagrama de Módulos

```
app/
├── main.py              # Entry point Flet
├── config.py            # Leitura da configuração (Config dataclass)
├── projetos.py          # ProjetosManager + Projeto dataclass (CRUD)
├── menu.py              # Menu terminal (legado — mantido como referência)
├── git_tools.py         # Operações Git (GitTools)
├── github_tools.py      # Consulta GitHub Issues
├── historico.py         # Histórico de atividades (+ listar)
├── vscode.py            # Controle VS Code (+ close_vscode)
├── utils.py             # Utilitários (saudacao, resolve_full_path)
├── services/            # Camada de serviços
│   ├── project_service.py
│   ├── git_service.py
│   ├── github_service.py
│   ├── historico_service.py
│   └── vscode_service.py
└── ui/                  # Interface gráfica Flet
    ├── app.py           # Orquestrador principal (BotVSCode2App)
    ├── tema.py          # Tema escuro
    ├── helpers.py       # Utilitários de UI
    ├── componentes/
    └── paginas/
        ├── inicio.py
        ├── projetos.py
        ├── atividades.py
        └── configuracoes.py
```

## Responsabilidades

### Core (Regras de Negócio)

#### projetos.py
- Dataclass `Projeto`: `nome`, `pasta`, `branch`, `linguagem`, `github_repo`, `historico_pasta`
- Classe `ProjetosManager`: CRUD completo (`save`, `adicionar`, `editar`, `remover`, `existe_nome`, `carregar`)
- Persistência em `config/projetos.json` com `json.dump(indent=2, ensure_ascii=False)`

#### git_tools.py
- Classe `GitTools`: encapsula comandos Git via `subprocess`
- Métodos: `is_git_repo()`, `fetch()`, `pull()`, `push()`, `commit()`, `stage_all()`, `status_short()`, `has_uncommitted_changes()`, `get_current_branch()`, `get_branch_status()`

#### github_tools.py
- `list_open_issues(repo)`: consulta GitHub Issues via CLI `gh` ou API REST

#### historico.py
- `registrar(tipo, descricao, pasta)`: adiciona entrada no arquivo do dia
- `listar(pasta)`: retorna lista de registros do dia
- `listar_arquivos(pasta)`: lista arquivos de histórico disponíveis

#### vscode.py
- `open_vscode(project_path)`: abre VS Code no diretório
- `close_vscode(project_path)`: fecha VS Code via taskkill
- `is_vscode_installed()`: verifica se `code` está no PATH

### Services (Camada de Integração)

Cada Service é um **wrapper fino** que:
- Expõe API simplificada para a UI
- Traduz exceções em tuplas `(bool, mensagem)`
- Não contém regras de negócio

| Service | Classe Core | Função |
|---------|-------------|--------|
| `ProjectService` | `ProjetosManager` | CRUD com validação |
| `GitService` | `GitTools` + `resolve_full_path` | Operações Git |
| `GitHubService` | `list_open_issues` | Consulta Issues |
| `HistoricoService` | `registrar` + `listar` | Histórico |
| `VSCodeService` | `open_vscode` + `close_vscode` | Controle VS Code |

### UI (Apresentação)

#### app.py (BotVSCode2App)
- Orquestrador principal do Flet
- Cria NavigationBar com 4 abas
- Gerencia página ativa via `_mudar_aba()`
- Barra de mensagens inferior

#### páginas/inicio.py
- Projeto atual (nome, pasta, branch)
- Botões **Iniciar Atividade** e **Encerrar Atividade**
- Status Git e VSCode
- Última sincronização e última atividade

#### páginas/projetos.py
- Lista de projetos (carregada de `projetos.json`)
- Formulário de cadastro/edição (Nome, Pasta, Branch, Linguagem, GitHub, Histórico)
- Botões: Novo, Salvar, Remover

#### páginas/atividades.py
- Tabela com histórico do dia (somente leitura)

#### páginas/configuracoes.py
- Placeholder para Fase 3 (VSCode, Git, GitHub, Tema, Histórico)

## Fluxo de Dados

```
Botão na UI
    ↓
Evento Flet → método na página
    ↓
Service (ex: GitService.pull)
    ↓
Classe Core (ex: GitTools.pull)
    ↓
Resultado → UI atualizada
```

## Fluxo "Iniciar Atividade"

```
1. Validar projeto selecionado
2. Verificar se caminho existe
3. Verificar se é repositório Git
4. Executar Git Fetch
5. Comparar branch local vs remota
6. Se remoto à frente → Git Pull
7. Abrir VS Code (se instalado)
8. Registrar atividade no histórico
9. Atualizar tela com status
```

## Fluxo "Encerrar Atividade"

```
1. Validar projeto selecionado
2. Verificar alterações locais
3. Se sem alterações → Push direto
4. Se com alterações:
   a. Perguntar se deseja commitar
   b. Solicitar mensagem do commit
   c. Stage All → Commit → Push
5. Fechar VS Code (se configurado)
6. Registrar atividade no histórico
7. Atualizar tela com status
```

## Decisões de Arquitetura

1. **Flet como framework UI**: moderno, Python puro, dark theme nativo, componentes responsivos
2. **Services como ponte**: UI nunca acessa Core diretamente — isolamento total de responsabilidades
3. **ProjetosManager com CRUD**: métodos `save/adicionar/editar/remover/existe_nome` com persistência imediata
4. **Config e Projetos em JSON**: compatibilidade total com BotVSCode original
5. **Dataclasses para modelos**: tipagem e sem boilerplate
6. **Git via subprocess**: sem dependências externas de bibliotecas Git
7. **menu.py mantido**: referência técnica do fluxo original, não utilizado pela UI

## Padrões Utilizados

- **Camadas (Layered Architecture)**: UI → Services → Core
- **Método Factory**: `Config.load()`, `ProjetosManager.carregar()`
- **Façade**: Services como fachada para classes Core
- **Composição**: páginas recebem Services por injeção de dependência
- **Dataclass**: modelos de dados tipados

## Extensibilidade

Para adicionar uma nova funcionalidade na Fase 3:

1. Implementar/estender a classe Core (regra de negócio)
2. Criar/estender o Service correspondente
3. Criar a página Flet ou adicionar o componente
4. Conectar no `app.py`
