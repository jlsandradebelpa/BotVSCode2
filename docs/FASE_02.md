# Fase 2 — Interface Gráfica Flet

*Status: Concluída*

## Objetivo

Substituir a interface em terminal por uma interface gráfica moderna utilizando **Flet**, mantendo 100% da lógica existente inalterada.

## Estratégia

- **BotVSCode original** (`C:\projetos\botvscode`) permanece congelado como baseline
- **BotVSCode2** (`C:\projetos\botvscode2`) é o novo projeto com interface gráfica
- Nenhuma regra de negócio foi alterada
- Interface é apenas uma nova camada visual sobre o sistema existente

## Arquitetura

### Camadas

```
UI (Flet) → Services → Core (Regras de Negócio)
```

- **UI**: páginas Flet com componentes visuais
- **Services**: camada intermediária que traduz chamadas da UI para as classes Core
- **Core**: classes originais do BotVSCode (ProjetosManager, GitTools, etc.)

### Services Criados

| Service | Função |
|---------|--------|
| `ProjectService` | CRUD de projetos via ProjetosManager |
| `GitService` | Operações Git via GitTools |
| `GitHubService` | Consulta de Issues via github_tools |
| `HistoricoService` | Registro e listagem de histórico |
| `VSCodeService` | Abrir/fechar VS Code |

## Telas Implementadas

### Início
- Projeto atual (nome, pasta, branch)
- Botões **Iniciar Atividade** e **Encerrar Atividade**
- Status Git (branch, ahead/behind)
- Status VS Code (instalado/não encontrado)
- Última sincronização e última atividade
- Área de mensagens

### Projetos
- Lista de projetos carregada de `%APPDATA%/BotVsCode2/projetos.json`
- Formulário de cadastro/edição
- CRUD completo: adicionar, editar, remover
- Persistência com `json.dump(indent=2, ensure_ascii=False)`

### Atividades
- Tabela com histórico do dia (somente leitura)
- Colunas: #, Hora, Tipo, Descrição

### Configurações
- Placeholder para Fase 3
- Seções: VSCode, Git, GitHub, Tema, Histórico

## Melhorias no Core

### ProjetosManager (projetos.py)
- `save()` — persistir lista em JSON
- `adicionar(projeto)` — adicionar e salvar
- `editar(index, projeto)` — substituir e salvar
- `remover(index)` — remover e salvar
- `existe_nome(nome)` — verificar duplicidade
- `carregar()` — recarregar do arquivo

### Histórico (historico.py)
- `listar(pasta)` — retornar registros do dia como dicionários
- `listar_arquivos(pasta)` — listar arquivos disponíveis

### VS Code (vscode.py)
- `close_vscode(project_path)` — fechar VS Code filtrando por nome da pasta do projeto via `Get-CimInstance` (Windows)

## Fluxo "Iniciar Atividade"

```
1. Validar projeto selecionado
2. Verificar se caminho existe
3. Verificar se é repositório Git
4. Executar Git Fetch
5. Comparar branch local vs remota
6. Se remoto à frente → Git Pull
7. Abrir VS Code (se instalado)
8. Registrar atividade no histórico
9. Atualizar tela com status
```

## Fluxo "Encerrar Atividade"

```
1. Validar projeto selecionado
2. Verificar alterações locais
3. Se sem alterações → Push direto
4. Se com alterações:
   a. Diálogo: confirmar commit?
   b. Diálogo: mensagem do commit
   c. Stage All → Commit → Push
5. Fechar VS Code (se configurado)
6. Registrar atividade no histórico
7. Atualizar tela com status
```

## Aparência

- **Tema**: Dark (indigo seed)
- **Fundo**: `GREY_900`
- **Cards**: `GREY_800` com borda `GREY_700`
- **Componentes**: nativos Flet
- **Responsivo**: layout adaptável

## Repositório GitHub

- **URL**: https://github.com/jlsandradebelpa/BotVSCode2
- **Project**: https://github.com/users/jlsandradebelpa/projects/9
- **Issues**: 7 issues criadas e vinculadas ao projeto

## Commits

```
470018d Fase 2: Interface gráfica Flet + CRUD projetos + serviços
ef7385e Adicionado seletor de pasta no campo Pasta Local
4b3930e Corrigido FilePicker - adicionado ao overlay na inicialização
15e0ccf Removido FilePicker - não suportado nesta versão do Flet
```

## Critérios de Aceitação

1. ✅ Interface gráfica totalmente funcional (Flet)
2. ✅ Tela Início pronta
3. ✅ Tela Projetos pronta (CRUD completo)
4. ✅ Tela Atividades pronta (histórico somente leitura)
5. ✅ Tela Configurações pronta (placeholder)
6. ✅ Cadastro de projetos funcionando
7. ✅ Alteração de projetos funcionando
8. ✅ Leitura do `config/projetos.json` funcionando
9. ✅ Gravação do `config/projetos.json` funcionando
10. ✅ Botão Iniciar Atividade funcionando
11. ✅ Botão Encerrar Atividade funcionando
12. ✅ Histórico funcionando
13. ✅ Todas as funcionalidades atuais reutilizadas
14. ✅ Nenhuma regra de negócio alterada
15. ✅ BotVSCode original permanece intacto
