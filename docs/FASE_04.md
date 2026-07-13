# Atualização — Tarefas Pendentes por Projeto

*Status: Concluída*

## Objetivo

Adicionar ao BotVSCode a capacidade de listar as tarefas pendentes relacionadas ao projeto selecionado após a abertura do VS Code.

Essa funcionalidade ajuda o usuário a iniciar o desenvolvimento já sabendo quais atividades estão pendentes para aquele projeto.

---

## Fluxo Ajustado — Iniciar Trabalho

Novo fluxo:

```text
Selecionar Projeto
↓
Localizar Projeto
↓
Validar repositório Git
↓
Executar Git Fetch
↓
Comparar repositório local e remoto
↓
Verificar alterações locais
↓
Perguntar se deseja atualizar
↓
Executar Git Pull
↓
Abrir Visual Studio Code
↓
Listar tarefas pendentes do projeto
```

---

## Origem das Tarefas Pendentes

A implementação considera, nesta ordem:

1. **GitHub Issues** do repositório vinculado ao projeto (implementado nesta fase).
2. GitHub Project vinculado ao projeto (futuro).
3. Arquivo local (futuro, caso exista necessidade).

---

## Exemplo de Exibição

```text
Projeto: BotVSCode

Tarefas pendentes:

#16 - Criar histórico diário de atividades
#17 - Listar tarefas pendentes ao iniciar trabalho
#18 - Integrar informações com Automação RPO Protheus

Status:
Pendente
```

---

## Regras

- Listar apenas tarefas pendentes ou em andamento.
- Não listar tarefas concluídas.
- A listagem é apenas informativa.
- O BotVSCode não altera status automaticamente nesta fase.
- Caso não existam tarefas pendentes, exibir:

```text
Nenhuma tarefa pendente encontrada para este projeto.
```

---

## Integração com Histórico de Atividades

Ao iniciar o trabalho, o BotVSCode registra automaticamente no histórico diário:

```text
001 | 08:03 | Git | Projeto iniciado e sincronizado: BotVSCode
002 | 08:04 | GitHub Issues | Listadas 3 tarefas pendentes de jlsandradebelpa/botvscode
```

---

## Implementação

### Alterações Realizadas

#### `app/projetos.py`

Adicionado campo opcional `github_repo` ao dataclass `Projeto`:

```python
@dataclass
class Projeto:
    nome: str
    pasta: str
    branch: str
    linguagem: str
    github_repo: Optional[str] = None
```

#### `app/github_tools.py` (novo)

Módulo para consulta de issues do GitHub via API REST (usando apenas biblioteca padrão `urllib`):

- `list_open_issues(repo)` — lista issues abertas do repositório, filtrando pull requests.

#### `app/historico.py` (novo)

Módulo para registro de histórico de atividades diárias:

- `registrar(tipo, descricao)` — adiciona entrada numerada no arquivo `historico_atividades_YYYY-MM-DD.txt`.

#### `config/projetos.json`

Adicionado campo `github_repo` aos projetos que possuem repositório GitHub:

```json
{
  "nome": "BotVSCode",
  "pasta": "C:\\Projetos\\BotVSCode",
  "branch": "main",
  "linguagem": "Python",
  "github_repo": "jlsandradebelpa/botvscode"
}
```

#### `app/menu.py`

- Importados `list_open_issues` e `registrar_historico`.
- Adicionado método `_list_pending_tasks()`.
- Chamada a listagem ao final do fluxo "Iniciar Trabalho", após abrir o VS Code.
- Registro de entrada no histórico ao iniciar o trabalho.

---

## Módulos Envolvidos

| Módulo | Tipo | Descrição |
|--------|------|-----------|
| `app/projetos.py` | Alterado | Campo `github_repo` opcional |
| `app/github_tools.py` | Novo | Consulta de GitHub Issues |
| `app/historico.py` | Novo | Registro de histórico diário |
| `app/menu.py` | Alterado | Fluxo com listagem de tarefas |
| `config/projetos.json` | Alterado | Campo `github_repo` adicionado |

---

## Critérios de Aceitação

1. Após o fluxo "Iniciar Trabalho", o VS Code abre normalmente.
2. Em seguida, o BotVSCode lista as tarefas pendentes do projeto.
3. A consulta usa o repositório GitHub configurado no projeto.
4. Tarefas concluídas não aparecem.
5. Caso não existam tarefas pendentes, o sistema informa claramente.
6. O fluxo de produção não é executado pelo BotVSCode.
7. A integração com Automação RPO Protheus permanece apenas informativa e de apoio.
