from __future__ import annotations

import datetime
from typing import Callable, Optional

import flet as ft

from projetos import Projeto
from services.git_service import GitService
from services.github_service import GitHubService
from services.historico_service import HistoricoService
from services.vscode_service import VSCodeService
from utils import saudacao


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

    def definir_on_mensagem(self, callback: Callable[[str], None]) -> None:
        self._on_mensagem = callback

    def _mensagem(self, texto: str) -> None:
        self._on_mensagem(texto)

    def definir_projeto(self, projeto: Optional[Projeto]) -> None:
        self._projeto_atual = projeto
        if hasattr(self, "_txt_nome") and hasattr(self, "_txt_pasta") and hasattr(self, "_txt_branch"):
            if projeto:
                self._txt_nome.value = projeto.nome
                caminho = self._git_service.get_caminho(projeto.pasta)
                self._txt_pasta.value = str(caminho) if caminho else projeto.pasta
                self._txt_branch.value = projeto.branch
            else:
                self._txt_nome.value = "Nenhum projeto selecionado"
                self._txt_pasta.value = ""
                self._txt_branch.value = ""
            self._atualizar()

    def _atualizar(self) -> None:
        if hasattr(self, "_txt_status_git"):
            if self._projeto_atual:
                branch = self._git_service.get_current_branch(self._projeto_atual.pasta)
                status = self._git_service.get_branch_status(self._projeto_atual.pasta)
                self._txt_status_git.value = (
                    f"Branch: {branch or '---'} | "
                    f"Local: {status.get('ahead', '?')} | "
                    f"Remoto: {status.get('behind', '?')}"
                )
                if self._vscode_service.installed():
                    self._txt_status_vscode.value = "VS Code instalado"
                    self._txt_status_vscode.color = ft.Colors.GREEN
                else:
                    self._txt_status_vscode.value = "VS Code não encontrado"
                    self._txt_status_vscode.color = ft.Colors.ORANGE
            else:
                self._txt_status_git.value = "---"
                self._txt_status_vscode.value = "---"
            self._txt_ultima_sinc.value = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            if self._projeto_atual:
                hist = self._historico_service.listar()
                if hist:
                    self._txt_ultima_ativ.value = f"{hist[-1].get('hora', '')} - {hist[-1].get('descricao', '')}"
                else:
                    self._txt_ultima_ativ.value = "Nenhuma atividade registrada hoje."
            else:
                self._txt_ultima_ativ.value = "---"

    def construir(self) -> ft.Control:
        self._txt_nome = ft.Text("Nenhum projeto selecionado", size=16, weight=ft.FontWeight.BOLD)
        self._txt_pasta = ft.Text("", size=13, color=ft.Colors.GREY_400)
        self._txt_branch = ft.Text("", size=13, color=ft.Colors.GREY_400)

        self._txt_status_git = ft.Text("---", size=13)
        self._txt_status_vscode = ft.Text("---", size=13)
        self._txt_ultima_sinc = ft.Text("---", size=13)
        self._txt_ultima_ativ = ft.Text("---", size=13)

        btn_iniciar = ft.ElevatedButton(
            "INICIAR ATIVIDADE",
            icon=ft.Icons.PLAY_ARROW,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_700,
            style=ft.ButtonStyle(padding=ft.Padding(left=16, top=16, right=16, bottom=16)),
            on_click=self._ao_clicar_iniciar,
        )

        btn_encerrar = ft.ElevatedButton(
            "ENCERRAR ATIVIDADE",
            icon=ft.Icons.STOP,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.RED_700,
            style=ft.ButtonStyle(padding=ft.Padding(left=16, top=16, right=16, bottom=16)),
            on_click=self._ao_clicar_encerrar,
        )

        projeto_card = ft.Container(
            content=ft.Column([
                ft.Text("Projeto Atual", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                ft.Row([
                    ft.Column([ft.Text("Nome", weight=ft.FontWeight.BOLD, size=13), self._txt_nome], expand=True),
                ]),
                ft.Row([
                    ft.Column([ft.Text("Pasta", weight=ft.FontWeight.BOLD, size=13), self._txt_pasta], expand=True),
                ]),
                ft.Row([
                    ft.Column([ft.Text("Branch", weight=ft.FontWeight.BOLD, size=13), self._txt_branch], expand=True),
                ]),
            ]),
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
            border_radius=8,
            bgcolor=ft.Colors.GREY_800,
        )

        botoes_card = ft.Container(
            content=ft.Column([
                btn_iniciar,
                ft.Container(height=10),
                btn_encerrar,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
            border_radius=8,
            bgcolor=ft.Colors.GREY_800,
        )

        status_card = ft.Container(
            content=ft.Column([
                ft.Text("Status", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                ft.Row([ft.Text("Git:", weight=ft.FontWeight.BOLD, size=13), self._txt_status_git]),
                ft.Row([ft.Text("VSCode:", weight=ft.FontWeight.BOLD, size=13), self._txt_status_vscode]),
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                ft.Row([ft.Text("Última sincronização:", weight=ft.FontWeight.BOLD, size=13), self._txt_ultima_sinc]),
                ft.Row([ft.Text("Última atividade:", weight=ft.FontWeight.BOLD, size=13), self._txt_ultima_ativ]),
            ]),
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
            border_radius=8,
            bgcolor=ft.Colors.GREY_800,
        )

        return ft.Column([
            ft.Text(saudacao(), size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=16),
            projeto_card,
            ft.Container(height=16),
            botoes_card,
            ft.Container(height=16),
            status_card,
        ], scroll=ft.ScrollMode.AUTO)

    def _ao_clicar_iniciar(self, e: ft.ControlEvent) -> None:
        if not self._projeto_atual:
            self._mensagem("Selecione um projeto na aba Projetos antes de iniciar.")
            return

        projeto = self._projeto_atual
        self._mensagem(f"Iniciando atividade para {projeto.nome}...")

        caminho = self._git_service.get_caminho(projeto.pasta)
        if not caminho:
            self._mensagem(f"ERRO: Caminho não encontrado: {projeto.pasta}")
            return

        if not self._git_service.is_git_repo(projeto.pasta):
            self._mensagem("AVISO: O diretório não é um repositório Git.")
            return

        self._mensagem("Repositório Git encontrado.")

        success, _ = self._git_service.fetch(projeto.pasta)
        if not success:
            self._mensagem("AVISO: Não foi possível conectar ao repositório remoto.")
        else:
            self._mensagem("Fetch realizado com sucesso.")

        status = self._git_service.get_branch_status(projeto.pasta)
        branch = self._git_service.get_current_branch(projeto.pasta)
        behind = status.get("behind", "0")

        if behind not in ("0", "?"):
            self._mensagem("Atualizando projeto (git pull)...")
            ok, out = self._git_service.pull(projeto.pasta, branch)
            if ok:
                self._mensagem(f"Pull realizado: {out}")
            else:
                self._mensagem(f"Falha no pull: {out}")

        if self._vscode_service.installed():
            if projeto.nome:
                if self._vscode_service.abrir(projeto.pasta):
                    self._mensagem("VS Code aberto com sucesso.")
                else:
                    self._mensagem("Falha ao abrir VS Code.")

        self._historico_service.registrar("Git", f"Projeto iniciado e sincronizado: {projeto.nome}")
        self._mensagem(f"{saudacao()} Ambiente pronto para desenvolvimento!")
        self._atualizar()

    def _ao_clicar_encerrar(self, e: ft.ControlEvent) -> None:
        if not self._projeto_atual:
            self._mensagem("Selecione um projeto na aba Projetos antes de encerrar.")
            return

        projeto = self._projeto_atual
        self._mensagem(f"Encerrando atividade para {projeto.nome}...")

        caminho = self._git_service.get_caminho(projeto.pasta)
        if not caminho:
            self._mensagem(f"ERRO: Caminho não encontrado: {projeto.pasta}")
            return

        if not self._git_service.is_git_repo(projeto.pasta):
            self._mensagem("AVISO: O diretório não é um repositório Git.")
            return

        has_changes = self._git_service.has_uncommitted_changes(projeto.pasta)
        if not has_changes:
            branch = self._git_service.get_current_branch(projeto.pasta)
            ok, out = self._git_service.push(projeto.pasta, branch)
            if ok:
                self._historico_service.registrar("Git", f"Trabalho encerrado: {projeto.nome} sincronizado (sem alterações)")
                self._mensagem(f"Push realizado. Branch {branch} sincronizada.")
            else:
                self._mensagem(f"Falha no push: {out}")
            self._atualizar()
            return

        self._mensagem("Alterações locais encontradas.")
        dlg = ft.AlertDialog(
            title=ft.Text("Commit e Push"),
            content=ft.Text("Deseja commitar e enviar as alterações?"),
            actions=[
                ft.TextButton("Sim", on_click=lambda ev: self._confirmar_commit(ev)),
                ft.TextButton("Não", on_click=lambda ev: self._cancelar_commit(ev)),
            ],
        )
        e.page.show_dialog(dlg)

    def _confirmar_commit(self, e: ft.ControlEvent) -> None:
        projeto = self._projeto_atual
        if not projeto:
            return
        e.page.pop_dialog()

        dlg = ft.AlertDialog(
            title=ft.Text("Mensagem do Commit"),
            content=ft.TextField(hint_text="Digite a mensagem do commit...", multiline=False),
            actions=[
                ft.TextButton("Confirmar", on_click=lambda ev: self._executar_commit(ev)),
                ft.TextButton("Cancelar", on_click=lambda ev: ev.control.page.pop_dialog()),
            ],
        )
        e.page.show_dialog(dlg)

    def _executar_commit(self, e: ft.ControlEvent) -> None:
        projeto = self._projeto_atual
        if not projeto:
            return
        dialog = e.control.parent
        text_field = dialog.content
        msg = text_field.value.strip() if text_field else ""
        e.page.pop_dialog()

        if not msg:
            self._mensagem("Mensagem do commit não pode estar vazia.")
            return

        ok_stage, out_stage = self._git_service.stage_all(projeto.pasta)
        if not ok_stage:
            self._mensagem(f"Erro ao preparar arquivos: {out_stage}")
            return

        ok_commit, out_commit = self._git_service.commit(projeto.pasta, msg)
        if not ok_commit:
            self._mensagem(f"Erro no commit: {out_commit}")
            return

        self._historico_service.registrar("Git", f"Commit realizado em {projeto.nome}: {msg}")
        self._mensagem("Commit realizado com sucesso.")

        branch = self._git_service.get_current_branch(projeto.pasta)
        ok_push, out_push = self._git_service.push(projeto.pasta, branch)
        if ok_push:
            self._historico_service.registrar("Git", f"Trabalho encerrado: {projeto.nome} commitado e enviado")
            self._mensagem("Push realizado com sucesso. Projeto sincronizado com o GitHub.")
        else:
            self._mensagem(f"Falha no push: {out_push}")

        if self._vscode_service.installed():
            self._vscode_service.fechar(projeto.pasta)

        self._atualizar()

    def _cancelar_commit(self, e: ft.ControlEvent) -> None:
        e.page.pop_dialog()
        self._mensagem("Alterações não foram enviadas.")
