"""Updater para pacotes PyPI."""

import json
import urllib.request
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class PyPIUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.package_name = config.get("package_name", "")

    def _api_request(self, url: str) -> Optional[dict]:
        """Faz uma requisição GET para a API do PyPI."""
        headers = {"User-Agent": "auto-updater/1.0"}
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode())
        except Exception as e:
            self.log(f"Erro na API do PyPI: {e}")
            return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há nova versão no PyPI."""
        if not self.package_name:
            self.log("Sem package_name configurado")
            return None

        url = f"https://pypi.org/pypi/{self.package_name}/json"
        data = self._api_request(url)

        if not data:
            return None

        info = data.get("info", {})
        new_version = info.get("version", "")
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
            source="pypi",
            url=f"https://pypi.org/project/{self.package_name}/",
            notes=f"Nova versão {new_version} do pacote PyPI {self.package_name}",
        )
