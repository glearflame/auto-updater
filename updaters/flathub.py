"""Updater para pacotes Flatpak/Flathub."""

import subprocess
import json
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class FlatpakUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.flatpak_id = config.get("flatpak_id", "")
        self.check_installed = config.get("check_installed", True)

    def _run_flatpak(self, args: list) -> Optional[dict]:
        """Executa um comando flatpak e retorna o JSON parseado."""
        try:
            result = subprocess.run(
                ["flatpak"] + args,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                self.log(f"flatpak falhou: {result.stderr.strip()}")
                return None
            if not result.stdout.strip():
                return None
            return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
            self.log(f"Erro ao executar flatpak: {e}")
            return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há atualização disponível no Flathub."""
        if not self.flatpak_id:
            self.log("Sem flatpak_id configurado")
            return None

        remote_info = self._run_flatpak([
            "remote-info", "--columns=name,version,application",
            "flathub", self.flatpak_id
        ])

        new_version = None
        if remote_info and isinstance(remote_info, list):
            for item in remote_info:
                if item.get("application") == self.flatpak_id:
                    new_version = item.get("version")
                    break

        if not new_version:
            installed = self._run_flatpak([
                "list", "--columns=name,application,version",
                "--user", "--system"
            ])
            if installed:
                for item in installed:
                    if item.get("application") == self.flatpak_id:
                        new_version = item.get("version")
                        break

        if not new_version:
            self.log(f"Não foi possível obter versão para {self.flatpak_id}")
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
            source="flathub",
            url=f"https://flathub.org/apps/{self.flatpak_id}",
            notes=f"Atualização do {self.flatpak_id} para versão {new_version}",
        )
