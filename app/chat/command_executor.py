from __future__ import annotations

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
        if self._git_service.has_uncommitted_changes(projeto.pasta):
            return (
                "Existem alterações locais pendentes. Faça commit antes de encerrar."
            )
        branch = self._git_service.get_current_branch(projeto.pasta)
        if not branch:
            return "Não foi possível determinar a branch atual."
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

    def atualizar_documentacao_local(self, args: str) -> str:
        projeto = self._context.current_project
        if not projeto:
            return "Nenhum projeto selecionado. Use /selecionar-projeto primeiro."
        if not self._git_service.is_git_repo(projeto.pasta):
            return f"O diretório de '{projeto.nome}' não é um repositório Git."
        branch = self._git_service.get_current_branch(projeto.pasta)
        ok, output = self._git_service.pull(projeto.pasta, branch)
        if not ok:
            return f"Falha ao atualizar: {output}"
        return (
            f"Documentação local atualizada com sucesso para '{projeto.nome}'."
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
            "/atualizar-documentacao-local\n"
            "  Pull do projeto atual\n\n"
            "/ajuda\n"
            "  Exibe esta mensagem"
        )
