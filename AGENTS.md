# Regras do projeto para agentes de IA

Estas regras são obrigatórias para qualquer agente de IA que trabalhe neste repositório. Elas definem como preparar, executar, registrar e concluir o trabalho; não substituem o contexto do projeto nem a documentação técnica.

## Fontes de verdade

- `README.md`: apresentação e porta de entrada para pessoas.
- `PROJECT_CONTEXT.md`: contexto mínimo e estável para IA.
- `AGENTS.md`: regras obrigatórias de trabalho para agentes.
- `docs/`: documentação técnica consolidada.
- `config/*.default.json`: valores iniciais versionados, nunca dados pessoais ativos.
- `tests/`: testes e critérios automatizados de validação.
- GitHub Issues e Project 9 `BotVSCode2`: trabalho atual, pendências e histórico operacional.

Em caso de conflito, prevalece a regra mais específica do projeto. Não replique em `README.md` ou `PROJECT_CONTEXT.md` detalhes que pertencem a `docs/`, às issues ou a este arquivo.

## Preparação obrigatória

Antes de implementar, corrigir, refatorar, revisar ou produzir documentação relevante:

1. Leia `README.md`.
2. Leia `PROJECT_CONTEXT.md`.
3. Leia `AGENTS.md` por completo.
4. Verifique o repositório local, a branch atual, o upstream e alterações preexistentes.
5. Confirme o remoto GitHub configurado.
6. Consulte o GitHub Project 9 e as issues abertas.
7. Identifique a issue correspondente à solicitação.
8. Leia somente a documentação técnica necessária ao escopo.

Preserve alterações do usuário e arquivos não relacionados. Não inicie a implementação sem concluir essa verificação.

## Vínculo obrigatório com issue

Toda funcionalidade, correção, refatoração relevante, mudança de comportamento, decisão técnica ou documentação estrutural deve estar vinculada a uma issue.

Se não houver issue correspondente:

1. interrompa a implementação;
2. proponha ou crie a issue quando houver autorização;
3. adicione-a ao Project 9 `BotVSCode2`;
4. defina o status inicial como **Pendente**;
5. aguarde aprovação quando a criação automática não estiver autorizada.

Não amplie o escopo além do que a issue e o usuário autorizaram.

## Fluxo no GitHub Project

O fluxo oficial é:

```text
Pendente -> Em andamento -> Concluído
```

Ao iniciar:

1. confirme que a issue está no Project 9;
2. mova-a de **Pendente** para **Em andamento**;
3. registre comentário de início quando houver contexto relevante.

Durante o trabalho:

- registre decisões, bloqueios e evidências relevantes na issue;
- mantenha o escopo limitado aos arquivos e comportamentos autorizados;
- atualize `docs/` quando uma decisão técnica for consolidada;
- não registre segredos nem dados pessoais desnecessários.

Ao finalizar:

1. execute as verificações aplicáveis;
2. confirme exatamente quais arquivos foram alterados;
3. atualize a documentação técnica necessária;
4. registre comentário final com resumo, verificações e commit, quando houver;
5. mova a issue para **Concluído**;
6. feche a issue somente quando o escopo estiver atendido e houver autorização.

Quando o usuário exigir revisão antes de commit, push ou fechamento, apresente o resultado e aguarde aprovação.

## Arquitetura e dados pessoais

- Preserve a separação `UI -> Services -> Core` descrita em `docs/ARQUITETURA.md`.
- A UI Flet e o chat devem usar os Services; não duplique regras Git em novos caminhos de interface.
- Dados pessoais ficam em `%APPDATA%\BotVsCode2`.
- O repositório controla apenas `config/projetos.default.json` e `config/preferences.default.json`.
- Nunca volte a versionar `config/projetos.json`, `config/preferences.json`, estado da interface, sessões, logs ou backups pessoais.
- Migrações devem criar backup, validar o resultado e preservar o original em qualquer falha.

## Regras para operações Git do aplicativo

- Validar branch configurada, branch atual e upstream antes de pull ou push.
- Usar somente `git pull --ff-only` quando a atualização for segura.
- Executar fetch antes de comparar commits e novamente antes do push.
- Nunca trocar branch automaticamente.
- Nunca adicionar todos os arquivos sem seleção e confirmação do usuário.
- Nunca executar automaticamente `git reset --hard`, `git clean -fd` ou `git push --force`.
- Nunca descartar, sobrescrever ou ocultar alterações locais.
- No Windows, usar `schannel` sem desabilitar a validação SSL.

## Regras de desenvolvimento Python/Flet

- Manter compatibilidade com Python 3.13 e Flet 0.85.x definidos no projeto.
- Preservar tipagem, dataclasses e injeção de dependências já adotadas.
- Evitar regras de negócio em controles ou callbacks da UI.
- Não remover funcionalidades consolidadas sem justificativa registrada na issue.
- Não introduzir dependência nova sem necessidade, validação e documentação.
- Mensagens ao usuário devem explicar causa, bloqueio e próxima ação segura.

## Verificação obrigatória

Execute, conforme o escopo:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m compileall -q app tests
git diff --check
git status --short --branch
```

Mudanças em Git devem incluir testes com repositórios temporários reais quando o comportamento não puder ser comprovado apenas com mocks.

## Branches e publicação

- `devjlsa` é a branch de desenvolvimento e validação.
- `main` é a branch oficial e estável.
- A promoção ocorre por Pull Request de `devjlsa` para `main` após validação.
- Não faça push direto, force-push ou exclusão da `main`.
- Não faça commit, push, fechamento de issue ou mudança de status quando o usuário exigir aprovação prévia.

## Segurança e limites

- Nunca registre tokens, chaves, senhas, credenciais ou dados pessoais em código, documentação, issues, comentários, logs ou evidências.
- Não enfraqueça certificados, autenticação ou outras proteções como solução.
- Não altere arquivos fora do escopo da issue.
- Não misture correções independentes no mesmo commit.
- Se o acesso impedir atualizar Issue ou Project, informe a limitação e não simule o estado esperado.
