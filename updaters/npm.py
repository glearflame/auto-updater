"""Updater para pacotes npm."""

import json
import urllib.request
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class NPMUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.package_name = config.get("package_name", "")

    def _api_request(self, url: str) -> Optional[dict]:
        """Faz uma requisição GET para a API do npm."""
        headers = {"User-Agent": "auto-updater/1.0"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            self.log(f"Erro na API do npm: {e}")
            return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há nova versão no npm."""
        if not self.package_name:
            self.log("Sem package_name configurado")
            return None

        url = f"https://registry.npmjs.org/{self.package_name}"
        data = self._api_request(url)

        if not data:
            return None

        new_version = data.get("dist-tags", {}).get("latest", "")
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
            source="npm",
            url=f"https://www.npmjs.com/package/{self.package_name}",
            notes=f"Nova versão {new_version} do pacote npm {self.package_name}",
        )
