from __future__ import annotations

from typing import Callable

import flet as ft

from preferences import Preferences
from services.preferences_service import PreferencesService


class PreferenciasPage:
    def __init__(
        self,
        service: PreferencesService,
        on_aplicar: Callable[[Preferences], None],
        on_mensagem: Callable[[str], None],
    ) -> None:
        self._service = service
        self._on_aplicar = on_aplicar
        self._on_mensagem = on_mensagem

    def construir(self) -> ft.Control:
        preferences = self._service.preferences
        self._tema = ft.Dropdown(
            label="Tema",
            value=preferences.theme_mode,
            options=[
                ft.DropdownOption(key="dark", text="Escuro"),
                ft.DropdownOption(key="light", text="Claro"),
                ft.DropdownOption(key="system", text="Seguir o sistema"),
            ],
            expand=True,
        )
        self._cor = ft.Dropdown(
            label="Cor de destaque",
            value=preferences.color_seed,
            options=[
                ft.DropdownOption(key="indigo", text="Índigo"),
                ft.DropdownOption(key="blue", text="Azul"),
                ft.DropdownOption(key="teal", text="Verde-azulado"),
                ft.DropdownOption(key="orange", text="Laranja"),
                ft.DropdownOption(key="purple", text="Roxo"),
            ],
            expand=True,
        )
        self._fonte = ft.Dropdown(
            label="Fonte",
            value=preferences.font_family,
            options=[
                ft.DropdownOption(key="Segoe UI", text="Segoe UI"),
                ft.DropdownOption(key="Arial", text="Arial"),
                ft.DropdownOption(key="Consolas", text="Consolas"),
                ft.DropdownOption(key="Roboto", text="Roboto"),
            ],
            expand=True,
        )

        card = ft.Container(
            content=ft.Column([
                ft.Text("Aparência", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                ft.ResponsiveRow([self._tema, self._cor, self._fonte], spacing=12),
                ft.Row([
                    ft.FilledButton("Aplicar", icon=ft.Icons.CHECK, on_click=self._salvar),
                    ft.OutlinedButton("Restaurar padrões", icon=ft.Icons.RESTART_ALT, on_click=self._restaurar),
                ]),
            ]),
            padding=16,
            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
            border_radius=8,
            bgcolor=ft.Colors.SURFACE_CONTAINER,
        )

        return ft.Column([
            ft.Text("Preferências", size=20, weight=ft.FontWeight.BOLD),
            ft.Text(
                "Personalize a aparência. As escolhas são preservadas nas próximas execuções.",
                size=13,
                color=ft.Colors.GREY_500,
            ),
            ft.Container(height=8),
            card,
        ], scroll=ft.ScrollMode.AUTO, expand=True)

    def _salvar(self, e: ft.ControlEvent) -> None:
        preferences = self._service.salvar(
            self._tema.value or "dark",
            self._cor.value or "indigo",
            self._fonte.value or "Segoe UI",
        )
        self._on_aplicar(preferences)
        self._on_mensagem("Preferências salvas e aplicadas.")

    def _restaurar(self, e: ft.ControlEvent) -> None:
        preferences = self._service.restaurar()
        self._tema.value = preferences.theme_mode
        self._cor.value = preferences.color_seed
        self._fonte.value = preferences.font_family
        self._on_aplicar(preferences)
        if self._tema.page:
            self._tema.page.update()
        self._on_mensagem("Preferências padrão restauradas.")
