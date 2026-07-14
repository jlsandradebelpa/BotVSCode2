# Fase 3 — UX, Preferências e Fluxos de Atividade

*Status: Implementada e validada*

## Objetivo

Evoluir a interface Flet do BotVSCode2 para aproveitar melhor a tela, manter um
projeto explicitamente selecionado durante a sessão e tornar confiáveis os
fluxos de início e encerramento de atividade.

## Escopo e critérios de aceite

### 1. Janela maximizada

- A aplicação inicia maximizada no Windows.
- O usuário ainda pode restaurar e redimensionar a janela.

### 2. Ações na barra principal

- **Iniciar Atividade** e **Encerrar Atividade** ficam na mesma barra e paleta
  visual das opções Início, Projetos, Atividades, Configurações e Preferências.
- Acionar uma atividade não troca a página que estava selecionada.

### 3. Remover saudação

- A saudação por horário deixa de aparecer na tela Início.
- Mensagens finais não incluem saudação.

### 4. Reaproveitar espaço da tela Início

- O card exclusivo dos botões deixa de existir.
- Projeto Atual e Status ocupam a área central em colunas expansíveis.
- O layout continua utilizável quando a janela for redimensionada.

### 5. Rolagem na lista de projetos

- A lista possui rolagem vertical sempre visível.
- Todos os projetos permanecem alcançáveis sem deslocar o formulário.

### 6. Seleção explícita de projeto

- Clicar em um item carrega seus dados para consulta/edição.
- O botão **Selecionar** confirma o projeto de trabalho.
- O projeto selecionado permanece em memória durante a sessão.
- A tela Início mostra imediatamente o projeto confirmado.

### 7. Aba Preferências

- Nova aba **Preferências** na navegação principal.
- Permite alterar tema (claro, escuro ou sistema), cor de destaque e fonte.
- Preferências são gravadas em `config/preferences.json` e reaplicadas ao abrir.
- Existe uma ação para restaurar os padrões.

### 8. Fluxos Iniciar e Encerrar Atividade

#### Iniciar

1. Exigir projeto explicitamente selecionado.
2. Validar caminho e repositório Git.
3. Executar fetch e consultar ahead/behind.
4. Executar pull quando o remoto estiver à frente.
5. Não registrar sucesso se pull ou abertura do VS Code falhar.
6. Abrir o VS Code, registrar histórico e atualizar o status.

#### Encerrar

1. Exigir projeto explicitamente selecionado.
2. Validar caminho e repositório Git.
3. Sem alterações: executar push e registrar o resultado.
4. Com alterações: confirmar, exigir mensagem, stage, commit e push.
5. Manter mensagens de erro visíveis e atualizar o status após o fluxo.

## Arquitetura

```text
NavigationBar / páginas Flet
        ↓
Services
        ↓
Core + persistência JSON
```

- `app/ui/app.py`: janela, navegação e ações globais.
- `app/ui/paginas/inicio.py`: resumo do projeto e fluxos de atividade.
- `app/ui/paginas/projetos.py`: lista rolável e seleção explícita.
- `app/ui/paginas/preferencias.py`: edição das preferências visuais.
- `app/preferences.py`: modelo e persistência das preferências.
- `app/services/preferences_service.py`: acesso da UI à persistência.
- `config/preferences.json`: valores escolhidos pelo usuário.

## Fora do escopo

- Alterar o BotVSCode original.
- Trocar o framework Flet.
- Criar instalador ou executável distribuível.
- Alterar credenciais Git/GitHub pela tela de preferências.

## Validação

- Compilação de todos os módulos Python.
- Testes automatizados para persistência e seleção.
- Teste visual da abertura maximizada, navegação e rolagem.
- Testes dos fluxos Git usando repositório temporário ou mocks, sem publicar
  alterações reais durante a validação.

### Resultado

- 6 testes automatizados executados com sucesso.
- Janela real aberta pelo atalho e confirmada como maximizada pelo Windows.
- Processo Flet confirmado como responsivo, com título `BotVSCode2`.
- Arquivo de histórico direcionado para `historico_pasta`, sem sujar o repositório.

## Rastreabilidade

- Épica: [#16 — Fase 3: UX, Preferências e Fluxos](https://github.com/jlsandradebelpa/BotVSCode2/issues/16)
- [#8 — Abrir a aplicação maximizada](https://github.com/jlsandradebelpa/BotVSCode2/issues/8)
- [#9 — Integrar Iniciar e Encerrar à barra principal](https://github.com/jlsandradebelpa/BotVSCode2/issues/9)
- [#10 — Remover saudação](https://github.com/jlsandradebelpa/BotVSCode2/issues/10)
- [#11 — Reaproveitar o espaço da tela Início](https://github.com/jlsandradebelpa/BotVSCode2/issues/11)
- [#12 — Adicionar rolagem à lista de projetos](https://github.com/jlsandradebelpa/BotVSCode2/issues/12)
- [#13 — Adicionar seleção explícita de projeto](https://github.com/jlsandradebelpa/BotVSCode2/issues/13)
- [#14 — Criar aba Preferências](https://github.com/jlsandradebelpa/BotVSCode2/issues/14)
- [#15 — Corrigir fluxos Iniciar e Encerrar](https://github.com/jlsandradebelpa/BotVSCode2/issues/15)
