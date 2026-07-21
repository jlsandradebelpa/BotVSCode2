# Contexto do projeto — BotVSCode2

Este arquivo fornece o contexto mínimo e estável para uma IA começar a trabalhar no projeto sem depender do histórico de conversas. Ele não substitui o `README.md`, as regras de `AGENTS.md`, a documentação técnica em `docs/` nem o controle operacional no GitHub.

## Identidade

- Projeto: assistente de produtividade para preparar e encerrar sessões de desenvolvimento.
- Interface: aplicação desktop em Python com Flet.
- Repositório oficial: `jlsandradebelpa/BotVSCode2`.
- Branch de desenvolvimento: `devjlsa`.
- Branch oficial: `main`.
- Controle do trabalho: GitHub Issues e Project 9 `BotVSCode2`.
- Documentação técnica oficial: diretório `docs/`.

## Modelo mental

O usuário seleciona explicitamente um projeto. A interface consulta os Services, que validam caminhos e Git por meio do Core. Somente operações seguras são executadas; decisões com risco de perda, conflito ou mudança de branch permanecem com o usuário.

```text
Interface Flet e chat
        |
        v
Services do aplicativo
        |
        v
Core: projetos, Git, histórico e VS Code
        |
        +--> Repositórios locais e GitHub
        |
        +--> Dados pessoais em APPDATA
```

O BotVsCode2 é um assistente de produtividade, não um cliente Git completo.

## Princípios estáveis

- Proteger alterações locais e nunca tomar decisões destrutivas automaticamente.
- Validar branch configurada, branch local, upstream e situação remota.
- Atualizar somente por fast-forward quando for seguro.
- Exigir seleção explícita dos arquivos antes de commit.
- Buscar novamente o remoto antes do push.
- Manter dados pessoais fora do repositório Git.
- Manter UI, Services e Core separados.
- Registrar toda alteração relevante em issue e no Project 9 antes de implementar.
- Não armazenar credenciais, tokens, senhas ou dados pessoais desnecessários.

## Dados versionados e dados pessoais

O repositório contém os valores iniciais:

```text
config/projetos.default.json
config/preferences.default.json
```

Os dados ativos pertencem ao usuário e ficam fora do Git:

```text
%APPDATA%/BotVsCode2/
  projetos.json
  preferences.json
  state.json
  logs/
  backup/
  sessions/
```

Na primeira execução, a aplicação migra arquivos legados com backup, validação e rollback. Arquivos pessoais nunca devem voltar a ser versionados.

## Fluxo Iniciar Atividade

```text
Selecionar projeto
        |
        v
Validar caminho e repositório
        |
        v
Fetch com prune
        |
        v
Validar branch, upstream, conflitos e commits
        |
        v
Pull --ff-only quando seguro
        |
        v
Abrir VS Code e registrar sessão
```

Alterações locais impedem o pull. Branch incorreta, upstream ausente, divergência e conflito bloqueiam o fluxo com diagnóstico explícito.

## Fluxo Encerrar Atividade

```text
Fetch e validação remota
        |
        v
Listar e selecionar arquivos
        |
        v
Confirmar mensagem e commit
        |
        v
Novo fetch
        |
        v
Push somente se o remoto não avançou
```

## Separação das fontes de verdade

- `README.md`: apresentação e uso do projeto.
- `PROJECT_CONTEXT.md`: contexto mínimo e estável para IA.
- `AGENTS.md`: regras obrigatórias de trabalho e governança.
- `docs/ARQUITETURA.md`: arquitetura detalhada.
- `docs/PROJECT_GITHUB.md`: repositório, Project e fluxo operacional.
- `docs/FLUXO_BRANCHES.md`: branches e promoção para produção.
- `docs/PLANO_OFICIAL_ESTABILIZACAO_BOTVSCODE2.md`: plano estrutural vigente da versão 2.x.
- `docs/RELATORIO_ESTABILIZACAO_2026-07-15.md`: evidências da estabilização executada.
- `tests/`: comportamento automatizado e cenários Git.
- GitHub Issues e Project 9: trabalho atual, pendências e decisões em andamento.

Não use este arquivo para diário, incidentes temporários, resultados pontuais de testes, credenciais ou detalhes já consolidados em documento específico.

## Roteiro para uma IA

Antes de analisar ou alterar o projeto:

1. Leia `README.md`.
2. Leia `AGENTS.md` por completo.
3. Consulte a issue relacionada e confirme seu status no Project 9.
4. Abra somente os documentos relevantes ao escopo.
5. Inspecione código e testes antes de propor mudanças.
6. Preserve alterações preexistentes.
7. Trabalhe apenas na branch e no escopo autorizados.

Para estado atual, pendências ou decisões ainda não consolidadas, consulte sempre o GitHub. Não trate conversas antigas, resumos de sessão ou arquivos pessoais como fonte técnica vigente.
