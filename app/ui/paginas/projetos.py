from __future__ import annotations

from typing import Callable, Optional

import flet as ft

from projetos import Projeto
from services.project_service import ProjectService


class ProjetosPage:
    def __init__(self, project_service: ProjectService) -> None:
        self._service = project_service
        self._indice_edicao: Optional[int] = None
        self._on_mensagem: Callable[[str], None] = lambda msg: None
        self._on_projeto_selecionado: Callable[[Optional[Projeto]], None] = lambda p: None

    def definir_on_mensagem(self, callback: Callable[[str], None]) -> None:
        self._on_mensagem = callback

    def definir_on_projeto_selecionado(self, callback: Callable[[Optional[Projeto]], None]) -> None:
        self._on_projeto_selecionado = callback

    def construir(self) -> ft.Control:
        self._lista_container = ft.Column(spacing=4)
        self._carregar_lista()

        self._txt_nome = ft.TextField(label="Nome", hint_text="Nome do projeto", expand=True)
        self._txt_pasta = ft.TextField(label="Pasta Local", hint_text="Caminho completo ou relativo ao workspace", expand=True)

        self._txt_branch = ft.TextField(label="Branch", hint_text="main", expand=True)
        self._txt_linguagem = ft.TextField(label="Linguagem", hint_text="ADVPL, Python, ...", expand=True)
        self._txt_github = ft.TextField(label="GitHub", hint_text="user/repo (opcional)", expand=True)
        self._txt_historico = ft.TextField(label="Pasta Histórico", hint_text="Caminho (opcional)", expand=True)

        self._btn_salvar = ft.ElevatedButton(
            "Salvar",
            icon=ft.Icons.SAVE,
            on_click=self._ao_salvar,
        )
        self._btn_limpar = ft.OutlinedButton(
            "Novo",
            icon=ft.Icons.ADD,
            on_click=self._ao_novo,
        )
        self._btn_remover = ft.OutlinedButton(
            "Remover",
            icon=ft.Icons.DELETE,
            on_click=self._ao_remover,
        )

        lista_card = ft.Container(
            content=ft.Column([
                ft.Text("Lista de Projetos", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                self._lista_container,
            ]),
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
            border_radius=8,
            bgcolor=ft.Colors.GREY_800,
            expand=True,
        )

        form_card = ft.Container(
            content=ft.Column([
                ft.Text("Configuração", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(height=1, color=ft.Colors.GREY_700),
                self._txt_nome,
                self._txt_pasta,
                self._txt_branch,
                self._txt_linguagem,
                self._txt_github,
                self._txt_historico,
                ft.Container(height=8),
                ft.Row([self._btn_limpar, self._btn_salvar, self._btn_remover]),
            ]),
            padding=ft.Padding(left=16, top=16, right=16, bottom=16),
            border=ft.Border(left=ft.BorderSide(1, ft.Colors.GREY_700), top=ft.BorderSide(1, ft.Colors.GREY_700), right=ft.BorderSide(1, ft.Colors.GREY_700), bottom=ft.BorderSide(1, ft.Colors.GREY_700)),
            border_radius=8,
            bgcolor=ft.Colors.GREY_800,
            expand=True,
        )

        return ft.Row([
            lista_card,
            ft.Container(width=16),
            form_card,
        ], expand=True)

    def _carregar_lista(self) -> None:
        self._lista_container.controls.clear()
        projetos = self._service.projetos
        if not projetos:
            self._lista_container.controls.append(
                ft.Text("Nenhum projeto cadastrado.", color=ft.Colors.GREY_500, italic=True)
            )
        for i, p in enumerate(projetos):
            tile = ft.ListTile(
                title=ft.Text(p.nome),
                subtitle=ft.Text(f"{p.pasta} | {p.branch}", size=12, color=ft.Colors.GREY_400),
                on_click=lambda _, idx=i: self._selecionar(idx),
            )
            self._lista_container.controls.append(tile)
        try:
            if self._lista_container.page:
                self._lista_container.update()
        except RuntimeError:
            pass

    def _selecionar(self, index: int) -> None:
        projeto = self._service.get_by_index(index)
        if not projeto:
            return
        self._indice_edicao = index
        self._txt_nome.value = projeto.nome
        self._txt_pasta.value = projeto.pasta
        self._txt_branch.value = projeto.branch
        self._txt_linguagem.value = projeto.linguagem
        self._txt_github.value = projeto.github_repo or ""
        self._txt_historico.value = projeto.historico_pasta or ""
        if self._txt_nome.page:
            self._txt_nome.page.update()
        self._on_projeto_selecionado(projeto)

    def _ao_novo(self, e: ft.ControlEvent) -> None:
        self._indice_edicao = None
        self._txt_nome.value = ""
        self._txt_pasta.value = ""
        self._txt_branch.value = "main"
        self._txt_linguagem.value = ""
        self._txt_github.value = ""
        self._txt_historico.value = ""
        if self._txt_nome.page:
            self._txt_nome.page.update()

    def _ao_salvar(self, e: ft.ControlEvent) -> None:
        nome = self._txt_nome.value.strip()
        pasta = self._txt_pasta.value.strip()
        branch = self._txt_branch.value.strip()
        linguagem = self._txt_linguagem.value.strip()
        github = self._txt_github.value.strip()
        historico = self._txt_historico.value.strip()

        if not nome:
            self._mensagem("O campo Nome é obrigatório.")
            return
        if not pasta:
            self._mensagem("O campo Pasta é obrigatório.")
            return

        if self._indice_edicao is not None:
            ok, msg = self._service.editar(self._indice_edicao, nome, pasta, branch, linguagem, github, historico)
        else:
            ok, msg = self._service.adicionar(nome, pasta, branch, linguagem, github, historico)

        self._mensagem(msg)
        self._carregar_lista()
        if ok:
            projetos = self._service.projetos
            for p in projetos:
                if p.nome == nome:
                    self._on_projeto_selecionado(p)
                    break

    def _ao_remover(self, e: ft.ControlEvent) -> None:
        if self._indice_edicao is None:
            self._mensagem("Selecione um projeto para remover.")
            return
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmar remoção"),
            content=ft.Text(f"Remover o projeto '{self._txt_nome.value}'?"),
            actions=[
                ft.TextButton("Sim", on_click=lambda ev: self._confirmar_remocao(ev)),
                ft.TextButton("Não", on_click=lambda ev: ev.control.page.pop_dialog()),
            ],
        )
        e.page.show_dialog(dlg)

    def _confirmar_remocao(self, e: ft.ControlEvent) -> None:
        e.page.pop_dialog()
        if self._indice_edicao is not None:
            ok, msg = self._service.remover(self._indice_edicao)
            self._mensagem(msg)
            self._ao_novo(e)
            self._carregar_lista()
            self._on_projeto_selecionado(None)

    def _mensagem(self, texto: str) -> None:
        self._on_mensagem(texto)
