# Configuração do GitHub — BotVSCode2

## Repositório

- **URL**: https://github.com/jlsandradebelpa/BotVSCode2
- **Visibilidade**: Público
- **Branch padrão**: `main`
- **Labels**: `enhancement`, `documentation`, `testing`, `chore`

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

1. Toda issue nova entra como **Pendente**.
2. Ao iniciar a execução, mover para **Em andamento**.
3. Ao finalizar e validar, mover para **Concluído**.
4. Nenhuma issue deve ficar sem status definido.
5. O quadro (View 2) é o controle visual oficial do andamento.

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

O repositório original `jlsandradebelpa/botvscode` permanece congelado como baseline de referência.
