# Diretriz de Arquitetura — Integração com Automação RPO Protheus

*Status: Planejada (não implementada)*

## Objetivo

Definir como ocorrerá a futura integração entre o BotVSCode e o projeto **Automação RPO Protheus**.

---

## Princípios

O BotVSCode e o Automação RPO Protheus são projetos independentes.

Cada projeto possui:

- repositório Git próprio;
- ciclo de desenvolvimento próprio;
- documentação própria;
- roadmap próprio;
- versionamento próprio.

O BotVSCode deverá funcionar integralmente sem depender da existência do Automação RPO Protheus.

---

## Escopo da Integração

A integração terá caráter exclusivamente informativo.

O BotVSCode poderá consultar e exibir um resumo do estado do projeto relacionado à Automação RPO Protheus, sem executar qualquer operação de compilação, publicação ou alteração de dados.

Exemplo de informações:

```text
Projeto: intprotheussoc

Situação da Publicação

Última compilação:
05/07/2026 17:42

Última publicação:
06/07/2026 08:15

Status:
Produção Atualizada
```

As informações deverão ser resumidas e destinadas apenas ao acompanhamento do desenvolvedor.

---

## Restrições

O BotVSCode **NÃO** deverá:

- iniciar compilações;
- publicar RPO;
- alterar solicitações de publicação;
- aprovar implantações;
- modificar informações do Automação RPO Protheus;
- substituir funcionalidades da ferramenta utilizada pela gerente de projetos.

Toda a gestão de compilação e publicação continuará sendo responsabilidade exclusiva do projeto Automação RPO Protheus.

---

## Momento da Implementação

Esta integração **NÃO** faz parte do escopo inicial do BotVSCode.

Ela somente deverá ser iniciada quando o BotVSCode estiver considerado funcionalmente completo (versão 1.0 estável), com todos os recursos principais implementados e validados.

Até esse momento, nenhuma atividade de desenvolvimento relacionada à integração deverá ser priorizada.

---

## Objetivo Futuro

Quando implementada, a integração terá como finalidade fornecer ao desenvolvedor uma visão resumida do ciclo de implantação, facilitando o acompanhamento do andamento das customizações após sua entrega para a gerente de projetos.

Essa integração será apenas consultiva e não criará dependência entre os dois projetos.
