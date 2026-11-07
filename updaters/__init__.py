from .generic import BaseUpdater, UpdateInfo
from .flathub import FlatpakUpdater
from .github_releases import GitHubReleaseUpdater
from .pypi import PyPIUpdater
from .npm import NPMUpdater
from .dockerhub import DockerHubUpdater
from .arch import AURUpdater

__all__ = ["BaseUpdater", "UpdateInfo", "FlatpakUpdater", "GitHubReleaseUpdater",
           "PyPIUpdater", "NPMUpdater", "DockerHubUpdater", "AURUpdater"]

UPDATER_MAP = {
    "flathub": FlatpakUpdater,
    "github_release": GitHubReleaseUpdater,
    "pypi": PyPIUpdater,
    "npm": NPMUpdater,
    "dockerhub": DockerHubUpdater,
    "arch": AURUpdater,
}

def get_updater(repo_config: dict) -> BaseUpdater:
    """Retorna a instância do updater baseado no tipo configurado."""
    updater_type = repo_config.get("type", "github_release")
    cls = UPDATER_MAP.get(updater_type)
    if not cls:
        raise ValueError(f"Tipo de updater desconhecido: {updater_type}")
    return cls(repo_config)
