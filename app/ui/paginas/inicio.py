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
        self._file_checkboxes: list[ft.Checkbox] = []
        self._selected_files: list[str] = []

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

    def _atualizar(self, sincronizado: bool = False) -> None:
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

        if sincronizado:
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

        branch = self._git_service.get_current_branch(projeto.pasta)
        upstream = self._git_service.get_upstream(projeto.pasta)
        branch_error = self._validar_branch(projeto, branch, upstream)
        if branch_error:
            self._mensagem(branch_error)
            return

        if self._git_service.has_conflicts(projeto.pasta):
            self._mensagem("BLOQUEADO: existem conflitos Git não resolvidos no projeto.")
            return

        status = self._git_service.get_branch_status(projeto.pasta)
        ahead = self._numero_status(status.get("ahead", "?"))
        behind = self._numero_status(status.get("behind", "?"))
        if ahead is None or behind is None:
            self._mensagem("BLOQUEADO: não foi possível comparar a branch local com o upstream.")
            return
        if ahead > 0 and behind > 0:
            self._mensagem(
                f"BLOQUEADO: branch divergente. Local à frente: {ahead}; atrás: {behind}."
            )
            return

        changed_files = self._git_service.get_changed_files(projeto.pasta)
        if changed_files:
            self._mostrar_alteracoes_inicio(e, projeto, branch, upstream, status, changed_files)
            return

        if behind > 0:
            ok, output = self._git_service.pull(projeto.pasta, branch)
            if not ok:
                self._mensagem(f"Falha no pull --ff-only: {output}")
                return

        self._abrir_sessao(projeto)

    @staticmethod
    def _numero_status(value: str) -> Optional[int]:
        try:
            return int(value)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def _validar_branch(projeto: Projeto, branch: str, upstream: str) -> str:
        details = (
            f"Configurada: {projeto.branch or '---'} | "
            f"Atual: {branch or '---'} | Upstream: {upstream or '---'}"
        )
        if not branch:
            return f"BLOQUEADO: branch atual não identificada. {details}"
        if branch != projeto.branch:
            return f"BLOQUEADO: branch incorreta. {details}"
        if not upstream:
            return f"BLOQUEADO: branch sem upstream. {details}"
        upstream_branch = upstream.split("/", 1)[-1]
        if upstream_branch != branch:
            return f"BLOQUEADO: upstream não corresponde à branch atual. {details}"
        return ""

    @staticmethod
    def _formatar_arquivos(files: list[dict]) -> str:
        return "\n".join(
            f"{item.get('status', '??')}  {item.get('path', '')}" for item in files
        )

    def _mostrar_alteracoes_inicio(
        self,
        e: ft.ControlEvent,
        projeto: Projeto,
        branch: str,
        upstream: str,
        status: dict,
        files: list[dict],
    ) -> None:
        texto = (
            f"Branch atual: {branch}\n"
            f"Upstream: {upstream}\n"
            f"Commits à frente: {status.get('ahead', '?')}\n"
            f"Commits atrás: {status.get('behind', '?')}\n\n"
            f"Arquivos modificados:\n{self._formatar_arquivos(files)}\n\n"
            "O pull não será executado. Deseja abrir a sessão mantendo essas alterações?"
        )
        dialog = ft.AlertDialog(
            title=ft.Text("Alterações locais encontradas"),
            content=ft.Container(content=ft.Text(texto, selectable=True), width=620),
            actions=[
                ft.TextButton(
                    "Abrir sem atualizar",
                    on_click=lambda event: self._confirmar_abertura_sem_pull(event, projeto),
                ),
                ft.TextButton("Cancelar", on_click=self._cancelar_inicio),
            ],
        )
        e.page.show_dialog(dialog)
        self._mensagem("Alterações locais encontradas. Pull bloqueado; escolha como continuar.")

    def _confirmar_abertura_sem_pull(self, e: ft.ControlEvent, projeto: Projeto) -> None:
        e.page.pop_dialog()
        self._abrir_sessao(projeto, " Pull não executado devido a alterações locais.")

    def _cancelar_inicio(self, e: ft.ControlEvent) -> None:
        e.page.pop_dialog()
        self._mensagem("Início da atividade cancelado; nenhuma alteração foi descartada.")

    def _abrir_sessao(self, projeto: Projeto, observacao: str = "") -> None:

        if not self._vscode_service.installed():
            self._mensagem("VS Code não encontrado no PATH.")
            return
        if not self._vscode_service.abrir(projeto.pasta):
            self._mensagem("Falha ao abrir VS Code.")
            return

        self._historico_service.registrar(
            "Git", f"Projeto iniciado: {projeto.nome}.{observacao}"
        )
        self._mensagem(f"Atividade iniciada. Ambiente de {projeto.nome} pronto.{observacao}")
        self._atualizar(sincronizado=True)

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

        success, output = self._git_service.fetch(projeto.pasta)
        if not success:
            self._mensagem(f"Falha no fetch antes do encerramento: {output}")
            return

        branch = self._git_service.get_current_branch(projeto.pasta)
        upstream = self._git_service.get_upstream(projeto.pasta)
        branch_error = self._validar_branch(projeto, branch, upstream)
        if branch_error:
            self._mensagem(branch_error)
            return
        if self._git_service.has_conflicts(projeto.pasta):
            self._mensagem("BLOQUEADO: resolva os conflitos Git antes de encerrar.")
            return

        status = self._git_service.get_branch_status(projeto.pasta)
        ahead = self._numero_status(status.get("ahead", "?"))
        behind = self._numero_status(status.get("behind", "?"))
        if ahead is None or behind is None:
            self._mensagem("BLOQUEADO: não foi possível comparar a branch com o upstream.")
            return
        if behind > 0:
            self._mensagem(
                f"BLOQUEADO: o remoto avançou {behind} commit(s). Atualize com segurança antes do push."
            )
            return

        changed_files = self._git_service.get_changed_files(projeto.pasta)
        if not changed_files:
            if ahead > 0:
                ok, output = self._git_service.push(projeto.pasta, branch)
            else:
                ok, output = True, "Branch já sincronizada."
            if not ok:
                self._mensagem(f"Falha no push: {output}")
                return
            self._historico_service.registrar(
                "Git", f"Trabalho encerrado: {projeto.nome} sincronizado (sem alterações)"
            )
            if self._vscode_service.installed():
                self._vscode_service.fechar(projeto.pasta)
            self._mensagem(f"Atividade encerrada. Branch {branch} sincronizada.")
            self._atualizar(sincronizado=True)
            return

        self._mostrar_selecao_arquivos(e, changed_files)

    def _mostrar_selecao_arquivos(self, e: ft.ControlEvent, files: list[dict]) -> None:
        self._file_checkboxes = [
            ft.Checkbox(
                label=f"{item.get('status', '??')}  {item.get('path', '')}",
                value=False,
                data=item.get("path", ""),
            )
            for item in files
        ]
        dialog = ft.AlertDialog(
            title=ft.Text("Selecionar arquivos para o commit"),
            content=ft.Container(
                content=ft.Column(self._file_checkboxes, scroll=ft.ScrollMode.AUTO),
                width=650,
                height=min(420, max(120, len(files) * 48)),
            ),
            actions=[
                ft.TextButton("Continuar", on_click=self._confirmar_selecao),
                ft.TextButton("Cancelar", on_click=self._cancelar_commit),
            ],
        )
        e.page.show_dialog(dialog)
        self._mensagem("Selecione explicitamente os arquivos que deverão entrar no commit.")

    def _confirmar_selecao(self, e: ft.ControlEvent) -> None:
        if not self._projeto_atual:
            return
        self._selected_files = [
            str(checkbox.data)
            for checkbox in self._file_checkboxes
            if checkbox.value and checkbox.data
        ]
        if not self._selected_files:
            self._mensagem("Selecione pelo menos um arquivo antes de continuar.")
            return
        e.page.pop_dialog()
        self._commit_field = ft.TextField(
            label="Mensagem do commit",
            value=(
                f"Atualiza {self._projeto_atual.nome} - "
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            ),
            multiline=False,
            autofocus=True,
        )
        arquivos = "\n".join(self._selected_files)
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar commit"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("Arquivos selecionados:", weight=ft.FontWeight.BOLD),
                    ft.Text(arquivos, selectable=True),
                    self._commit_field,
                ]),
                width=650,
            ),
            actions=[
                ft.TextButton("Confirmar commit e push", on_click=self._executar_commit),
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

        ok, output = self._git_service.stage_files(projeto.pasta, self._selected_files)
        if not ok:
            self._mensagem(f"Erro ao preparar arquivos: {output}")
            return
        ok, output = self._git_service.commit(projeto.pasta, message)
        if not ok:
            self._mensagem(f"Erro no commit: {output}")
            return

        ok, output = self._git_service.fetch(projeto.pasta)
        if not ok:
            self._historico_service.registrar(
                "Git", f"Commit local em {projeto.nome}; fetch antes do push falhou: {message}"
            )
            self._mensagem(f"Commit local realizado, mas o fetch antes do push falhou: {output}")
            self._atualizar()
            return

        branch = self._git_service.get_current_branch(projeto.pasta)
        upstream = self._git_service.get_upstream(projeto.pasta)
        branch_error = self._validar_branch(projeto, branch, upstream)
        status = self._git_service.get_branch_status(projeto.pasta)
        behind = self._numero_status(status.get("behind", "?"))
        if branch_error or behind is None or behind > 0:
            detalhe = branch_error or f"O remoto avançou {behind} commit(s)."
            self._historico_service.registrar(
                "Git", f"Commit local em {projeto.nome}; push bloqueado: {message}"
            )
            self._mensagem(f"Commit local realizado, mas o push foi bloqueado. {detalhe}")
            self._atualizar()
            return

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
        self._atualizar(sincronizado=True)

    def _cancelar_commit(self, e: ft.ControlEvent) -> None:
        e.page.pop_dialog()
        self._mensagem("Alterações não enviadas; encerramento cancelado.")
