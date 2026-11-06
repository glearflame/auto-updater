"""Classe base para updaters."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class UpdateInfo:
    """Informações sobre uma atualização encontrada."""
    name: str
    current_version: Optional[str]
    new_version: str
    source: str
    url: str
    notes: str = ""
    asset_name: Optional[str] = None
    asset_url: Optional[str] = None
    released_at: Optional[str] = None


class BaseUpdater(ABC):
    """Classe base para todos os updaters."""

    def __init__(self, config: dict):
        self.config = config
        self.name = config.get("name", "unknown")
        self.type = config.get("type", "generic")

    @abstractmethod
    def check(self) -> Optional[UpdateInfo]:
        """Verifica se há atualização disponível.
        
        Returns:
            UpdateInfo se houver atualização, None caso contrário.
        """
        pass

    def get_current_version(self) -> Optional[str]:
        """Lê a versão atualmente registrada localmente."""
        versions_dir = Path("versions")
        version_file = versions_dir / f"{self.name}.txt"
        if version_file.exists():
            return version_file.read_text().strip()
        return None

    def save_version(self, version: str) -> None:
        """Salva a versão localmente."""
        versions_dir = Path("versions")
        versions_dir.mkdir(exist_ok=True)
        version_file = versions_dir / f"{self.name}.txt"
        version_file.write_text(version)

    def log(self, message: str) -> None:
        """Log simples com prefixo do repositório."""
        print(f"[{self.name}] {message}")
