from __future__ import annotations

import flet as ft

from services.historico_service import HistoricoService


class AtividadesPage:
    def __init__(self, historico_service: HistoricoService) -> None:
        self._historico_service = historico_service

    def construir(self) -> ft.Control:
        registros = self._historico_service.listar()

        if not registros:
            return ft.Column([
                ft.Text("Histórico de Atividades", size=18, weight=ft.FontWeight.BOLD),
                ft.Container(height=16),
                ft.Text("Nenhuma atividade registrada hoje.", color=ft.Colors.GREY_500, italic=True),
            ])

        linhas = [
            ft.DataRow(cells=[
                ft.DataCell(ft.Text(r.get("sequencia", ""), size=12)),
                ft.DataCell(ft.Text(r.get("hora", ""), size=12)),
                ft.DataCell(ft.Text(r.get("tipo", ""), size=12)),
                ft.DataCell(ft.Text(r.get("descricao", ""), size=12)),
            ]) for r in reversed(registros)
        ]

        tabela = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("#", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Hora", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Tipo", weight=ft.FontWeight.BOLD)),
                ft.DataColumn(ft.Text("Descricao", weight=ft.FontWeight.BOLD)),
            ],
            rows=linhas,
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
            border_radius=8,
            heading_row_color=ft.Colors.GREY_800,
            data_row_color=ft.Colors.GREY_900,
        )

        return ft.Column([
            ft.Text("Histórico de Atividades", size=18, weight=ft.FontWeight.BOLD),
            ft.Text("Somente leitura — registros do dia atual.", size=13, color=ft.Colors.GREY_500),
            ft.Container(height=16),
            ft.Container(
                content=ft.Column([tabela], scroll=ft.ScrollMode.AUTO),
                border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
                border_radius=8,
                bgcolor=ft.Colors.GREY_800,
                padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            ),
        ], scroll=ft.ScrollMode.AUTO)
