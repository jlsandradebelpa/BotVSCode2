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
from services.preferences_service import PreferencesService
from services.vscode_service import VSCodeService
from ui.paginas.atividades import AtividadesPage
from ui.paginas.configuracoes import ConfiguracoesPage
from ui.paginas.inicio import InicioPage
from ui.paginas.preferencias import PreferenciasPage
from ui.paginas.projetos import ProjetosPage
from ui.tema import aplicar_tema


class BotVSCode2App:
    def __init__(
        self,
        config: Config,
        projetos_manager: ProjetosManager,
        preferences_service: PreferencesService,
    ) -> None:
        self._config = config
        self._projetos_manager = projetos_manager

        self._project_service = ProjectService(projetos_manager)
        self._git_service = GitService(config.workspace_drive)
        self._github_service = GitHubService()
        self._vscode_service = VSCodeService(config.workspace_drive)

        hist_pasta: Optional[Path] = None
        if config.historico_pasta:
            hist_pasta = Path(config.historico_pasta)
        self._historico_service = HistoricoService(hist_pasta)
        self._preferences_service = preferences_service

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

        self._projeto_atual: Optional[Projeto] = None
        self._aba_atual = 0

    def _on_mensagem(self, texto: str) -> None:
        if hasattr(self, "_txt_mensagem"):
            self._txt_mensagem.value = texto
            self._txt_mensagem.update()

    def _on_projeto_selecionado(self, projeto: Optional[Projeto]) -> None:
        self._projeto_atual = projeto
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
                ft.Container(width=12),
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

        page.add(
            ft.Column([
                titulo,
                barra_principal,
                self._content,
                mensagem_bar,
            ], spacing=0, expand=True)
        )
        page.update()
