from __future__ import annotations

import flet as ft


def aplicar_tema(page: ft.Page) -> None:
    page.theme_mode = ft.ThemeMode.DARK
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.INDIGO,
    )
    page.bgcolor = ft.Colors.GREY_900
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
