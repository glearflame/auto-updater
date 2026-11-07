"""Updater para pacotes AUR (Arch Linux)."""

import subprocess
import json
import urllib.request
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class AURUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.package_name = config.get("package_name", "")

    def _run_command(self, cmd: list) -> Optional[str]:
        """Executa um comando e retorna o stdout."""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return None
            return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.log(f"Erro ao executar comando: {e}")
            return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há nova versão no AUR."""
        if not self.package_name:
            self.log("Sem package_name configurado")
            return None

        # Tenta obter versão via aur-ver ou curl no AUR
        url = f"https://aur.archlinux.org/rpc/?v=5&type=info&arg[]={self.package_name}"
        try:
            import urllib.request
            req = urllib.request.Request(url, headers={"User-Agent": "auto-updater/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode())
        except Exception as e:
            self.log(f"Erro ao consultar AUR: {e}")
            return None

        results = data.get("results", [])
        if not results:
            self.log(f"Pacote {self.package_name} não encontrado no AUR")
            return None

        new_version = results[0].get("Version", "")
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
            source="aur",
            url=f"https://aur.archlinux.org/packages/{self.package_name}",
            notes=f"Nova versão {new_version} do pacote AUR {self.package_name}",
        )
