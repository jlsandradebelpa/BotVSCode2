from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

from config import Config
from git_tools import GitTools
from github_tools import list_open_issues
from historico import registrar as registrar_historico
from projetos import Projeto, ProjetosManager
from utils import resolve_full_path, saudacao
from vscode import open_vscode, is_vscode_installed


class Menu:
    MODE_START = 1
    MODE_END = 2

    def __init__(
        self, config: Config, projetos_manager: ProjetosManager
    ) -> None:
        self._config = config
        self._workspace_drive = config.workspace_drive
        self._manager = projetos_manager

    def _historico_pasta(self, projeto: Projeto) -> Optional[Path]:
        if self._config.historico_pasta:
            return Path(self._config.historico_pasta)
        if projeto.historico_pasta:
            return Path(projeto.historico_pasta)
        return None

    def _header(self) -> None:
        print("\n" + "=" * 40)
        print("\nBotVSCode")
        print("Assistente de Desenvolvimento\n")
        print("=" * 40)

    def _wait(self) -> None:
        input("\nPressione Enter para continuar...")

    def _confirm(self, msg: str) -> bool:
        resp = input(f"\n{msg} (S/n): ").strip().lower()
        return resp != "n"

    # --- Main Mode Selection ---------------------

    def run(self) -> bool:
        self._header()
        print(f"\n{saudacao()}\n")
        print("[1] Iniciar Trabalho")
        print("[2] Encerrar Trabalho")
        print("[0] Sair\n")

        try:
            choice = int(input("Opcao: "))
        except ValueError:
            print("\nOpcao invalida.")
            self._wait()
            return True

        if choice == 0:
            print("\nEncerrando BotVSCode.")
            return False

        if choice == self.MODE_START:
            projeto = self._select_project()
            if projeto:
                self._start_workflow(projeto)
            return True

        if choice == self.MODE_END:
            projeto = self._select_project()
            if projeto:
                self._end_workflow(projeto)
            return True

        print("\nOpcao invalida.")
        self._wait()
        return True

    # --- Project Selection -----------------------

    def _select_project(self) -> Optional[Projeto]:
        projetos = self._manager.projetos

        print("\nSelecione o projeto:\n")
        for i, projeto in enumerate(projetos, 1):
            print(f"{i} - {projeto.nome}")
        print("0 - Voltar\n")

        try:
            choice = int(input("Opcao: "))
        except ValueError:
            print("\nOpcao invalida.")
            self._wait()
            return None

        if choice == 0:
            return None

        if 1 <= choice <= self._manager.count:
            return self._manager.get_by_index(choice - 1)

        print("\nOpcao invalida.")
        self._wait()
        return None

    # --- Iniciar Trabalho ------------------------

    def _start_workflow(self, projeto: Projeto) -> None:
        caminho = resolve_full_path(self._workspace_drive, projeto.pasta)

        print(f"\n{'-' * 40}")
        print(f"  Iniciar Trabalho: {projeto.nome}")
        print(f"{'-' * 40}\n")

        if not caminho.exists():
            print(f"[ERRO] Caminho nao encontrado: {caminho}")
            self._wait()
            return

        git = GitTools(caminho)

        if not git.is_git_repo():
            print("[AVISO] O diretorio nao e um repositorio Git.")
            self._wait()
            return

        print(f"[OK] Repositorio Git encontrado em {caminho.name}\n")

        success, _ = git.fetch()
        if not success:
            print("[AVISO] Nao foi possivel conectar ao repositorio remoto.")
            print("       Continuando com dados locais.\n")
        else:
            print("[OK] Fetch realizado com sucesso.\n")

        status = git.get_branch_status()
        branch = git.get_current_branch()
        ahead = status.get("ahead", "?")
        behind = status.get("behind", "?")

        print(f"  Branch atual : {branch}")
        print(f"  Commits a frente  (local): {ahead}")
        print(f"  Commits atras      (remoto): {behind}")
        print()

        has_changes = git.has_uncommitted_changes()
        if has_changes:
            _, changes = git.status_short()
            print("[ATENCAO] Voce possui alteracoes locais nao commitadas:\n")
            for line in changes.split("\n"):
                if line.strip():
                    print(f"    {line}")
            print()
        else:
            print("[OK] Nenhuma alteracao local pendente.\n")

        if behind != "0" and behind != "?":
            if self._confirm("Deseja atualizar o projeto (git pull)?"):
                print()
                ok, out = git.pull(branch)
                if ok:
                    print(f"[OK] Pull realizado com sucesso.\n{out}")
                else:
                    print(f"[FALHA] Erro ao executar pull:\n{out}")
                print()
        else:
            print("[OK] Projeto ja esta atualizado.\n")

        if is_vscode_installed():
            if self._confirm("Deseja abrir o VS Code?"):
                print()
                if open_vscode(caminho):
                    print("[OK] VS Code aberto com sucesso.")
                else:
                    print("[FALHA] Nao foi possivel abrir o VS Code.")
        else:
            print("[AVISO] VS Code nao encontrado no PATH.")
            print("       Instale o VS Code e adicione 'code' ao PATH.\n")

        registrar_historico("Git", f"Projeto iniciado e sincronizado: {projeto.nome}", self._historico_pasta(projeto))

        if projeto.github_repo:
            self._list_pending_tasks(projeto)

        print(f"\n{saudacao()} Ambiente pronto para desenvolvimento!\n")
        self._wait()

    # --- Tarefas Pendentes -----------------------

    def _list_pending_tasks(self, projeto: Projeto) -> None:
        print(f"[...] Consultando tarefas pendentes em {projeto.github_repo} ...\n")
        issues = list_open_issues(projeto.github_repo)
        if issues is None:
            print("[AVISO] Nao foi possivel consultar o GitHub.")
            print("       Verifique sua conexao e a autenticacao do GitHub CLI: gh auth status.\n")
            registrar_historico(
                "GitHub Issues", f"Falha ao consultar tarefas de {projeto.github_repo}", self._historico_pasta(projeto)
            )
            return
        if len(issues) == 0:
            print("[OK] Nenhuma tarefa pendente encontrada para este projeto.\n")
            registrar_historico(
                "GitHub Issues",
                f"Nenhuma tarefa pendente em {projeto.github_repo}",
                self._historico_pasta(projeto),
            )
            return
        print(f"Tarefas pendentes ({len(issues)}):\n")
        for issue in issues:
            numero = issue.get("number", "?")
            titulo = issue.get("title", "Sem titulo")
            print(f"  #{numero} - {titulo}")
        print()
        registrar_historico(
            "GitHub Issues",
            f"Listadas {len(issues)} tarefas pendentes de {projeto.github_repo}",
            self._historico_pasta(projeto),
        )

    # --- Encerrar Trabalho -----------------------

    def _end_workflow(self, projeto: Projeto) -> None:
        caminho = resolve_full_path(self._workspace_drive, projeto.pasta)

        print(f"\n{'-' * 40}")
        print(f"  Encerrar Trabalho: {projeto.nome}")
        print(f"{'-' * 40}\n")

        if not caminho.exists():
            print(f"[ERRO] Caminho nao encontrado: {caminho}")
            self._wait()
            return

        git = GitTools(caminho)

        if not git.is_git_repo():
            print("[AVISO] O diretorio nao e um repositorio Git.")
            self._wait()
            return

        has_changes = git.has_uncommitted_changes()
        if not has_changes:
            print("[OK] Nenhuma alteracao para commitar.\n")

            branch = git.get_current_branch()
            ok, out = git.push(branch)
            if not ok:
                registrar_historico("Git", f"Falha ao sincronizar {projeto.nome}: push falhou", self._historico_pasta(projeto))
                print(f"[FALHA] Erro ao executar push:\n{out}")
            else:
                registrar_historico("Git", f"Trabalho encerrado: {projeto.nome} sincronizado (sem alteracoes)", self._historico_pasta(projeto))
                print(f"[OK] Push realizado. Branch {branch} sincronizada.")
            self._wait()
            return

        print("[ATENCAO] Alteracoes locais encontradas:\n")
        _, changes = git.status_short()
        for line in changes.split("\n"):
            if line.strip():
                print(f"    {line}")
        print()

        if not self._confirm("Deseja commitar e enviar as alteracoes?"):
            print("\nAlteracoes nao foram enviadas. Lembre-se de commit-las depois.")
            self._wait()
            return

        print()
        msg = input("Mensagem do commit: ").strip()
        while not msg:
            print("A mensagem nao pode estar vazia.")
            msg = input("Mensagem do commit: ").strip()

        print()
        ok, out = git.stage_all()
        if not ok:
            print(f"[FALHA] Erro ao preparar alteracoes para commit:\n{out}")
            self._wait()
            return

        ok, out = git.commit(msg)
        if not ok:
            print(f"[FALHA] Erro ao executar commit:\n{out}")
            self._wait()
            return
        registrar_historico("Git", f"Commit realizado em {projeto.nome}: {msg}", self._historico_pasta(projeto))
        print(f"[OK] Commit realizado com sucesso.\n")

        branch = git.get_current_branch()
        print("Enviando para o GitHub...\n")
        ok, out = git.push(branch)
        if not ok:
            registrar_historico("Git", f"Falha ao fazer push de {projeto.nome} apos commit", self._historico_pasta(projeto))
            print(f"[FALHA] Erro ao executar push:\n{out}")
            self._wait()
            return

        registrar_historico("Git", f"Trabalho encerrado: {projeto.nome} commitado e enviado", self._historico_pasta(projeto))
        print(f"[OK] Push realizado com sucesso.")
        print(f"[OK] Projeto {projeto.nome} sincronizado com o GitHub.\n")
        print("Voce pode continuar o desenvolvimento em outro computador.\n")
        self._wait()
