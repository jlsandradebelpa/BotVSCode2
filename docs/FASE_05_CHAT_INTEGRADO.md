# Sprint 03 — Chat Integrado (Bot Jorge)

**Versão:** 1.0  
**Status:** Planejada  
**Autor da Especificação:** ChatGPT (Orquestrador do Projeto)

---

## Objetivo

Implementar a primeira versão do Chat Integrado do BotVSCode2.

O objetivo desta Sprint **não é implementar IA**. Nesta etapa será criada apenas a infraestrutura do chat e do sistema de comandos.

---

## Conceito

O BotVSCode2 deixará de depender exclusivamente de menus e botões. Será criado um Chat Integrado semelhante aos assistentes modernos. O usuário conversará com o Bot através de comandos iniciados por `/`.

No futuro o Chat aceitará linguagem natural, porém esta funcionalidade **não faz parte desta Sprint**.

---

## Interface

### Botão do Chat

Adicionar um botão flutuante na interface principal.

Características:
- Sempre visível
- Discreto
- Não ocupar espaço da interface
- Permanecer acima das demais telas (overlay)

**Posição sugerida:** canto inferior direito.

O botão deverá possuir animação ao passar o mouse (hover).

### Avatar

O botão deverá utilizar inicialmente um avatar padrão. Posteriormente será substituído pela foto do usuário (Bot Jorge). Nesta Sprint, deixar preparado para troca simples da imagem.

```
assets/avatar_bot.png   → avatar padrão (inicial)
assets/avatar_jorge.png → foto do usuário (futuro)
```

### Janela do Chat

Ao clicar no botão, abrir um painel de conversa. O painel **não** abrirá uma nova janela. Ele deverá deslizar, expandir e recolher sem fechar a aplicação.

**Layout:**

```
+-----------------------------------------+
| Projeto Atual                           |
| ...                                     |
| ...                                     |
|                    ( Avatar )           |
|                ___________________      |
|                Chat BotVSCode2         |
|                >                       |
|                ___________________      |
+-----------------------------------------+
```

### Campo de Digitação

Criar um campo de entrada com prefixo `>`. Ao pressionar ENTER, executar o comando.

---

## Sistema de Comandos

Todos os comandos iniciarão por `/`. Ao digitar `/`, abrir automaticamente uma lista de comandos disponíveis.

### Primeiros comandos (escopo inicial)

| Comando | Descrição |
|---------|-----------|
| `/selecionar-projeto` | Mostra lista de projetos cadastrados; guarda o selecionado no contexto |
| `/pendencias` | Lista pendências do projeto atual (usa contexto da sessão) |
| `/encerrar-projeto` | Encerra o projeto atual |
| `/encerrar-atividades` | Encerra atividades do dia |
| `/atualizar-documentacao-local` | Atualiza documentação local |
| `/ajuda` | Exibe ajuda dos comandos |

Nenhum outro comando será implementado nesta Sprint.

### Auto Complete

Enquanto o usuário digita `/at`, mostrar sugestão `/atualizar-documentacao-local`.

---

## Selecionar Projeto

Ao executar `/selecionar-projeto`, mostrar lista dos projetos cadastrados. Após seleção, guardar o projeto atual no contexto da sessão.

---

## Contexto

O Chat deverá manter memória apenas durante a sessão. Exemplo: ao selecionar projeto com `/selecionar-projeto`, o comando `/pendencias` não deverá perguntar novamente o projeto.

---

## Estrutura sugerida

Criar um novo módulo `app/chat/` com a seguinte estrutura:

```
chat/
    chat_service.py       # Serviço principal do chat
    command_registry.py   # Registry de comandos (evita cadeia de IFs)
    command_parser.py     # Parse de entrada e autocomplete
    command_context.py    # Contexto da sessão (projeto atual, etc.)
    command_executor.py   # Execução dos comandos
```

### Registry de comandos

Não utilizar diversos IFs. Criar um Registry que mapeia comandos para classes:

```
/pendencias           → PendenciasCommand
/ajuda                → HelpCommand
```

Preparar para crescimento futuro.

---

## Serviços

Toda regra de negócio deverá permanecer na camada `services/`. A UI apenas chama os serviços. O módulo `chat/` deve seguir o mesmo padrão, utilizando os Services existentes (`ProjectService`, `GitService`, `HistoricoService`, etc.).

---

## Fora do Escopo

Não implementar:
- ChatGPT / OpenAI / Gemini / Ollama
- MCP
- GitHub automático
- Linguagem Natural
- Voz / Microfone
- Reconhecimento de imagem

---

## Critérios de Aceite

Será considerado concluído quando:
- [ ] Botão do chat estiver funcionando (flutuante, canto inferior direito)
- [ ] Painel abrir e fechar corretamente (deslizar/expandir/recolher)
- [ ] Campo de digitação funcionando com prefixo `>`
- [ ] Menu `/` funcionando (lista de comandos ao digitar `/`)
- [ ] Autocomplete funcionando
- [ ] Comandos registrados no Registry (6 comandos)
- [ ] Contexto do projeto funcionando entre comandos

---

## Arquitetura

O novo módulo `app/chat/` se integrará à arquitetura existente em três camadas:

```
app/
    chat/                         # NOVO: módulo do chat
        chat_service.py           # Fachada do chat para a UI
        command_registry.py       # Registry de comandos
        command_parser.py         # Parse e autocomplete
        command_context.py        # Contexto de sessão
        command_executor.py       # Execução de comandos
    services/                     # EXISTENTE: camada de serviços
        project_service.py
        git_service.py
        historico_service.py
        ...
    ui/
        app.py                    # ALTERADO: adicionar botão flutuante e painel
        paginas/                  # EXISTENTE: páginas (inalteradas)
```

### Fluxo de Execução

```
Usuário digita "/pendencias" + ENTER
    ↓
command_parser.py → identifica comando
    ↓
command_registry.py → resolve para PendenciasCommand
    ↓
command_context.py → obtém projeto atual da sessão
    ↓
command_executor.py → executa PendenciasCommand
    ↓
    usa services/ → ProjectService, GitHubService, etc.
    ↓
chat_service.py → retorna resultado para a UI
```

---

## Observação Importante

O BotVSCode2 continuará sendo um assistente para organização do desenvolvimento. Ele **não executará** processos de compilação ou produção.

---

## Próxima Sprint (prevista)

- Linguagem Natural
- Histórico da conversa
- Memória do projeto
- Integração com GitHub
- Integração com MCP
- Integração com Automação RPO Protheus (somente consulta)

---

## Diretriz

Durante esta Sprint:
- Não alterar funcionalidades existentes
- Não refatorar módulos sem necessidade
- Não criar novas telas
- Não alterar a arquitetura atual
- Implementar somente o escopo descrito neste documento
- Atualizar o `STATUS_PROJETO.md` ao final da implementação
