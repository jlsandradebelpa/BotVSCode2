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
│  páginas/preferencias.py        │
├─────────────────────────────────┤
│     Services                    │  ← Integração
│  project_service.py             │
│  git_service.py                 │
│  github_service.py              │
│  historico_service.py           │
│  preferences_service.py         │
│  vscode_service.py              │
├─────────────────────────────────┤
│     Core (Regras de Negócio)    │  ← Domínio
│  projetos.py (ProjetosManager)  │
│  git_tools.py (GitTools)        │
│  github_tools.py                │
│  historico.py                   │
│  vscode.py                      │
│  config.py / utils.py           │
│  data_paths.py / app_state.py   │
└─────────────────────────────────┘
```

**Regra fundamental**: A camada UI **nunca** acessa diretamente as classes Core. Toda comunicação passa pelos Services.

## Diagrama de Módulos

```
app/
├── main.py              # Entry point Flet
├── config.py            # Leitura da configuração (Config dataclass)
├── data_paths.py        # Migração e diretórios pessoais em APPDATA
├── app_state.py         # Estado persistente da interface
├── preferences.py       # Persistência das preferências visuais
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
│   ├── preferences_service.py
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
        ├── configuracoes.py
        └── preferencias.py
```

## Responsabilidades

### Core (Regras de Negócio)

#### projetos.py
- Dataclass `Projeto`: `nome`, `pasta`, `branch`, `linguagem`, `github_repo`, `historico_pasta`
- Classe `ProjetosManager`: CRUD completo (`save`, `adicionar`, `editar`, `remover`, `existe_nome`, `carregar`)
- Persistência pessoal em `%APPDATA%/BotVsCode2/projetos.json`
- `config/projetos.default.json` é usado somente na primeira execução

#### git_tools.py
- Classe `GitTools`: encapsula comandos Git via `subprocess`
- Executa subprocessos sem shell e usa `schannel` no Windows
- Oferece fetch com prune, `pull --ff-only`, upstream, conflitos, comparação de commits e staging seletivo

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
| `PreferencesService` | `Preferences` | Tema, cor e fonte persistentes |
| `VSCodeService` | `open_vscode` + `close_vscode` | Controle VS Code |

### UI (Apresentação)

#### app.py (BotVSCode2App)
- Orquestrador principal do Flet
- Cria NavigationBar com 5 abas
- Mantém Iniciar/Encerrar Atividade na barra principal
- Inicia a janela maximizada
- Gerencia página ativa via `_mudar_aba()`
- Barra de mensagens inferior

#### páginas/inicio.py
- Projeto atual (nome, pasta, branch)
- Botões **Iniciar Atividade** e **Encerrar Atividade**
- Status Git e VSCode
- Última sincronização e última atividade

#### páginas/projetos.py
- Lista de projetos carregada de `%APPDATA%/BotVsCode2/projetos.json`
- Formulário de cadastro/edição (Nome, Pasta, Branch, Linguagem, GitHub, Histórico)
- Botões: Novo, Salvar, Remover

#### páginas/atividades.py
- Tabela com histórico do dia (somente leitura)

#### páginas/configuracoes.py
- Informações técnicas de VS Code, Git, GitHub e histórico

#### páginas/preferencias.py
- Tema claro, escuro ou conforme o sistema
- Cor de destaque e fonte
- Persistência em `%APPDATA%/BotVsCode2/preferences.json`

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
4. Executar `git fetch --all --prune`
5. Validar branch configurada, branch atual e upstream
6. Bloquear conflitos ou divergência
7. Se houver alterações locais, listar e permitir abrir sem pull ou cancelar
8. Se o remoto estiver à frente e for seguro, executar `git pull --ff-only`
9. Abrir VS Code e registrar a sessão
```

## Fluxo "Encerrar Atividade"

```
1. Validar projeto selecionado
2. Executar fetch e validar branch/upstream
3. Bloquear conflitos, divergência ou remoto à frente
4. Listar arquivos e exigir seleção explícita
5. Sugerir mensagem de commit e permitir edição
6. Executar `git add` somente nos arquivos selecionados e confirmar o commit
7. Executar novo fetch; bloquear push se o remoto avançou
8. Fazer push, fechar VS Code e registrar a atividade
```

## Decisões de Arquitetura

1. **Flet como framework UI**: moderno, Python puro, dark theme nativo, componentes responsivos
2. **Services como ponte**: UI nunca acessa Core diretamente — isolamento total de responsabilidades
3. **ProjetosManager com CRUD**: métodos `save/adicionar/editar/remover/existe_nome` com persistência imediata
4. **Dados pessoais fora do Git**: JSONs pessoais em APPDATA e padrões versionados no repositório
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
