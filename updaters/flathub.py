"""Updater para pacotes Flatpak/Flathub."""

import subprocess
from typing import Optional
from .generic import BaseUpdater, UpdateInfo


class FlatpakUpdater(BaseUpdater):
    def __init__(self, config: dict):
        super().__init__(config)
        self.flatpak_id = config.get("flatpak_id", "")
        self.check_installed = config.get("check_installed", True)

    def _run_flatpak(self, args: list) -> Optional[str]:
        """Executa um comando flatpak e retorna o stdout como texto."""
        try:
            result = subprocess.run(
                ["flatpak"] + args,
                capture_output=True,
                text=True,
                timeout=30,
            )
            if result.returncode != 0:
                return None
            return result.stdout.strip()
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.log(f"Erro ao executar flatpak: {e}")
            return None

    def _get_remote_version(self) -> Optional[str]:
        """Obtém a versão remota do flathub."""
        # Tenta com --system primeiro
        output = self._run_flatpak([
            "remote-info", "--system", "flathub", self.flatpak_id
        ])
        if output:
            version = self._parse_version_from_info(output)
            if version:
                return version

        # Tenta com --user
        output = self._run_flatpak([
            "remote-info", "--user", "flathub", self.flatpak_id
        ])
        if output:
            version = self._parse_version_from_info(output)
            if version:
                return version

        return None

    @staticmethod
    def _parse_version_from_info(output: str) -> Optional[str]:
        """Extrai a versão da saída do flatpak remote-info ou info.
        
        Funciona em qualquer idioma (procura por 'Version:', 'Versão:', etc.).
        """
        import re
        for line in output.splitlines():
            # Procura por padrões como "Versão: 159.0.1" ou "Version: 159.0.1"
            match = re.search(r'(?:version|versão)\s*:\s*([^\s]+)', line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None

    def _get_installed_version(self) -> Optional[str]:
        """Obtém a versão instalada localmente."""
        output = self._run_flatpak([
            "list", "--app", "--columns=name,version"
        ])
        if output:
            for line in output.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2 and parts[0] == self.flatpak_id:
                    return parts[1]
        return None

    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há atualização disponível no Flathub."""
        if not self.flatpak_id:
            self.log("Sem flatpak_id configurado")
            return None

        new_version = self._get_remote_version()
        if not new_version:
            self.log(f"Não foi possível obter versão remota para {self.flatpak_id}")
            return None

        current_version = self.get_current_version()
        installed_version = self._get_installed_version()

        if current_version is None and installed_version:
            current_version = installed_version

        if current_version == new_version:
            self.log(f"Já está na versão {new_version}")
            return None

        self.log(f"Nova versão disponível: {new_version} (atual: {current_version or 'desconhecida'})")

        return UpdateInfo(
            name=self.name,
            current_version=current_version,
            new_version=new_version,
            source="flathub",
            url=f"https://flathub.org/apps/{self.flatpak_id}",
            notes=f"Atualização do {self.flatpak_id} para versão {new_version}",
        )
