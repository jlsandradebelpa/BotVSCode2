# Manual de Contribuição — BotVSCode2

## Para: Jean Rocha (`JEAN-ROCHA`)

---

## 1. Repositório

- **URL**: https://github.com/jlsandradebelpa/BotVSCode2
- **Visibilidade**: Público
- **Sua branch**: `jean-rocha/develop`

---

## 2. Primeira configuração

### Clonar o projeto

```bash
git clone -b jean-rocha/develop https://github.com/jlsandradebelpa/BotVSCode2.git
cd BotVSCode2
```

### Criar ambiente virtual e instalar dependências

```bash
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
```

### Executar o projeto

```bash
python app/main.py
```

### Criar atalho na Área de Trabalho

1. Abra o Bloco de Notas e cole o conteúdo abaixo:
   ```bat
   @echo off
   cd /d C:\projetos\BotVSCode2
   .venv\Scripts\python app\main.py
   ```
2. Salve como `BotVSCode2.bat` na Área de Trabalho
3. (Opcional) Clique com botão direito > `Enviar para > Área de Trabalho (criar atalho)` no arquivo `app/main.py` e ajuste o destino para:
   ```
   C:\projetos\BotVSCode2\.venv\Scripts\pythonw.exe C:\projetos\BotVSCode2\app\main.py
   ```

---

## 3. Fluxo de trabalho diário

### Antes de começar — sempre atualizar

```bash
git pull origin jean-rocha/develop
```

### Criar uma alteração

```bash
# Ver o que foi alterado
git status
git diff

# Preparar os arquivos
git add .

# Commit com mensagem clara
git commit -m "Descrição do que foi feito"
```

### Enviar para o GitHub

```bash
git push origin jean-rocha/develop
```

---

## 4. Como contribuir com melhorias

1. Faça suas alterações na branch `jean-rocha/develop`
2. Faça commit e push normalmente
3. Quando quiser que o Jorge revise, abra um **Pull Request**:
   - **Base**: `devjlsa`
   - **Compare**: `jean-rocha/develop`
4. URL para abrir PR diretamente:
   ```
   https://github.com/jlsandradebelpa/BotVSCode2/compare/devjlsa...jean-rocha/develop
   ```
5. No PR, descreva o que foi alterado e por quê
6. Após revisão e aprovação, o Jorge fará o merge

---

## 5. Estrutura do projeto

```
app/                    # Código principal
  main.py               # Ponto de entrada
  ui/                   # Interface gráfica (Flet)
  services/             # Regras de negócio
  chat/                 # Chat integrado
config/                 # Configurações JSON
docs/                   # Documentação
tests/                  # Testes
assets/                 # Recursos visuais
```

---

## 6. Como pedir ajuda ao assistente AI (OpenCode)

Você pode pedir ajuda diretamente no chat do OpenCode para:

- **Criar ou alterar código** — descreva o que quer fazer
- **Gerar documentação** — peça um `ProtheusDOC` ou manual
- **Revisar seu código** — peça uma revisão antes do PR
- **Corrigir bugs** — cole o erro ou descreva o comportamento inesperado
- **Refatorar** — peça para extrair funções, simplificar lógica, melhorar performance
- **Testes** — solicite geração de testes unitários
- **Dúvidas técnicas** — pergunte sobre padrões, bibliotecas, boas práticas

### Exemplos de comandos

> "Crie uma nova funcionalidade de exportar relatório em PDF"
>
> "Revise meu código em app/services/git_service.py"
>
> "Adicione documentação na função X"
>
> "Me ajude a corrigir esse erro: [cole o erro]"

### Lembrete importante

Toda alteração gerada pelo assistente precisa ser **revisada e testada** antes do commit. Você é o responsável pelo que entra no repositório.

---

## 7. Convenções

- **Idioma**: Código em português (mensagens de commit em português também)
- **Branches**: `main` (estável) ← `devjlsa` (desenvolvimento ativo) ← `jean-rocha/develop` (suas contribuições)
- **Nunca** fazer push direto para `main`
- **Commits**: Mensagens curtas e descritivas

---

## 8. Problemas comuns

| Problema | Solução |
|----------|---------|
| `pull` rejeita por conflito | `git pull origin jean-rocha/develop --rebase` |
| Esqueci de criar a branch | `git checkout -b jean-rocha/develop origin/jean-rocha/develop` |
| Commit errado | `git commit --amend -m "mensagem corrigida"` (só se ainda não deu push) |
| Dúvidas | Falar com Jorge ou abrir uma Issue no GitHub |

---

## 9. Referências

- [Fluxo de branches](FLUXO_BRANCHES.md)
- [Arquitetura do projeto](ARQUITETURA.md)
- [README principal](../README.md)
