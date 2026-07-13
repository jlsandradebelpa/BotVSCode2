# Configuração do GitHub — BotVSCode / JA WorkStart

## Repositório

- **URL**: https://github.com/jlsandradebelpa/botvscode
- **Visibilidade**: Público
- **Branch padrão**: `main`
- **Labels**: `enhancement`, `documentation`, `testing`, `chore`

## GitHub Project

- **Nome**: BotVSCode - JA WorkStart
- **URL**: https://github.com/users/jlsandradebelpa/projects/6
- **Visibilidade**: Privado
- **Vinculado ao repositório**: `jlsandradebelpa/botvscode`

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

1. Toda issue nova entra como **Pendente**.
2. Ao iniciar a execução, mover para **Em andamento**.
3. Ao finalizar e validar, mover para **Concluído**.
4. Nenhuma issue deve ficar sem status definido.
5. O quadro (View 2) é o controle visual oficial do andamento.

### Issues iniciais (15)

| # | Título | Label |
|---|--------|-------|
| 1 | Criar estrutura base do projeto | enhancement |
| 2 | Criar README inicial | documentation |
| 3 | Criar ROADMAP do projeto | documentation |
| 4 | Implementar cadastro de projetos | enhancement |
| 5 | Implementar leitura de configuração | enhancement |
| 6 | Criar menu inicial | enhancement |
| 7 | Detectar unidade de projetos automaticamente | enhancement |
| 8 | Exibir projeto selecionado | enhancement |
| 9 | Preparar módulo Git | enhancement |
| 10 | Preparar módulo VS Code | enhancement |
| 11 | Preparar módulo de voz | enhancement |
| 12 | Criar documentação da Fase 1 | documentation |
| 13 | Criar documentação da arquitetura | documentation |
| 14 | Criar primeiro teste automatizado | testing |
| 15 | Criar commit inicial organizado | chore |

## Primeiro commit

```
204d9e4 feat: estrutura inicial do BotVSCode — Fase 1
```

Enviado para `origin/main` em 07/07/2026.
