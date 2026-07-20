from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Optional

import flet as ft

from app_state import AppState
from config import Config
from data_paths import AppDataPaths
from projetos import Projeto, ProjetosManager
from services.git_service import GitService
from services.github_service import GitHubService
from services.historico_service import HistoricoService
from services.project_service import ProjectService
from services.preferences_service import PreferencesService
from services.vscode_service import VSCodeService
from ui.paginas.atividades import AtividadesPage
from ui.paginas.configuracoes import ConfiguracoesPage
from ui.paginas.inicio import InicioPage
from ui.paginas.preferencias import PreferenciasPage
from ui.paginas.projetos import ProjetosPage
from ui.tema import aplicar_tema
from chat.chat_service import ChatService


class BotVSCode2App:
    def __init__(
        self,
        config: Config,
        projetos_manager: ProjetosManager,
        preferences_service: PreferencesService,
        data_paths: Optional[AppDataPaths] = None,
    ) -> None:
        self._config = config
        self._projetos_manager = projetos_manager
        self._state_path = data_paths.state if data_paths else None
        self._state = AppState.load(self._state_path) if self._state_path else AppState()

        self._project_service = ProjectService(projetos_manager)
        self._git_service = GitService(config.workspace_drive)
        self._github_service = GitHubService()
        self._vscode_service = VSCodeService(config.workspace_drive)

        hist_pasta: Optional[Path] = data_paths.sessions_dir if data_paths else None
        if hist_pasta is None and config.historico_pasta:
            hist_pasta = Path(config.historico_pasta)
        self._historico_service = HistoricoService(hist_pasta)
        self._preferences_service = preferences_service

        self._chat_service = ChatService(
            self._project_service,
            self._git_service,
            self._github_service,
            self._historico_service,
            self._vscode_service,
        )

        self._inicio_page = InicioPage(
            self._git_service,
            self._vscode_service,
            self._historico_service,
            self._github_service,
            config.workspace_drive,
        )
        self._projetos_page = ProjetosPage(self._project_service)
        self._atividades_page = AtividadesPage(self._historico_service)
        self._configuracoes_page = ConfiguracoesPage()
        self._preferencias_page = PreferenciasPage(
            self._preferences_service,
            self._aplicar_preferencias,
            self._on_mensagem,
        )

        self._projeto_atual: Optional[Projeto] = next(
            (
                projeto
                for projeto in self._project_service.projetos
                if projeto.nome == self._state.selected_project
            ),
            None,
        )
        self._aba_atual = 0

    def _on_mensagem(self, texto: str) -> None:
        if hasattr(self, "_txt_mensagem"):
            self._txt_mensagem.value = texto
            self._txt_mensagem.update()

    def _on_projeto_selecionado(self, projeto: Optional[Projeto]) -> None:
        self._projeto_atual = projeto
        self._state = AppState(selected_project=projeto.nome if projeto else "")
        if self._state_path:
            self._state.save(self._state_path)
        self._inicio_page.definir_projeto(projeto)
        if projeto:
            self._on_mensagem(f"Projeto selecionado: {projeto.nome}")

    def _aplicar_preferencias(self, preferences) -> None:
        if hasattr(self, "_page"):
            aplicar_tema(self._page, preferences)
            self._page.update()

    def _mudar_aba(self, page: ft.Page, index: int) -> None:
        self._aba_atual = index
        if index == 0:
            nova_pagina = self._inicio_page.construir()
            self._inicio_page.definir_projeto(self._projeto_atual)
        elif index == 1:
            nova_pagina = self._projetos_page.construir()
        elif index == 2:
            nova_pagina = self._atividades_page.construir()
        elif index == 3:
            nova_pagina = self._configuracoes_page.construir()
        elif index == 4:
            nova_pagina = self._preferencias_page.construir()
        else:
            return
        self._content.content = nova_pagina
        page.update()

    def _iniciar_atividade(self, e: ft.ControlEvent) -> None:
        self._inicio_page.iniciar_atividade(e)

    def _encerrar_atividade(self, e: ft.ControlEvent) -> None:
        self._inicio_page.encerrar_atividade(e)

    # --- Chat ---

    def _toggle_chat(self, e: ft.ControlEvent) -> None:
        self._chat_panel.visible = not self._chat_panel.visible
        self._page.update()

    def _add_chat_message(self, text: str, is_user: bool = False) -> None:
        bg = (
            ft.Colors.PRIMARY_CONTAINER
            if is_user
            else ft.Colors.SURFACE_CONTAINER_HIGHEST
        )
        self._chat_messages.controls.append(
            ft.Container(
                content=ft.Text(text, size=13, selectable=True),
                padding=ft.Padding(left=12, top=8, right=12, bottom=8),
                bgcolor=bg,
                border_radius=12,
            )
        )
        try:
            self._chat_messages.update()
        except RuntimeError:
            pass

    def _on_chat_submit(self, e: ft.ControlEvent) -> None:
        text = (self._chat_input.value or "").strip()
        if not text:
            return

        suggestions = self._chat_service.get_suggestions(text)

        if len(suggestions) == 1:
            text = suggestions[0]
        elif len(suggestions) > 1:
            self._chat_input.value = ""
            self._chat_input.update()
            self._add_chat_message(f"> {text}", is_user=True)
            self._add_chat_message(
                "Mais de um comando corresponde. "
                "Clique na sugestão ou digite mais caracteres."
            )
            return

        self._chat_input.value = ""
        self._suggestions_container.visible = False
        self._chat_input.update()

        if text:
            self._add_chat_message(f"> {text}", is_user=True)
            response = self._chat_service.process_input(text)
            if response:
                self._add_chat_message(response)

    def _on_chat_input_change(self, e: ft.ControlEvent) -> None:
        text = (self._chat_input.value or "").strip()
        suggestions = self._chat_service.get_suggestions(text)

        if suggestions:
            self._suggestions_container.visible = True
            self._suggestions_list.controls.clear()

            label = "Comandos disponíveis" if text.strip() == "/" else "Sugestões"
            self._suggestions_list.controls.append(
                ft.Text(label, size=11, color=ft.Colors.GREY_400, weight=ft.FontWeight.BOLD)
            )

            for cmd in suggestions:
                btn = ft.TextButton(
                    content=ft.Text(cmd, size=13),
                    on_click=lambda _, c=cmd: self._select_suggestion(c),
                    style=ft.ButtonStyle(
                        padding=ft.Padding(left=12, top=4, right=12, bottom=4),
                    ),
                )
                self._suggestions_list.controls.append(btn)
        else:
            self._suggestions_container.visible = False

        self._suggestions_container.update()

    def _select_suggestion(self, command: str) -> None:
        self._chat_input.value = ""
        self._suggestions_container.visible = False
        self._suggestions_container.update()
        self._add_chat_message(f"> {command}", is_user=True)
        response = self._chat_service.process_input(command)
        if response:
            self._add_chat_message(response)

    def _build_chat_ui(self) -> None:
        self._chat_messages = ft.Column(
            spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
        )

        self._chat_input = ft.TextField(
            hint_text='Digite "/" para comandos...',
            prefix=ft.Text("> ", weight=ft.FontWeight.BOLD),
            on_submit=self._on_chat_submit,
            on_change=self._on_chat_input_change,
            border=ft.InputBorder.NONE,
            content_padding=ft.Padding(left=8, top=8, right=8, bottom=8),
            text_size=14,
            expand=True,
        )

        self._suggestions_list = ft.Column(spacing=2, scroll=ft.ScrollMode.AUTO)
        self._suggestions_container = ft.Container(
            content=self._suggestions_list,
            visible=False,
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            border_radius=8,
            padding=ft.Padding(left=4, top=4, right=4, bottom=4),
            height=220,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.2, ft.Colors.BLACK),
            ),
        )

        avatar_panel = (
            ft.Image(
                src=str(Path(__file__).resolve().parent.parent.parent / "assets" / "avatar_bot.png"),
                width=32, height=32, fit=ft.ImageFit.CONTAIN,
            )
            if (Path(__file__).resolve().parent.parent.parent / "assets" / "avatar_bot.png").exists()
            else ft.Icon(ft.Icons.SMART_TOY, size=28, color=ft.Colors.PRIMARY)
        )

        header = ft.Container(
            content=ft.Row(
                [avatar_panel, ft.Text("Chat BotVSCode2", size=16, weight=ft.FontWeight.BOLD)],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=8,
            ),
            padding=ft.Padding(left=16, top=12, right=16, bottom=12),
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            border_radius=16,
        )

        panel_body = ft.Column([
            ft.Container(content=self._chat_messages, padding=16, expand=True),
            self._suggestions_container,
            ft.Container(
                content=ft.Row([self._chat_input], vertical_alignment=ft.CrossAxisAlignment.CENTER),
                padding=ft.Padding(left=8, top=4, right=8, bottom=8),
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            ),
        ], spacing=0, expand=True)

        self._chat_panel = ft.Container(
            content=ft.Column([header, ft.Divider(height=0), panel_body], spacing=0),
            visible=False,
            width=380,
            height=520,
            border_radius=16,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            shadow=ft.BoxShadow(
                spread_radius=2,
                blur_radius=16,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
            right=20,
            bottom=80,
            animate=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )

        avatar_btn = (
            ft.Image(
                src=str(Path(__file__).resolve().parent.parent.parent / "assets" / "avatar_bot.png"),
                width=48, height=48, fit=ft.ImageFit.CONTAIN, border_radius=24,
            )
            if (Path(__file__).resolve().parent.parent.parent / "assets" / "avatar_bot.png").exists()
            else ft.Container(
                content=ft.Row(
                    [ft.Icon(ft.Icons.SMART_TOY, size=28, color=ft.Colors.WHITE)],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                width=48, height=48,
                bgcolor=ft.Colors.PRIMARY,
                border_radius=24,
            )
        )

        self._chat_button = ft.Container(
            content=avatar_btn,
            right=20,
            bottom=20,
            width=56,
            height=56,
            border_radius=28,
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=8,
                color=ft.Colors.with_opacity(0.3, ft.Colors.BLACK),
            ),
            on_click=self._toggle_chat,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            ink=True,
        )

    def _mostrar_sobre(self, e: ft.ControlEvent) -> None:
        dlg = ft.AlertDialog(
            title=ft.Text("Sobre o BotVSCode2"),
            content=ft.Container(
                content=ft.Column([
                    ft.Text("BotVSCode2 v2.0.0", size=18, weight=ft.FontWeight.BOLD),
                    ft.Text("Assistente de produtividade para desenvolvedores", size=13),
                    ft.Divider(height=1),
                    ft.Text("Autor: Jorge Andrade", size=13),
                    ft.Text("Licença: MIT", size=13),
                    ft.Text("Repositório: jlsandradebelpa/BotVSCode2", size=13),
                    ft.Text("Tecnologias: Python + Flet + Git", size=13),
                ], spacing=6),
                width=400,
            ),
            actions=[ft.TextButton("Fechar", on_click=lambda ev: ev.control.page.pop_dialog())],
        )
        e.page.show_dialog(dlg)

    def _mostrar_backlog(self, e: ft.ControlEvent) -> None:
        repo = "jlsandradebelpa/BotVSCode2"

        try:
            repo_dir = Path(__file__).resolve().parent.parent.parent
            kwargs = {"creationflags": subprocess.CREATE_NO_WINDOW} if os.name == "nt" else {}
            result = subprocess.run(
                ["git", "log", "--format=%ad|||%s", "--date=short", "--no-decorate", "-30"],
                cwd=str(repo_dir),
                capture_output=True, text=True, encoding="utf-8",
                timeout=15, **kwargs,
            )
            raw = result.stdout.strip() if result.returncode == 0 else ""
        except Exception:
            raw = ""

        if raw:
            linhas = []
            data_atual = ""
            seq = 0
            for linha in raw.split("\n"):
                if "|||" not in linha:
                    continue
                data, msg = linha.split("|||", 1)
                if data != data_atual:
                    data_atual = data
                    seq = 0
                    linhas.append("")
                    linhas.append(data)
                seq += 1
                linhas.append(f"  {seq}. {msg.strip()}")
            log_texto = "\n".join(linhas).strip()
        else:
            log_texto = "Nenhum histórico encontrado."

        issues = self._github_service.listar_issues(repo)
        if issues:
            issues_lines = [""]
            for issue in issues:
                num = issue.get("number", "?")
                titulo = issue.get("title", "Sem título")
                issues_lines.append(f"  #{num} - {titulo}")
            issues_texto = "\n".join(issues_lines)
        else:
            issues_texto = "\n  Nenhuma issue em aberto."

        elementos = [
            ft.Text("Últimas atualizações:", size=14, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(log_texto, size=12, selectable=True, font_family="monospace"),
                padding=ft.Padding(top=4, left=0, right=0, bottom=0),
            ),
            ft.Divider(height=16),
            ft.Text("Issues em aberto:", size=14, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Text(issues_texto, size=12, selectable=True),
                padding=ft.Padding(top=4, left=0, right=0, bottom=0),
            ),
        ]

        dlg = ft.AlertDialog(
            title=ft.Text("Backlog de atualizações"),
            content=ft.Container(
                content=ft.Column(elementos),
                width=680,
            ),
            scrollable=True,
            actions=[ft.TextButton("Fechar", on_click=lambda ev: ev.control.page.pop_dialog())],
        )
        e.page.show_dialog(dlg)

    def _menu_ir_config(self, e: ft.ControlEvent) -> None:
        if hasattr(self, "_page"):
            self._page.navigation_bar.selected_index = 3
            self._mudar_aba(self._page, 3)
            self._page.update()

    def run(self, page: ft.Page) -> None:
        self._page = page
        aplicar_tema(page, self._preferences_service.preferences)
        page.title = "BotVSCode2"
        page.window.maximized = True

        self._txt_mensagem = ft.Text("", size=13, color=ft.Colors.GREEN, selectable=True)

        nav = ft.NavigationBar(
            selected_index=0,
            on_change=lambda e: self._mudar_aba(page, e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.Icons.FOLDER, label="Projetos"),
                ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Atividades"),
                ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Configuracoes"),
                ft.NavigationBarDestination(icon=ft.Icons.PALETTE, label="Preferências"),
            ],
            expand=True,
        )

        menu = ft.PopupMenuButton(
            icon=ft.Icons.MENU,
            tooltip="Menu",
            items=[
                ft.PopupMenuItem(content=ft.Text("Configurações"), icon=ft.Icons.SETTINGS, on_click=self._menu_ir_config),
                ft.PopupMenuItem(content=ft.Text("Sobre"), icon=ft.Icons.INFO, on_click=self._mostrar_sobre),
                ft.PopupMenuItem(content=ft.Text("Backlog de atualizações"), icon=ft.Icons.HISTORY, on_click=self._mostrar_backlog),
            ],
        )

        barra_principal = ft.Container(
            content=ft.Row([
                nav,
                ft.Container(width=8),
                ft.FilledTonalButton(
                    "Iniciar atividade",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=self._iniciar_atividade,
                ),
                ft.FilledTonalButton(
                    "Encerrar atividade",
                    icon=ft.Icons.STOP,
                    on_click=self._encerrar_atividade,
                ),
                ft.Container(expand=True),
                menu,
                ft.Container(width=8),
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        self._inicio_page.definir_on_mensagem(self._on_mensagem)
        self._projetos_page.definir_on_mensagem(self._on_mensagem)
        self._projetos_page.definir_on_projeto_selecionado(self._on_projeto_selecionado)

        titulo = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CODE, color=ft.Colors.PRIMARY, size=28),
                ft.Text("BotVSCode2", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PRIMARY),
            ]),
            padding=ft.Padding(left=16, top=8, right=0, bottom=8),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        pagina_inicial = self._inicio_page.construir()
        self._inicio_page.definir_projeto(self._projeto_atual)
        self._content = ft.Container(
            content=pagina_inicial,
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            expand=True,
        )

        mensagem_bar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.GREY_400),
                self._txt_mensagem,
            ]),
            padding=ft.Padding(left=12, top=12, right=12, bottom=12),
            bgcolor=ft.Colors.SURFACE_CONTAINER,
            border=ft.Border(top=ft.BorderSide(1, ft.Colors.OUTLINE_VARIANT)),
        )

        main_column = ft.Column([
            titulo,
            barra_principal,
            self._content,
            mensagem_bar,
        ], spacing=0, expand=True)

        self._build_chat_ui()

        self._chat_service.definir_on_projeto_selecionado(self._on_projeto_selecionado)

        stack = ft.Stack(
            controls=[main_column, self._chat_panel, self._chat_button],
            expand=True,
        )

        page.add(stack)
        self._add_chat_message(
            "Chat integrado ativo.\n\n"
            "Digite / para ver os comandos disponíveis "
            "ou /ajuda para obter ajuda."
        )
        page.update()
