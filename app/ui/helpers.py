from __future__ import annotations

import flet as ft


def borda_all(cor=ft.Colors.GREY_700, largura: float = 1) -> ft.Border:
    side = ft.BorderSide(largura, cor)
    return ft.Border(left=side, top=side, right=side, bottom=side)


def padding_all(valor: float = 16) -> ft.Padding:
    return ft.Padding(left=valor, top=valor, right=valor, bottom=valor)
