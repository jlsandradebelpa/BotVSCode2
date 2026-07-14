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

## Configuração dos bots

O BotVSCode e o BotVSCode2 devem cadastrar o projeto `BotVsCode2` com:

```json
{
  "nome": "BotVsCode2",
  "pasta": "C:\\projetos\\BotVsCode2",
  "branch": "devjlsa",
  "github_repo": "jlsandradebelpa/BotVSCode2"
}
```

Os módulos MCP usam a propriedade `branch_padrao` com o valor `devjlsa`. A
branch `main` não deve ser usada pelos fluxos automáticos de commit e push.
