# Diretriz — Pasta do Histórico de Atividades

*Status: Planejada (não implementada)*

> Os exemplos de cadastro preservam o contexto original. A branch operacional
> deve ser lida da configuração atual; não use `main` automaticamente.

## Objetivo

Permitir que o usuário defina onde os arquivos de histórico de atividades
(`historico_atividades_YYYY-MM-DD.txt`) serão armazenados, podendo ser
uma pasta global para todos os projetos ou uma pasta específica por projeto.

---

## Regras de Precedência

A definição da pasta de histórico segue esta ordem:

1. **`config.json` → `historico_pasta`** (global) — se definido, todos os
   projetos usam essa mesma pasta. O valor deve ser um caminho absoluto.

2. **`projetos.json` → `historico_pasta`** (por projeto) — usado somente
   quando o campo global em `config.json` não está definido. Caminho absoluto.

3. **Padrão (fallback)** — quando nenhum dos dois é definido, o histórico
   continua sendo salvo na raiz do BotVSCode, mantendo o comportamento
   original.

> Se ambos os campos forem definidos, **o global (`config.json`) prevalece**
> sobre o por projeto.

---

## Arquivos Afetados

### `config/config.json`

Adicionado campo opcional `historico_pasta` (string, caminho absoluto):

```json
{
  "workspace_drive": "AUTO",
  "usuario": "Jorge",
  "empresa": "CBAA",
  "historico_pasta": "C:\\Historicos"
}
```

Quando definido, **todos** os projetos registram o histórico nessa pasta.

### `config/projetos.json`

Adicionado campo opcional `historico_pasta` por projeto (string):

```json
{
  "nome": "BotVSCode",
  "pasta": "C:\\Projetos\\BotVSCode",
  "branch": "main",
  "linguagem": "Python",
  "github_repo": "jlsandradebelpa/botvscode",
  "historico_pasta": "C:\\Historicos\\BotVSCode"
}
```

Usado **apenas** quando `config.json` não define `historico_pasta`.

---

## Módulos Envolvidos

| Módulo | Tipo | Descrição |
|--------|------|-----------|
| `app/config.py` | Alterado | Campo `historico_pasta` no dataclass `Config` |
| `app/projetos.py` | Alterado | Campo `historico_pasta` no dataclass `Projeto` |
| `app/historico.py` | Alterado | Aceita caminho customizado via parâmetro |
| `app/menu.py` | Alterado | Passa o caminho resolvido ao `registrar_historico` |
| `app/main.py` | Alterado | Passa `Config` e `Projeto` ao `Menu` |
| `config/config.json` | Alterado | Campo `historico_pasta` adicionado |
| `config/projetos.json` | Alterado | Campo `historico_pasta` adicionado |

---

## Critérios de Aceitação

1. Se `config.json` define `historico_pasta`, todos os projetos salvam
   o histórico nessa pasta.
2. Se `config.json` não define e `projetos.json` define por projeto,
   cada projeto salva na sua pasta.
3. Se nenhum define, o comportamento padrão é mantido (raiz do BotVSCode).
4. O diretório é criado automaticamente se não existir.
5. O parâmetro é opcional e não quebra projetos existentes.
