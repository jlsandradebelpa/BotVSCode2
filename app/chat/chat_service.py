from __future__ import annotations

from typing import Callable, List, Optional

from projetos import Projeto
from services.git_service import GitService
from services.github_service import GitHubService
from services.historico_service import HistoricoService
from services.project_service import ProjectService
from services.vscode_service import VSCodeService
from chat.command_context import CommandContext
from chat.command_executor import CommandExecutor
from chat.command_parser import CommandParser
from chat.command_registry import CommandRegistry


class ChatService:
    def __init__(
        self,
        project_service: ProjectService,
        git_service: GitService,
        github_service: GitHubService,
        historico_service: HistoricoService,
        vscode_service: VSCodeService,
    ) -> None:
        self._context = CommandContext()
        self._registry = CommandRegistry()
        self._executor = CommandExecutor(
            project_service,
            git_service,
            github_service,
            historico_service,
            vscode_service,
            self._context,
        )
        self._on_projeto_selecionado: Optional[
            Callable[[Optional[Projeto]], None]
        ] = None

        self._register_commands()

    def _register_commands(self) -> None:
        self._registry.register(
            "selecionar-projeto",
            self._executor.selecionar_projeto,
            "Lista e seleciona um projeto",
        )
        self._registry.register(
            "pendencias",
            self._executor.pendencias,
            "Lista tarefas pendentes do projeto atual",
        )
        self._registry.register(
            "encerrar-projeto",
            self._executor.encerrar_projeto,
            "Encerra o projeto atual",
        )
        self._registry.register(
            "encerrar-atividades",
            self._executor.encerrar_atividades,
            "Encerra atividades com push",
        )
        self._registry.register(
            "atualizar-documentacao-local",
            self._executor.atualizar_documentacao_local,
            "Pull do projeto atual",
        )
        self._registry.register(
            "ajuda",
            self._executor.ajuda,
            "Exibe esta mensagem de ajuda",
        )

    def definir_on_projeto_selecionado(
        self, callback: Callable[[Optional[Projeto]], None]
    ) -> None:
        self._on_projeto_selecionado = callback
        self._executor._on_projeto_selecionado = callback

    @property
    def context(self) -> CommandContext:
        return self._context

    def process_input(self, text: str) -> str:
        if not text.strip():
            return ""

        if self._context.awaiting_selection:
            return self._handle_selection(text)

        command, args = CommandParser.parse(text)
        if command is None:
            return (
                'Digite "/" para ver os comandos disponíveis '
                "ou /ajuda para obter ajuda."
            )

        handler = self._registry.get_handler(command)
        if handler is None:
            return (
                f"Comando '{command}' não encontrado. "
                "Digite /ajuda para ver os comandos disponíveis."
            )

        return handler(args)

    def _handle_selection(self, text: str) -> str:
        self._context.awaiting_selection = False
        try:
            indice = int(text.strip()) - 1
        except ValueError:
            return "Digite o número do projeto desejado."
        return self._executor._selecionar_por_indice(indice)

    def get_suggestions(self, text: str) -> List[str]:
        available = list(self._registry.commands.keys())
        suggestions = CommandParser.get_suggestions(text, available)
        return [f"/{cmd}" for cmd in suggestions]

    def list_commands(self) -> List[dict]:
        return self._registry.list_commands()
