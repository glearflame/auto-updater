"""Updater para releases do GitHub."""

import urllib.request
import json
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class GitHubReleaseUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.owner = config.get("owner", "")
        self.repo = config.get("repo", "")
        self.asset_name = config.get("asset_name")
        self.check_installed = config.get("check_installed", False)

    def _api_request(self, url: str) -> Optional[dict]:
        """Faz uma requisição GET para a API do GitHub."""
        headers = {"User-Agent": "auto-updater/1.0"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            self.log(f"Erro na API do GitHub: {e}")
            return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há nova release no GitHub."""
        if not self.owner or not self.repo:
            self.log("Owner ou repo não configurado")
            return None

        url = f"https://api.github.com/repos/{self.owner}/{self.repo}/releases/latest"
        data = self._api_request(url)

        if not data:
            return None

        new_version = data.get("tag_name", "").lstrip("v")
        if not new_version:
            self.log("Não foi obter a tag da release")
            return None

        current_version = self.get_current_version()

        if current_version == new_version:
            self.log(f"Já está na versão {new_version}")
            return None

        # Busca asset específico se configurado
        asset_url = None
        asset_name_found = None
        if self.asset_name:
            for asset in data.get("assets", []):
                if asset.get("name") == self.asset_name:
                    asset_url = asset.get("browser_download_url")
                    asset_name_found = asset.get("name")
                    break

        self.log(f"Nova versão disponível: {new_version} (atual: {current_version})")

        return UpdateInfo(
            name=self.name,
            current_version=current_version,
            new_version=new_version,
            source="github_release",
            url=data.get("html_url", f"https://github.com/{self.owner}/{self.repo}/releases/latest"),
            notes=data.get("body", "")[:500] or f"Nova versão {new_version}",
            asset_name=asset_name_found,
            asset_url=asset_url,
            released_at=data.get("published_at"),
        )
