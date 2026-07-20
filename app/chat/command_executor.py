from __future__ import annotations

import subprocess
from typing import Callable, Optional

from projetos import Projeto
from services.git_service import GitService
from services.github_service import GitHubService
from services.historico_service import HistoricoService
from services.project_service import ProjectService
from services.vscode_service import VSCodeService
from chat.command_context import CommandContext


class CommandExecutor:
    def __init__(
        self,
        project_service: ProjectService,
        git_service: GitService,
        github_service: GitHubService,
        historico_service: HistoricoService,
        vscode_service: VSCodeService,
        context: CommandContext,
        on_projeto_selecionado: Optional[Callable[[Optional[Projeto]], None]] = None,
    ) -> None:
        self._project_service = project_service
        self._git_service = git_service
        self._github_service = github_service
        self._historico_service = historico_service
        self._vscode_service = vscode_service
        self._context = context
        self._on_projeto_selecionado = on_projeto_selecionado

    def _validar_git(self, projeto: Projeto) -> tuple[bool, str, dict]:
        ok, output = self._git_service.fetch(projeto.pasta)
        if not ok:
            return False, f"Falha no fetch: {output}", {}

        branch = self._git_service.get_current_branch(projeto.pasta)
        upstream = self._git_service.get_upstream(projeto.pasta)
        details = (
            f"Configurada: {projeto.branch or '---'} | "
            f"Atual: {branch or '---'} | Upstream: {upstream or '---'}"
        )
        if branch != projeto.branch:
            return False, f"Operação bloqueada: branch incorreta. {details}", {}
        if not upstream:
            return False, f"Operação bloqueada: branch sem upstream. {details}", {}
        if upstream.split("/", 1)[-1] != branch:
            return False, f"Operação bloqueada: upstream incompatível. {details}", {}
        if self._git_service.has_conflicts(projeto.pasta):
            return False, "Operação bloqueada: existem conflitos Git não resolvidos.", {}

        status = self._git_service.get_branch_status(projeto.pasta)
        try:
            ahead = int(status.get("ahead", "?"))
            behind = int(status.get("behind", "?"))
        except (TypeError, ValueError):
            return False, "Operação bloqueada: não foi possível comparar os commits.", {}
        if ahead > 0 and behind > 0:
            return (
                False,
                f"Operação bloqueada: branch divergente (à frente {ahead}, atrás {behind}).",
                status,
            )
        return True, "", status

    def selecionar_projeto(self, args: str) -> str:
        projetos = self._project_service.projetos
        if not projetos:
            return "Nenhum projeto cadastrado."

        self._context.awaiting_selection = True
        lines = ["Projetos disponíveis:\n"]
        for i, p in enumerate(projetos, 1):
            lines.append(f"{i}. {p.nome}")
        lines.append("\nDigite o número do projeto desejado.")
        return "\n".join(lines)

    def _selecionar_por_indice(self, indice: int) -> str:
        projeto = self._project_service.get_by_index(indice)
        if not projeto:
            return "Índice inválido."
        self._context.current_project = projeto
        if self._on_projeto_selecionado:
            self._on_projeto_selecionado(projeto)
        return f"Projeto selecionado: {projeto.nome}"

    def pendencias(self, args: str) -> str:
        projeto = self._context.current_project
        if not projeto:
            return "Nenhum projeto selecionado. Use /selecionar-projeto primeiro."
        if not projeto.github_repo:
            return (
                f"Projeto '{projeto.nome}' não possui repositório GitHub "
                "configurado no cadastro."
            )
        issues = self._github_service.listar_issues(projeto.github_repo)
        if issues is None:
            return "Não foi possível consultar o GitHub. Verifique sua conexão."
        if not issues:
            return f"Nenhuma tarefa pendente encontrada para {projeto.nome}."
        lines = [f"Tarefas pendentes ({len(issues)}):\n"]
        for issue in issues:
            numero = issue.get("number", "?")
            titulo = issue.get("title", "Sem título")
            lines.append(f"#{numero} - {titulo}")
        return "\n".join(lines)

    def encerrar_projeto(self, args: str) -> str:
        projeto = self._context.current_project
        if not projeto:
            return "Nenhum projeto selecionado."
        self._context.clear()
        if self._on_projeto_selecionado:
            self._on_projeto_selecionado(None)
        return f"Projeto '{projeto.nome}' encerrado."

    def encerrar_atividades(self, args: str) -> str:
        projeto = self._context.current_project
        if not projeto:
            return "Nenhum projeto selecionado. Use /selecionar-projeto primeiro."
        if not self._git_service.is_git_repo(projeto.pasta):
            return f"O diretório de '{projeto.nome}' não é um repositório Git."
        valid, error, status = self._validar_git(projeto)
        if not valid:
            return error

        branch = self._git_service.get_current_branch(projeto.pasta)
        changed_files = self._git_service.get_changed_files(projeto.pasta)

        if changed_files:
            files = "\n".join(item.get("path", "") for item in changed_files)
            return (
                "Arquivos alterados:\n"
                f"{files}\n\n"
                'Para enviar, digite: /commit <mensagem do commit>\n'
                "Para cancelar, digite /encerrar-projeto"
            )

        if int(status["behind"]) > 0:
            return "Push bloqueado: o remoto avançou. Inicie a atividade para atualizar."

        if int(status["ahead"]) > 0:
            ok, output = self._git_service.fetch(projeto.pasta)
            if not ok:
                return f"Falha no re-fetch: {output}"
            status2 = self._git_service.get_branch_status(projeto.pasta)
            if int(status2.get("behind", "1")) > 0:
                return "O remoto avançou durante a operação. Tente novamente."
            ok, output = self._git_service.push(projeto.pasta, branch)
            if not ok:
                return f"Falha no push: {output}"

        self._historico_service.registrar(
            "Git", f"Atividades encerradas via chat: {projeto.nome}"
        )
        return (
            f"Atividades encerradas para '{projeto.nome}'. "
            f"Branch '{branch}' sincronizada."
        )

    def _executar_commit_chat(self, message: str) -> str:
        projeto = self._context.current_project
        if not projeto:
            return "Nenhum projeto selecionado."
        if not self._git_service.is_git_repo(projeto.pasta):
            return f"O diretório de '{projeto.nome}' não é um repositório Git."
        branch = self._git_service.get_current_branch(projeto.pasta)
        upstream = self._git_service.get_upstream(projeto.pasta)
        branch_error = self._validar_branch(projeto, branch, upstream)
        if branch_error:
            return branch_error
        changed_files = self._git_service.get_changed_files(projeto.pasta)
        if not changed_files:
            return "Nenhum arquivo alterado para commit."

        ok, output = self._git_service.stage_all(projeto.pasta)
        if not ok:
            return f"Erro ao preparar arquivos: {output}"
        ok, output = self._git_service.commit(projeto.pasta, message)
        if not ok:
            return f"Erro no commit: {output}"
        ok, output = self._git_service.fetch(projeto.pasta)
        if not ok:
            return f"Commit local realizado, mas o fetch falhou: {output}"
        status = self._git_service.get_branch_status(projeto.pasta)
        if int(status.get("behind", "1")) > 0:
            return "Commit local realizado, mas o remoto avançou. Inicie a atividade para atualizar antes do push."
        ok, output = self._git_service.push(projeto.pasta, branch)
        if not ok:
            return f"Commit local realizado, mas o push falhou: {output}"
        self._historico_service.registrar(
            "Git", f"Chat commit+push: {projeto.nome}: {message}"
        )
        return f"Commit e push realizados com sucesso para '{projeto.nome}'."

    def atualizar_documentacao_local(self, args: str) -> str:
        projeto = self._context.current_project
        if not projeto:
            return "Nenhum projeto selecionado. Use /selecionar-projeto primeiro."
        if not self._git_service.is_git_repo(projeto.pasta):
            return f"O diretório de '{projeto.nome}' não é um repositório Git."
        valid, error, status = self._validar_git(projeto)
        if not valid:
            return error
        changed_files = self._git_service.get_changed_files(projeto.pasta)
        if changed_files:
            files = "\n".join(item.get("path", "") for item in changed_files)
            return f"Pull bloqueado por alterações locais:\n{files}"
        if int(status["behind"]) > 0:
            branch = self._git_service.get_current_branch(projeto.pasta)
            ok, output = self._git_service.pull(projeto.pasta, branch)
            if not ok:
                return f"Falha ao atualizar com pull --ff-only: {output}"
        return (
            f"Documentação local atualizada com sucesso para '{projeto.nome}'."
        )

    def opencode(self, args: str) -> str:
        projeto = self._context.current_project
        pasta = projeto.pasta if projeto else None

        import os
        destino = pasta or os.getcwd()
        try:
            subprocess.Popen(
                f'start "OpenCode - {projeto.nome if projeto else ""}" '
                f'opencode "{destino}"',
                shell=True,
            )
        except FileNotFoundError:
            return (
                "OpenCode não encontrado. "
                "Abra um terminal e execute: opencode"
            )
        return (
            "OpenCode iniciado para "
            + (f"'{projeto.nome}'" if projeto else "o diretório atual")
            + ".\n"
            "Use o terminal do OpenCode para analisar código, "
            "ver pendências ou refatorar."
        )

    def ajuda(self, args: str) -> str:
        return (
            "Comandos disponíveis:\n\n"
            "/selecionar-projeto\n"
            "  Lista e seleciona um projeto\n\n"
            "/pendencias\n"
            "  Lista tarefas pendentes do projeto atual\n\n"
            "/encerrar-projeto\n"
            "  Encerra o projeto atual\n\n"
            "/encerrar-atividades\n"
            "  Encerra atividades com push\n\n"
            "/commit <mensagem>\n"
            "  Commita e envia todas as alterações do projeto atual\n\n"
            "/atualizar-documentacao-local\n"
            "  Pull do projeto atual\n\n"
            "/opencode [pergunta]\n"
            "  Abre o OpenCode para o projeto atual\n\n"
            "/ajuda\n"
            "  Exibe esta mensagem"
        )
