from __future__ import annotations

import flet as ft

from preferences import Preferences


CORES = {
    "indigo": ft.Colors.INDIGO,
    "blue": ft.Colors.BLUE,
    "teal": ft.Colors.TEAL,
    "orange": ft.Colors.DEEP_ORANGE,
    "purple": ft.Colors.PURPLE,
}


def aplicar_tema(page: ft.Page, preferences: Preferences) -> None:
    modos = {
        "dark": ft.ThemeMode.DARK,
        "light": ft.ThemeMode.LIGHT,
        "system": ft.ThemeMode.SYSTEM,
    }
    page.theme_mode = modos.get(preferences.theme_mode, ft.ThemeMode.DARK)
    page.theme = ft.Theme(
        color_scheme_seed=CORES.get(preferences.color_seed, ft.Colors.INDIGO),
        font_family=preferences.font_family,
    )
    page.bgcolor = None
    page.horizontal_alignment = ft.CrossAxisAlignment.STRETCH
