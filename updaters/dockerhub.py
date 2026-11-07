"""Updater para imagens Docker Hub."""

import json
import urllib.request
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class DockerHubUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.repository = config.get("repository", "")  # ex: "library/nginx"

    def _api_request(self, url: str) -> Optional[dict]:
        """Faz uma requisição GET para a API do Docker Hub."""
        headers = {"User-Agent": "auto-updater/1.0"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            self.log(f"Erro na API do Docker Hub: {e}")
            return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há nova tag no Docker Hub."""
        if not self.repository:
            self.log("Sem repository configurado")
            return None

        url = f"https://registry.hub.docker.com/v2/repositories/{self.repository}/tags/latest"
        data = self._api_request(url)

        if not data:
            return None

        new_version = data.get("name", "")
        if not new_version:
            self.log("Não foi possível obter a versão")
            return None

        current_version = self.get_current_version()

        if current_version == new_version:
            self.log(f"Já está na versão {new_version}")
            return None

        self.log(f"Nova versão disponível: {new_version} (atual: {current_version})")

        return UpdateInfo(
            name=self.name,
            current_version=current_version,
            new_version=new_version,
            source="dockerhub",
            url=f"https://hub.docker.com/r/{self.repository}",
            notes=f"Nova versão {new_version} da imagem Docker {self.repository}",
        )
