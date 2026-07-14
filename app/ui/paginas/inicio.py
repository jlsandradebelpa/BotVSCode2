from __future__ import annotations

import datetime
from typing import Callable, Optional

import flet as ft

from projetos import Projeto
from services.git_service import GitService
from services.github_service import GitHubService
from services.historico_service import HistoricoService
from services.vscode_service import VSCodeService


class InicioPage:
    def __init__(
        self,
        git_service: GitService,
        vscode_service: VSCodeService,
        historico_service: HistoricoService,
        github_service: GitHubService,
        workspace_drive: str,
    ) -> None:
        self._git_service = git_service
        self._vscode_service = vscode_service
        self._historico_service = historico_service
        self._github_service = github_service
        self._workspace_drive = workspace_drive
        self._projeto_atual: Optional[Projeto] = None
        self._on_mensagem: Callable[[str], None] = lambda msg: None
        self._commit_field: Optional[ft.TextField] = None

    def definir_on_mensagem(self, callback: Callable[[str], None]) -> None:
        self._on_mensagem = callback

    def _mensagem(self, texto: str) -> None:
        self._on_mensagem(texto)

    def definir_projeto(self, projeto: Optional[Projeto]) -> None:
        self._projeto_atual = projeto
        if not hasattr(self, "_txt_nome"):
            return

        if projeto:
            self._txt_nome.value = projeto.nome
            caminho = self._git_service.get_caminho(projeto.pasta)
            self._txt_pasta.value = str(caminho) if caminho else projeto.pasta
            self._txt_branch.value = projeto.branch
        else:
            self._txt_nome.value = "Nenhum projeto selecionado"
            self._txt_pasta.value = "Selecione um projeto na aba Projetos."
            self._txt_branch.value = ""
        self._atualizar()

    def _atualizar(self) -> None:
        if not hasattr(self, "_txt_status_git"):
            return

        if self._projeto_atual:
            branch = self._git_service.get_current_branch(self._projeto_atual.pasta)
            status = self._git_service.get_branch_status(self._projeto_atual.pasta)
            self._txt_status_git.value = (
                f"Branch: {branch or '---'} | "
                f"À frente: {status.get('ahead', '?')} | "
                f"Atrás: {status.get('behind', '?')}"
            )
            if self._vscode_service.installed():
                self._txt_status_vscode.value = "VS Code instalado"
                self._txt_status_vscode.color = ft.Colors.GREEN
            else:
                self._txt_status_vscode.value = "VS Code não encontrado"
                self._txt_status_vscode.color = ft.Colors.ORANGE
            historico = self._historico_service.listar()
            self._txt_ultima_ativ.value = (
                f"{historico[-1].get('hora', '')} - {historico[-1].get('descricao', '')}"
                if historico
                else "Nenhuma atividade registrada hoje."
            )
        else:
            self._txt_status_git.value = "---"
            self._txt_status_vscode.value = "---"
            self._txt_ultima_ativ.value = "---"

        self._txt_ultima_sinc.value = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        try:
            if self._txt_status_git.page:
                self._txt_status_git.page.update()
        except RuntimeError:
            pass

    def construir(self) -> ft.Control:
        self._txt_nome = ft.Text(
            "Nenhum projeto selecionado", size=16, weight=ft.FontWeight.BOLD
        )
        self._txt_pasta = ft.Text(
            "Selecione um projeto na aba Projetos.",
            size=13,
            color=ft.Colors.GREY_500,
            selectable=True,
        )
        self._txt_branch = ft.Text("", size=13, color=ft.Colors.GREY_500)
        self._txt_status_git = ft.Text("---", size=13, selectable=True)
        self._txt_status_vscode = ft.Text("---", size=13)
        self._txt_ultima_sinc = ft.Text("---", size=13)
        self._txt_ultima_ativ = ft.Text("---", size=13, selectable=True)

        projeto_card = ft.Container(
            content=ft.Column([
                ft.Text("Projeto Atual", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                ft.Text("Nome", weight=ft.FontWeight.BOLD, size=13),
                self._txt_nome,
                ft.Text("Pasta", weight=ft.FontWeight.BOLD, size=13),
                self._txt_pasta,
                ft.Text("Branch", weight=ft.FontWeight.BOLD, size=13),
                self._txt_branch,
            ]),
            padding=16,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            col={"sm": 12, "md": 6},
        )

        status_card = ft.Container(
            content=ft.Column([
                ft.Text("Status", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                ft.Text("Git", weight=ft.FontWeight.BOLD, size=13),
                self._txt_status_git,
                ft.Text("VS Code", weight=ft.FontWeight.BOLD, size=13),
                self._txt_status_vscode,
                ft.Divider(height=1, color=ft.Colors.OUTLINE_VARIANT),
                ft.Text("Última sincronização", weight=ft.FontWeight.BOLD, size=13),
                self._txt_ultima_sinc,
                ft.Text("Última atividade", weight=ft.FontWeight.BOLD, size=13),
                self._txt_ultima_ativ,
            ]),
            padding=16,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            col={"sm": 12, "md": 6},
        )

        return ft.Column([
            ft.ResponsiveRow(
                [projeto_card, status_card],
                spacing=16,
                run_spacing=16,
            ),
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    def iniciar_atividade(self, e: ft.ControlEvent) -> None:
        if not self._projeto_atual:
            self._mensagem("Selecione um projeto na aba Projetos antes de iniciar.")
            return

        projeto = self._projeto_atual
        self._mensagem(f"Iniciando atividade para {projeto.nome}...")

        caminho = self._git_service.get_caminho(projeto.pasta)
        if not caminho:
            self._mensagem(f"ERRO: caminho não encontrado: {projeto.pasta}")
            return
        if not self._git_service.is_git_repo(projeto.pasta):
            self._mensagem("ERRO: o diretório não é um repositório Git.")
            return

        success, output = self._git_service.fetch(projeto.pasta)
        if not success:
            self._mensagem(f"Falha no fetch: {output}")
            return

        status = self._git_service.get_branch_status(projeto.pasta)
        branch = self._git_service.get_current_branch(projeto.pasta)
        behind = status.get("behind", "0")
        if behind not in ("0", "?"):
            if self._git_service.has_uncommitted_changes(projeto.pasta):
                self._mensagem(
                    "Existem alterações locais. Faça commit, stash ou descarte antes do pull."
                )
                return
            ok, output = self._git_service.pull(projeto.pasta, branch)
            if not ok:
                self._mensagem(f"Falha no pull: {output}")
                return

        if not self._vscode_service.installed():
            self._mensagem("VS Code não encontrado no PATH.")
            return
        if not self._vscode_service.abrir(projeto.pasta):
            self._mensagem("Falha ao abrir VS Code.")
            return

        self._historico_service.registrar(
            "Git", f"Projeto iniciado e sincronizado: {projeto.nome}"
        )
        self._mensagem(f"Atividade iniciada. Ambiente de {projeto.nome} pronto.")
        self._atualizar()

    def encerrar_atividade(self, e: ft.ControlEvent) -> None:
        if not self._projeto_atual:
            self._mensagem("Selecione um projeto na aba Projetos antes de encerrar.")
            return

        projeto = self._projeto_atual
        caminho = self._git_service.get_caminho(projeto.pasta)
        if not caminho:
            self._mensagem(f"ERRO: caminho não encontrado: {projeto.pasta}")
            return
        if not self._git_service.is_git_repo(projeto.pasta):
            self._mensagem("ERRO: o diretório não é um repositório Git.")
            return

        if not self._git_service.has_uncommitted_changes(projeto.pasta):
            branch = self._git_service.get_current_branch(projeto.pasta)
            ok, output = self._git_service.push(projeto.pasta, branch)
            if not ok:
                self._mensagem(f"Falha no push: {output}")
                return
            self._historico_service.registrar(
                "Git", f"Trabalho encerrado: {projeto.nome} sincronizado (sem alterações)"
            )
            if self._vscode_service.installed():
                self._vscode_service.fechar(projeto.pasta)
            self._mensagem(f"Atividade encerrada. Branch {branch} sincronizada.")
            self._atualizar()
            return

        self._mensagem("Alterações locais encontradas.")
        dialog = ft.AlertDialog(
            title=ft.Text("Commit e Push"),
            content=ft.Text("Deseja commitar e enviar as alterações?"),
            actions=[
                ft.TextButton("Sim", on_click=self._confirmar_commit),
                ft.TextButton("Não", on_click=self._cancelar_commit),
            ],
        )
        e.page.show_dialog(dialog)

    def _confirmar_commit(self, e: ft.ControlEvent) -> None:
        if not self._projeto_atual:
            return
        e.page.pop_dialog()
        self._commit_field = ft.TextField(
            hint_text="Digite a mensagem do commit...",
            multiline=False,
            autofocus=True,
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Mensagem do Commit"),
            content=self._commit_field,
            actions=[
                ft.TextButton("Confirmar", on_click=self._executar_commit),
                ft.TextButton("Cancelar", on_click=lambda ev: ev.page.pop_dialog()),
            ],
        )
        e.page.show_dialog(dialog)

    def _executar_commit(self, e: ft.ControlEvent) -> None:
        projeto = self._projeto_atual
        if not projeto or not self._commit_field:
            return
        message = (self._commit_field.value or "").strip()
        if not message:
            self._mensagem("A mensagem do commit não pode estar vazia.")
            return
        e.page.pop_dialog()

        ok, output = self._git_service.stage_all(projeto.pasta)
        if not ok:
            self._mensagem(f"Erro ao preparar arquivos: {output}")
            return
        ok, output = self._git_service.commit(projeto.pasta, message)
        if not ok:
            self._mensagem(f"Erro no commit: {output}")
            return

        branch = self._git_service.get_current_branch(projeto.pasta)
        ok, output = self._git_service.push(projeto.pasta, branch)
        if not ok:
            self._historico_service.registrar(
                "Git", f"Commit local em {projeto.nome}, mas push falhou: {message}"
            )
            self._mensagem(f"Commit realizado, mas o push falhou: {output}")
            self._atualizar()
            return

        self._historico_service.registrar(
            "Git", f"Trabalho encerrado: {projeto.nome} commitado e enviado: {message}"
        )
        if self._vscode_service.installed():
            self._vscode_service.fechar(projeto.pasta)
        self._mensagem("Atividade encerrada. Commit e push realizados com sucesso.")
        self._atualizar()

    def _cancelar_commit(self, e: ft.ControlEvent) -> None:
        e.page.pop_dialog()
        self._mensagem("Alterações não enviadas; encerramento cancelado.")
