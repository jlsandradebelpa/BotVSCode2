from __future__ import annotations

import flet as ft


class ConfiguracoesPage:
    def construir(self) -> ft.Control:
        return ft.Column([
            ft.Text("Configurações", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Campos reservados para as próximas fases.", size=13, color=ft.Colors.GREY_500),
            ft.Container(height=16),

            ft.Container(
                content=ft.Column([
                    ft.Text("VS Code", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.GREY_700),
                    ft.TextField(label="Caminho do VS Code", hint_text="code (PATH)", read_only=True),
                ]),
                padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
                border_radius=8,
                bgcolor=ft.Colors.GREY_800,
            ),
            ft.Container(height=12),

            ft.Container(
                content=ft.Column([
                    ft.Text("Git", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.GREY_700),
                    ft.TextField(label="Nome do usuário Git", hint_text="user.name", read_only=True),
                    ft.TextField(label="Email do usuário Git", hint_text="user.email", read_only=True),
                ]),
                padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
                border_radius=8,
                bgcolor=ft.Colors.GREY_800,
            ),
            ft.Container(height=12),

            ft.Container(
                content=ft.Column([
                    ft.Text("GitHub", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.GREY_700),
                    ft.TextField(label="Token GitHub", hint_text="ghp_...", password=True, read_only=True),
                ]),
                padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
                border_radius=8,
                bgcolor=ft.Colors.GREY_800,
            ),
            ft.Container(height=12),

            ft.Container(
                content=ft.Column([
                    ft.Text("Aparência", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.GREY_700),
                    ft.Text("Preferências visuais disponíveis na aba Preferências.", size=13, color=ft.Colors.PRIMARY),
                ]),
                padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
                border_radius=8,
                bgcolor=ft.Colors.GREY_800,
            ),
            ft.Container(height=12),

            ft.Container(
                content=ft.Column([
                    ft.Text("Histórico", size=16, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=1, color=ft.Colors.GREY_700),
                    ft.TextField(label="Pasta de histórico", hint_text="C:/projetos/historico_atividades", read_only=True),
                ]),
                padding=ft.Padding(left=16, top=16, right=16, bottom=16),
                border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
                border_radius=8,
                bgcolor=ft.Colors.GREY_800,
            ),
        ], scroll=ft.ScrollMode.AUTO)
