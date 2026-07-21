# Configuração do GitHub — BotVSCode2

## Repositório

- **URL**: https://github.com/jlsandradebelpa/BotVSCode2
- **Visibilidade**: Público
- **Branch padrão**: `main`
- **Labels de trabalho principais**: `bug`, `documentation`, `enhancement`,
  `workflow`, `ui-ux`, `preferences`, `fase-3`

## Política de branches

- `main` é a branch oficial, protegida e representa a versão de produção.
- `devjlsa` recebe commits e pushes durante desenvolvimento e testes.
- A promoção para produção ocorre somente por Pull Request de `devjlsa` para
  `main`.
- Push direto, force-push e exclusão da `main` são bloqueados no GitHub.
- O BotVSCode e o BotVSCode2 registram este projeto com a branch operacional
  `devjlsa`.
- As configurações operacionais também usam `devjlsa` para BotVSCode,
  ImpProtheusSOC e CBAA Asfaltos.

Detalhes: [Fluxo de branches e promoção](FLUXO_BRANCHES.md).

## GitHub Project

- **Nome**: BotVSCode2
- **URL**: https://github.com/users/jlsandradebelpa/projects/9
- **Visibilidade**: Privado
- **Vinculado ao repositório**: `jlsandradebelpa/BotVSCode2`

### Views

| View | Nome | Layout | Agrupamento |
|------|------|--------|-------------|
| View 1 | Lista de tarefas | Tabela | — |
| View 2 | Quadro | Board | Status |

### Status (campo único de seleção)

| Opção | Cor | Descrição |
|-------|-----|-----------|
| Pendente | Cinza | Tarefa ainda não iniciada |
| Em andamento | Azul | Tarefa em execução |
| Concluído | Verde | Tarefa finalizada e validada |

### Regras de fluxo

1. Toda funcionalidade, correção, refatoração relevante, mudança de
   comportamento, decisão técnica ou documentação estrutural deve possuir uma
   issue antes da implementação.
2. Toda issue nova entra como **Pendente**.
3. Ao iniciar a execução, mover para **Em andamento**.
4. Ao finalizar e validar, mover para **Concluído**.
5. Nenhuma issue deve ficar sem status definido.
6. O quadro (View 2) é o controle visual oficial do andamento.
7. Agentes de IA devem cumprir também o `AGENTS.md` da raiz do repositório.

### Issues da Fase 2

| # | Título | Label |
|---|--------|-------|
| 1 | Criar interface gráfica com Flet - Tela Início | enhancement |
| 2 | Criar interface gráfica com Flet - Tela Projetos | enhancement |
| 3 | Criar interface gráfica com Flet - Tela Atividades | enhancement |
| 4 | Criar interface gráfica com Flet - Tela Configurações | enhancement |
| 5 | Implementar CRUD completo no ProjetosManager | enhancement |
| 6 | Criar camada de Services para isolamento da interface | enhancement |
| 7 | Estender Histórico com função de listagem | enhancement |

## Commits

```
470018d Fase 2: Interface gráfica Flet + CRUD projetos + serviços
ef7385e Adicionado seletor de pasta no campo Pasta Local
4b3930e Corrigido FilePicker - adicionado ao overlay na inicialização
15e0ccf Removido FilePicker - não suportado nesta versão do Flet
```

## Projeto Original

O repositório original `jlsandradebelpa/botvscode` permanece como aplicação de
terminal e também adota `devjlsa` para desenvolvimento. Ele não deve ser tratado
como congelado.
