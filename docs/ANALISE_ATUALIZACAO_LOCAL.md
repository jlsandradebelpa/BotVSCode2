# Análise dos problemas de atualização local do BotVsCode2

**Data da análise:** 15/07/2026

**Projeto:** BotVsCode2

**Branch de desenvolvimento:** `devjlsa`

**Objetivo:** registrar as causas dos problemas recorrentes de atualização, as evidências encontradas e as soluções recomendadas para estudo antes da implementação.

## 1. Resumo executivo

O repositório remoto e a branch `devjlsa` estavam corretos. O problema ocorreu no computador local porque o BotVsCode2 permite alterar arquivos de configuração que continuam sendo controlados pelo Git.

No incidente analisado, o arquivo `config/projetos.json` possuía alterações locais e, ao mesmo tempo, havia seis commits novos no repositório remoto. O BotVsCode2 detectou qualquer alteração não commitada como impedimento para executar o `git pull`. Por isso, a atualização não foi aplicada automaticamente.

O mesmo problema pode voltar a acontecer com `config/preferences.json`, pois ele também é controlado pelo Git e pode ser alterado pela interface do programa.

A causa principal, portanto, não foi falha no GitHub, na autenticação ou na branch remota. Foi a mistura de dois tipos de dados no mesmo arquivo:

- configuração padrão do projeto, que deve ser versionada;
- configuração pessoal e operacional da máquina, que não deveria bloquear atualizações do sistema.

## 2. Evidências do incidente

Na verificação realizada em 15/07/2026, foi constatado:

- branch local: `devjlsa`;
- branch remota: `origin/devjlsa`;
- situação inicial: branch local seis commits atrás da remota;
- arquivo alterado localmente: `config/projetos.json`;
- o repositório remoto também possuía alterações nesse arquivo;
- a rotina de início de atividade bloqueava o `pull` ao encontrar alterações locais;
- depois de preservar a configuração local e limpar o estado do Git, o `pull` foi executado em modo fast-forward;
- a branch local passou a ficar sincronizada com `origin/devjlsa`;
- os seis testes unitários existentes passaram;
- a compilação dos arquivos Python também passou.

Foi criado um backup da configuração local antes da atualização:

`C:\Users\JLSAndrade\AppData\Local\Temp\BotVsCode2-projetos-20260715-204936.json`

## 3. Alterações locais encontradas em projetos.json

Comparando a configuração local com a versão remota, foram encontradas diferenças nas branches configuradas para quatro projetos:

| Projeto | Branch no remoto | Branch na configuração local |
|---|---|---|
| MemCalcExplorer | `main` | `devjlsa` |
| Prj_TIR | `main` | `devjlsa` |
| OpenCodeSessionExplorer | `master` | `devjlsa` |
| candidato_cbaa | `master` | `devjlsa` |

Essas diferenças podem ser intencionais, mas mostram por que uma configuração pessoal não deve compartilhar o mesmo arquivo que a configuração oficial distribuída pelo Git.

## 4. Problemas confirmados e melhores soluções

### 4.1. Configurações pessoais controladas pelo Git

**Problema confirmado**

Os arquivos abaixo são alterados durante o uso normal da aplicação e também são versionados:

- `config/projetos.json`;
- `config/preferences.json`.

Quando o usuário muda projetos, branches, aparência ou outras preferências, o repositório fica com alterações locais. Isso interfere no processo de atualização.

**Melhor solução**

Separar configuração padrão de configuração pessoal:

- manter no Git somente arquivos de exemplo ou valores padrão;
- salvar dados pessoais fora do repositório;
- carregar os padrões e aplicar as preferências locais por cima deles.

Estrutura sugerida:

```text
BotVsCode2/
  config/
    projetos.default.json       controlado pelo Git
    preferences.default.json    controlado pelo Git

%APPDATA%/BotVsCode2/
  projetos.json                 configuração pessoal
  preferences.json              preferências pessoais
```

Salvar os arquivos em `%APPDATA%\BotVsCode2` é a opção mais segura, pois elimina completamente a possibilidade de serem adicionados ao repositório por engano.

### 4.2. Atualização bloqueada por qualquer arquivo modificado

**Problema confirmado**

A rotina atual verifica se o repositório está sujo. Se qualquer arquivo possuir alteração não commitada, o `pull` não é executado. Essa proteção evita perda de trabalho, mas não diferencia código-fonte de configuração local.

**Melhor solução**

Depois da separação das configurações, manter a proteção para alterações reais de código. O fluxo recomendado é:

1. executar `git fetch`;
2. identificar a branch atual e seu upstream;
3. informar quantos commits existem à frente e atrás;
4. listar os arquivos locais modificados;
5. permitir atualização automática somente quando for segura;
6. se houver alterações de código, pedir decisão ao usuário;
7. criar backup antes de qualquer migração de configuração.

Não é recomendável executar automaticamente `git reset`, descartar arquivos ou forçar o `pull`.

### 4.3. Branch configurada não é validada contra a branch real

**Problema confirmado**

O campo `branch` da configuração do projeto é exibido pela interface, porém as operações Git acontecem sobre a branch que estiver realmente selecionada no repositório. Assim, a configuração pode dizer `devjlsa`, enquanto o diretório está em `main` ou `master`.

**Melhor solução**

Antes de iniciar uma atividade, comparar:

- branch configurada no BotVsCode2;
- branch atualmente selecionada no repositório local;
- branch upstream vinculada;
- existência da branch no remoto.

Se houver diferença, o sistema deve avisar claramente e oferecer a troca de branch. A troca não deve acontecer silenciosamente quando existirem alterações locais.

### 4.4. Encerramento de atividade adiciona todos os arquivos

**Problema confirmado**

A implementação atual usa o equivalente a `git add -A`. Isso adiciona todos os arquivos novos, modificados e removidos, inclusive um arquivo criado por engano ou uma configuração pessoal versionada.

**Melhor solução**

Antes do commit:

- mostrar a lista de arquivos que serão incluídos;
- permitir confirmar ou cancelar;
- futuramente, permitir selecionar arquivos individualmente;
- garantir que configurações pessoais estejam fora do Git;
- alertar sobre arquivos potencialmente sensíveis ou muito grandes.

Para uma primeira correção, a confirmação explícita da lista já reduz bastante o risco.

### 4.5. Erro intermitente de certificado SSL no Windows

**Problema confirmado**

Durante as verificações foi observado o erro intermitente:

```text
SSL peer certificate or SSH remote key was not OK
```

O serviço Git usado pela aplicação não define explicitamente o backend de certificados do Windows.

**Melhor solução**

Executar os comandos Git usados pelo BotVsCode2 com o backend `schannel`, aproveitando o repositório de certificados do Windows, por exemplo por variável de ambiente ou configuração controlada pelo serviço Git.

Nunca deve ser usada a solução de desabilitar a validação SSL (`sslVerify=false`), pois ela reduz a segurança da conexão.

### 4.6. Testes não reproduzem o cenário real de atualização

**Problema confirmado**

Os testes atuais usam simulações e não reproduzem toda a combinação que causou o incidente:

- repositório local atrás do remoto;
- arquivo de configuração local modificado;
- o mesmo arquivo alterado no remoto;
- necessidade de backup e migração;
- divergência entre branch configurada e branch selecionada.

**Melhor solução**

Criar testes de integração com repositórios Git temporários reais. Os cenários mínimos devem incluir:

1. repositório limpo e atrás do remoto;
2. alteração local apenas em configuração pessoal;
3. alteração local em código-fonte;
4. conflito entre alteração local e remota;
5. branch configurada diferente da branch atual;
6. falha de rede ou certificado;
7. backup e migração de configuração antiga.

## 5. Itens que não foram a causa principal

Para evitar diagnósticos incorretos, os seguintes pontos foram verificados:

- o GitHub remoto possuía os commits esperados;
- a branch `devjlsa` remota estava correta;
- a autenticação já estava funcional;
- as mensagens da interface permanecem visíveis e não foram a causa do bloqueio;
- a ausência de reinício automático da aplicação não causou o `pull` bloqueado.

Um mecanismo externo de atualização e reinício pode ser útil no futuro, mas deve ser tratado como melhoria de arquitetura, não como correção da causa deste incidente.

## 6. Arquitetura recomendada

O desenho recomendado separa aplicação, configuração oficial e dados pessoais:

```text
Repositório Git
  código da aplicação
  configurações padrão
  documentação
  testes

Diretório do usuário (%APPDATA%\BotVsCode2)
  projetos configurados localmente
  preferências visuais
  estado da interface
  logs e backups locais
```

No carregamento:

1. o BotVsCode2 lê os valores padrão do repositório;
2. lê a configuração pessoal, se existir;
3. combina os dados, dando prioridade aos valores pessoais;
4. valida caminhos e branches;
5. nunca grava alterações pessoais nos arquivos padrão.

## 7. Plano de correção recomendado

### Fase 1 — Separar configurações

- criar arquivos padrão versionados;
- criar diretório de dados em `%APPDATA%\BotVsCode2`;
- implementar leitura combinada de padrão e configuração local;
- migrar os arquivos antigos com backup;
- incluir testes de migração.

Esta é a fase de maior prioridade porque elimina a causa recorrente.

### Fase 2 — Tornar a atualização segura

- validar branch configurada, branch atual e upstream;
- melhorar o diagnóstico de commits à frente e atrás;
- manter bloqueio para alterações reais de código;
- apresentar arquivos modificados e orientação objetiva;
- impedir operações destrutivas automáticas.

### Fase 3 — Tornar o encerramento seguro

- exibir arquivos antes do `git add`;
- pedir confirmação antes do commit;
- permitir seleção de arquivos em uma evolução posterior;
- verificar se há arquivos sensíveis ou configurações locais.

### Fase 4 — Confiabilidade e suporte

- configurar `schannel` nas operações Git do Windows;
- criar testes de integração com repositórios temporários;
- registrar logs técnicos úteis, sem armazenar credenciais;
- apresentar mensagens de erro com causa e orientação.

## 8. Migração sem perder a configuração atual

A implementação deve preservar os dados existentes:

1. detectar `config/projetos.json` e `config/preferences.json` antigos;
2. criar backup com data e hora;
3. copiar os valores pessoais para `%APPDATA%\BotVsCode2`;
4. validar se os novos arquivos podem ser lidos;
5. somente depois restaurar os arquivos padrão do repositório;
6. manter o backup para recuperação manual;
7. informar ao usuário o local do backup.

Em caso de qualquer falha, a migração deve parar sem apagar o arquivo original.

## 9. Critérios de aceite

A correção será considerada concluída quando:

- alterar projetos ou preferências não modificar o repositório Git;
- iniciar atividade atualizar um repositório limpo que esteja atrás do remoto;
- alterações de código local nunca forem descartadas automaticamente;
- a interface mostrar branch configurada, branch atual e remoto de forma coerente;
- o encerramento mostrar exatamente quais arquivos entrarão no commit;
- configurações pessoais não forem incluídas em commits;
- a migração criar backup e preservar os dados atuais;
- erros de certificado não forem contornados desabilitando SSL;
- testes de integração cobrirem os principais cenários Git;
- após dois ciclos completos de iniciar e encerrar atividades, o problema não voltar a ocorrer.

## 10. Decisões para estudo

Antes da implementação, devem ser confirmadas estas decisões:

1. **Local da configuração pessoal:** recomenda-se `%APPDATA%\BotVsCode2`, em vez de um arquivo ignorado dentro do repositório.
2. **Atualização com alterações de código:** recomenda-se bloquear o `pull`, listar os arquivos e pedir que o usuário resolva ou registre as mudanças.
3. **Atualização automática:** recomenda-se sempre informar o que será feito e criar backup quando houver migração.
4. **Seleção no encerramento:** inicialmente pode ser usada uma confirmação da lista completa; depois, seleção individual de arquivos.
5. **Branch oficial de cada projeto:** deve vir da configuração padrão, mas uma escolha pessoal temporária pode ser mantida na configuração local.

## 11. Prioridade sugerida

| Prioridade | Correção | Motivo |
|---|---|---|
| Crítica | Separar configuração pessoal do Git | Elimina a causa recorrente do bloqueio |
| Alta | Validar branch real, configurada e upstream | Evita atualizar ou publicar na branch errada |
| Alta | Exibir arquivos antes de `git add -A` | Evita commits acidentais |
| Média | Configurar `schannel` no Windows | Reduz falhas intermitentes de certificado |
| Média | Criar testes Git de integração | Impede regressões do fluxo de atualização |
| Baixa | Atualizador externo com reinício | Melhoria futura, não é a causa atual |

## 12. Conclusão

O comportamento observado por duas noites é coerente com a implementação atual: o próprio uso do BotVsCode2 pode modificar arquivos controlados pelo Git, e qualquer modificação local impede a atualização automática.

A correção estrutural é separar definitivamente os dados pessoais dos arquivos versionados. Depois disso, a validação de branches, o encerramento seletivo, o uso seguro de certificados no Windows e os testes de integração tornam o fluxo mais previsível e confiável.

Este documento registra a análise e as recomendações. Nenhuma das correções descritas foi implementada por meio deste documento.
