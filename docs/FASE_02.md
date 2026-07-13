# Fase 2 — Ciclo de Sincronização

*Status: Concluída*

## Objetivo

Implementar o ciclo completo de sincronização dos projetos entre ambientes de desenvolvimento (empresa ↔ casa), utilizando o GitHub como ponto central de sincronização.

## Visão Geral

O BotVSCode passa a operar em dois modos principais:

### Iniciar Trabalho

Prepara o ambiente antes do início do desenvolvimento:

```
Selecionar Projeto
        ↓
Localizar Projeto
        ↓
Validar repositório Git
        ↓
Executar Git Fetch
        ↓
Comparar branch local e remota
        ↓
Verificar alterações locais
        ↓
Informar situação ao usuário
        ↓
Perguntar se deseja atualizar
        ↓
Executar Git Pull
        ↓
Abrir Visual Studio Code
```

### Encerrar Trabalho

Garante que todas as alterações sejam enviadas ao GitHub:

```
Selecionar Projeto
        ↓
Git Status
        ↓
Existem alterações?
        ↓
  Sim → Mostrar arquivos modificados
         Solicitar mensagem do Commit
         Executar Git Commit
         Executar Git Push
         Confirmar sincronização
        ↓
  Não → Push (garantir sincronização)
        ↓
Encerrar
```

## Funcionalidades Implementadas

- [x] Menu principal com dois modos: Iniciar Trabalho / Encerrar Trabalho
- [x] Seleção de projeto antes de cada fluxo
- [x] Validação de repositório Git
- [x] Git Fetch (atualizar referências remotas)
- [x] Comparação de branch local vs remota (ahead/behind)
- [x] Detecção de alterações locais não commitadas
- [x] Git Pull com confirmação do usuário
- [x] Git Commit com mensagem personalizada
- [x] Git Push com feedback de resultado
- [x] Abertura automática do VS Code
- [x] Tratamento de erros (Git não instalado, diretório não encontrado)

## Módulos Envolvidos

- `git_tools.py`: classe `GitTools` com métodos `is_git_repo()`, `fetch()`, `pull()`, `commit()`, `push()`, `status()`, `get_branch_status()`, `has_uncommitted_changes()`, `get_current_branch()`
- `vscode.py`: funções `open_vscode()` e `is_vscode_installed()`
- `menu.py`: fluxo completo dos dois modos de operação

## Fluxo Diário

### Manhã (Empresa)

```text
BotVSCode → Iniciar Trabalho → Git Pull → VS Code
```

### Tarde (Empresa)

```text
BotVSCode → Encerrar Trabalho → Commit → Push
```

### Noite (Casa)

```text
BotVSCode → Iniciar Trabalho → Git Pull → VS Code
```

### Fim da noite (Casa)

```text
BotVSCode → Encerrar Trabalho → Commit → Push
```

Na manhã seguinte, ao iniciar na empresa, todas as alterações feitas em casa estarão disponíveis automaticamente.

## Dependências Externas

- Git instalado e acessível via PATH
- VS Code instalado e com `code` no PATH (opcional para o fluxo)

## Critérios de Aceitação

1. Menu exibe "Iniciar Trabalho" e "Encerrar Trabalho" como opções principais.
2. Ao selecionar "Iniciar Trabalho", o fluxo executa fetch, verifica status e oferece pull.
3. Ao selecionar "Encerrar Trabalho", detecta alterações e oferece commit+push.
4. VS Code abre automaticamente após pull (se instalado).
5. Mensagens de erro claras para Git não instalado, diretório inválido, etc.
6. Commit exige mensagem não vazia do usuário.
7. Push informa sucesso ou falha.
