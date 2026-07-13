from __future__ import annotations

from pathlib import Path
from typing import Optional

import flet as ft

from config import Config
from projetos import Projeto, ProjetosManager
from services.git_service import GitService
from services.github_service import GitHubService
from services.historico_service import HistoricoService
from services.project_service import ProjectService
from services.vscode_service import VSCodeService
from ui.paginas.atividades import AtividadesPage
from ui.paginas.configuracoes import ConfiguracoesPage
from ui.paginas.inicio import InicioPage
from ui.paginas.projetos import ProjetosPage
from ui.tema import aplicar_tema


class BotVSCode2App:
    def __init__(self, config: Config, projetos_manager: ProjetosManager) -> None:
        self._config = config
        self._projetos_manager = projetos_manager

        self._project_service = ProjectService(projetos_manager)
        self._git_service = GitService(config.workspace_drive)
        self._github_service = GitHubService()
        self._vscode_service = VSCodeService(config.workspace_drive)

        hist_pasta: Optional[Path] = None
        if config.historico_pasta:
            hist_pasta = Path(config.historico_pasta)
        self._historico_service = HistoricoService()

        self._inicio_page = InicioPage(
            self._git_service,
            self._vscode_service,
            self._historico_service,
            self._github_service,
            config.workspace_drive,
        )
        self._file_picker = ft.FilePicker()
        self._projetos_page = ProjetosPage(self._project_service, self._file_picker)
        self._atividades_page = AtividadesPage(self._historico_service)
        self._configuracoes_page = ConfiguracoesPage()

        self._projeto_atual: Optional[Projeto] = None

        if self._project_service.count > 0:
            self._projeto_atual = self._project_service.get_by_index(0)

    def _on_mensagem(self, texto: str) -> None:
        if hasattr(self, "_txt_mensagem"):
            self._txt_mensagem.value = texto
            self._txt_mensagem.update()

    def _on_projeto_selecionado(self, projeto: Optional[Projeto]) -> None:
        self._projeto_atual = projeto
        self._inicio_page.definir_projeto(projeto)

    def _mudar_aba(self, page: ft.Page, index: int) -> None:
        if index == 0:
            nova_pagina = self._inicio_page.construir()
        elif index == 1:
            nova_pagina = self._projetos_page.construir()
        elif index == 2:
            nova_pagina = self._atividades_page.construir()
        elif index == 3:
            nova_pagina = self._configuracoes_page.construir()
        else:
            return
        self._content.content = nova_pagina
        page.update()

    def run(self, page: ft.Page) -> None:
        aplicar_tema(page)
        page.title = "BotVSCode2"

        self._txt_mensagem = ft.Text("", size=13, color=ft.Colors.GREEN, selectable=True)

        nav = ft.NavigationBar(
            selected_index=0,
            on_change=lambda e: self._mudar_aba(page, e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(icon=ft.Icons.FOLDER, label="Projetos"),
                ft.NavigationBarDestination(icon=ft.Icons.HISTORY, label="Atividades"),
                ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Configuracoes"),
            ],
        )

        self._inicio_page.definir_on_mensagem(self._on_mensagem)
        self._inicio_page.definir_projeto(self._projeto_atual)
        self._projetos_page.definir_on_mensagem(self._on_mensagem)
        self._projetos_page.definir_on_projeto_selecionado(self._on_projeto_selecionado)

        titulo = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CODE, color=ft.Colors.INDIGO_300, size=28),
                ft.Text("BotVSCode2", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.INDIGO_300),
            ]),
            padding=ft.Padding(left=16, top=8, right=0, bottom=8),
            bgcolor=ft.Colors.GREY_800,
        )

        self._content = ft.Container(
            content=self._inicio_page.construir(),
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            expand=True,
        )

        mensagem_bar = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INFO_OUTLINE, size=16, color=ft.Colors.GREY_400),
                self._txt_mensagem,
            ]),
            padding=ft.Padding(left=12, top=12, right=12, bottom=12),
            bgcolor=ft.Colors.GREY_800,
            border=ft.Border(top=ft.BorderSide(1, ft.Colors.GREY_700)),
        )

        page.overlay.append(self._file_picker)

        page.add(
            ft.Column([
                titulo,
                nav,
                self._content,
                mensagem_bar,
            ], spacing=0, expand=True)
        )
        page.update()
