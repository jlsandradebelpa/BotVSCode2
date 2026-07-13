# Atualização do Projeto BotVSCode

*Status: Concluída*

## Objetivo

Atualizar o BotVSCode para que o próprio projeto **BotVSCode** faça parte da lista de projetos disponíveis para execução dos fluxos **Iniciar Trabalho** e **Encerrar Trabalho**.

---

## Alteração Solicitada

Adicionar o projeto abaixo na lista padrão de projetos cadastrados:

```text
Nome:
BotVSCode

Caminho:
C:\Projetos\BotVSCode

Branch padrão:
main

Abrir VS Code:
Sim

Favorito:
Sim
```

---

## Resultado Esperado

Ao iniciar o BotVSCode, o menu de seleção de projetos deverá conter também o próprio projeto.

```
=========================
        BotVSCode
=========================

Selecione o projeto

1 - BotVSCode
2 - intprotheussoc
3 - MemCalcExporter
4 - Prj_TIR
5 - AutomacaoTIR
6 - CBAA_Asfaltos_Empresa

0 - Sair
```

> A ordem será dinâmica conforme a implementação, porém o projeto **BotVSCode** estará sempre disponível na lista.

---

## Requisitos

* Adicionar o cadastro padrão do projeto BotVSCode.
* Utilizar o caminho `C:\Projetos\BotVSCode`.
* Validar se o diretório existe.
* Validar se é um repositório Git.
* Utilizar a branch padrão **main**.
* Permitir sua utilização normalmente nos fluxos:
  * Iniciar Trabalho
  * Encerrar Trabalho

---

## Implementação

### Alterações Realizadas

#### `config/projetos.json`

Adicionada a entrada do projeto BotVSCode na lista de projetos cadastrados:

```json
{
  "nome": "BotVSCode",
  "pasta": "C:\\Projetos\\BotVSCode",
  "branch": "main",
  "linguagem": "Python"
}
```

#### `app/utils.py`

A função `resolve_full_path` foi atualizada para verificar se o caminho armazenado já é absoluto. Quando um caminho absoluto é detectado (como `C:\Projetos\BotVSCode`), ele é retornado diretamente sem tentar combiná-lo com um drive detectado.

Esta alteração é **genérica** — qualquer projeto futuro que utilizar um caminho absoluto será tratado da mesma forma, sem tratamento especial para o BotVSCode.

### Como Funciona

A função `resolve_full_path` agora segue esta lógica:

1. Se o caminho informado for absoluto (ex: `C:\Projetos\BotVSCode`), retorna-o diretamente.
2. Caso contrário, usa a lógica anterior de detectar a unidade (D:, E:) e combinar com o caminho relativo.

---

## Observações

O BotVSCode é tratado exatamente como qualquer outro projeto gerenciado. Não há tratamento especial para ele.

Todas as funcionalidades funcionam da mesma forma:

* Git Fetch
* Git Pull
* Git Status
* Git Commit
* Git Push
* Abertura automática do VS Code

---

## Objetivo da Alteração

O próprio desenvolvimento do BotVSCode passará a utilizar o fluxo que ele automatiza, permitindo validar continuamente a ferramenta durante sua evolução.

Essa alteração foi implementada preservando toda a arquitetura existente, sem modificar o fluxo principal do sistema.

---

## Módulos Envolvidos

- `config/projetos.json`: cadastro do novo projeto
- `app/utils.py`: suporte genérico a caminhos absolutos em `resolve_full_path`

## Critérios de Aceitação

1. Projeto BotVSCode aparece no menu de seleção de projetos.
2. O fluxo "Iniciar Trabalho" funciona com o BotVSCode (fetch, pull, VS Code).
3. O fluxo "Encerrar Trabalho" funciona com o BotVSCode (commit, push).
4. Nenhum tratamento especial foi criado — a solução é genérica para qualquer caminho absoluto.
5. A documentação foi atualizada.
