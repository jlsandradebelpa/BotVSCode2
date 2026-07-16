# Fluxo de branches e promoção

## Objetivo

Separar o trabalho diário da versão oficial do BotVSCode2.

## Branches

| Branch | Finalidade |
|---|---|
| `devjlsa` | Desenvolvimento, commits, push e validação das atualizações |
| `main` | Versão oficial e estável usada em produção |

## Regras

1. Iniciar e encerrar atividades do BotVSCode2 na branch `devjlsa`.
2. Testar e validar as alterações antes da promoção.
3. Abrir Pull Request de `devjlsa` para `main`.
4. Resolver as conversas do Pull Request e confirmar os testes.
5. Mesclar em `main` somente quando a atualização puder entrar em produção.
6. Não executar push direto, force-push ou exclusão da branch `main`.

## Configuração operacional dos bots

| Projeto | Branch operacional |
|---|---|
| `ImpProtheusSOC` | `devjlsa` |
| `CBAA_Asfaltos_Empresa` | `devjlsa` |
| `BotVSCode` | `devjlsa` |
| `BotVsCode2` | `devjlsa` |

O arquivo versionado `config/projetos.default.json` fornece a matriz inicial.
As escolhas pessoais ficam em `%APPDATA%\BotVsCode2\projetos.json`, fora do Git.
A tela Início apresenta a branch configurada no cadastro e as operações Git
validam também a branch real e o upstream do repositório.

`candidato_cbaa` permanece fora deste fluxo enquanto não houver clone local
validado nesta estação.
