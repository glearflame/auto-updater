"""Publicador para GitHub - commit, push e tag."""

import os
import subprocess
from typing import List, Optional
from updaters.generic import UpdateInfo


class GitHubPublisher:
    def __init__(self, config: dict):
        self.config = config
        self.token = os.environ.get("GITHUB_TOKEN", "")
        self.user = os.environ.get("GITHUB_USER", "")
        self.email = os.environ.get("GITHUB_EMAIL", "")
        self.repo_owner = config.get("update_repo_owner", "glearflame")
        self.repo_name = config.get("update_repo_name", "auto-updater-releases")
        self.auto_push = config.get("auto_push", True)
        self.create_tag = config.get("create_github_tag", True)
        self.versions_dir = config.get("versions_dir", "versions")

    def is_configured(self) -> bool:
        return bool(self.token and self.user and self.email)

    def _run_git(self, args: list, cwd: str = None) -> tuple:
        """Executa um comando git e retorna (returncode, stdout, stderr)."""
        result = subprocess.run(
            ["git"] + args,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=60,
        )
        return result.returncode, result.stdout, result.stderr

    def publish(self, updates: list) -> bool:
        """Faz commit das novas versões no repositório do GitHub."""
        if not self.is_configured():
            print("GitHub não configurado (falta GITHUB_TOKEN/GITHUB_USER/GITHUB_EMAIL)")
            return False

        repo_path = self.config.get("repo_path", ".")

        # Configura usuário do git
        self._run_git(["config", "user.name", self.user], cwd=repo_path)
        self._run_git(["config", "user.email", self.email], cwd=repo_path)

        # Verifica status
        rc, stdout, _ = self._run_git(["status", "--porcelain"], cwd=repo_path)
        if rc != 0:
            print(f"Erro ao verificar status do git: {stdout}")
            return False

        if not stdout.strip():
            print("Nenhuma mudança para commitar")
            return True

        # Adiciona todos os arquivos de versão alterados
        self._run_git(["add", self.versions_dir], cwd=repo_path)

        # Monta mensagem de commit
        update_lines = []
        for u in updates:
            line = f"- {u.name}: {u.current_version or 'novo'} → {u.new_version}"
            update_lines.append(line)

        commit_message = f"""chore: atualização de versões

{chr(10).join(update_lines)}

Gerado automaticamente pelo auto-updater."""

        # Commit
        rc, stdout, stderr = self._run_git(
            ["commit", "-m", commit_message], cwd=repo_path
        )
        if rc != 0:
            print(f"Erro no commit: {stderr}")
            return False

        print(f"Commit realizado: {stdout.strip()}")

        # Push
        if self.auto_push:
            rc, stdout, stderr = self._run_git(["push"], cwd=repo_path)
            if rc != 0:
                print(f"Erro no push: {stderr}")
                return False
            print("Push realizado com sucesso")

            # Cria tag se configurado
            if self.create_tag and updates:
                latest = updates[-1]
                tag_name = f"{latest.name}-{latest.new_version}"
                rc, stdout, stderr = self._run_git(
                    ["tag", tag_name], cwd=repo_path
                )
                if rc == 0:
                    self._run_git(["push", "tags"], cwd=repo_path)
                    print(f"Tag {tag_name} criada")
                else:
                    print(f"Erro ao criar tag: {stderr}")

        return True
