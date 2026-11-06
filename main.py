#!/usr/bin/env python3
"""Auto-updater - Verifica e publica atualizações de pacotes."""

import argparse
import os
import sys
import yaml
from pathlib import Path
from datetime import datetime

from updaters import get_updater
from publishers import GitHubPublisher, RedditPublisher


def load_config(config_path: str = "config.yaml") -> dict:
    """Carrega o arquivo de configuração YAML."""
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_env(env_path: str = ".env") -> None:
    """Carrega variáveis de ambiente de um arquivo .env."""
    if not Path(env_path).exists():
        print(f"Arquivo {env_path} não encontrado. Usando variáveis de ambiente do sistema.")
        return

    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip())


def run(dry_run: bool = False, push: bool = False, prepare_reddit: bool = False) -> None:
    """Executa o ciclo completo de atualização."""
    config = load_config()
    load_env()

    repos = config.get("repositories", [])
    settings = config.get("settings", {})

    print(f"=== Auto-Updater iniciado - {datetime.now().isoformat()} ===")
    print(f"Repositórios a verificar: {len(repos)}")
    print()

    updates = []

    for repo_config in repos:
        name = repo_config.get("name", "desconhecido")
        try:
            updater = get_updater(repo_config)
            update_info = updater.check()

            if update_info:
                updates.append(update_info)
                updater.save_version(update_info.new_version)
                print(f"  ✅ {name}: {update_info.current_version or 'novo'} → {update_info.new_version}")
            else:
                print(f"  ✓ {name}: já está atualizado")
        except Exception as e:
            print(f"  ✗ {name}: erro - {e}")

    print()
    print(f"Total de atualizações encontradas: {len(updates)}")

    if not updates:
        print("Nada para atualizar. Encerrando.")
        return

    # Salva CHANGELOG
    changelog_path = Path("CHANGELOG.md")
    changelog_lines = [f"# Changelog - {datetime.now().strftime('%Y-%m-%d %H:%M')}", ""]
    for u in updates:
        changelog_lines.append(f"## {u.name} - {u.new_version}")
        changelog_lines.append(f"- Fonte: {u.source}")
        changelog_lines.append(f"- Anterior: {u.current_version or 'novo'}")
        if u.url:
            changelog_lines.append(f"- Link: {u.url}")
        if u.notes:
            changelog_lines.append(f"- Notas: {u.notes[:200]}")
        changelog_lines.append("")

    changelog_path.write_text("\n".join(changelog_lines), encoding="utf-8")
    print(f"CHANGELOG atualizado: {changelog_path}")

    # Publicação
    if not dry_run:
        # GitHub
        gh_publisher = GitHubPublisher({
            **settings,
            "repo_path": os.environ.get("REPO_PATH", "."),
        })
        if gh_publisher.is_configured():
            print("\n--- Publicando no GitHub ---")
            gh_publisher.publish(updates)
        else:
            print("\n--- GitHub não configurado (pulando push) ---")
            print("  Configure GITHUB_TOKEN, GITHUB_USER e GITHUB_EMAIL no .env")

        # Reddit
        if prepare_reddit:
            reddit_publisher = RedditPublisher(settings)
            if reddit_publisher.is_configured():
                print("\n--- Preparando post para Reddit ---")
                reddit_publisher.publish(updates)
            else:
                print("\n--- Reddit desabilitado ---")
    else:
        print("\n--- Modo dry-run: nenhuma alteração foi feita ---")


def main():
    parser = argparse.ArgumentParser(description="Auto-updater para pacotes Flathub e GitHub")
    parser.add_argument("--dry-run", action="store_true", help="Executa sem fazer alterações")
    parser.add_argument("--push", action="store_true", help="Faz commit e push no GitHub")
    parser.add_argument("--prepare-reddit", action="store_true", help="Prepara post para Reddit")
    parser.add_argument("--config", default="config.yaml", help="Caminho para o config.yaml")
    args = parser.parse_args()

    run(
        dry_run=args.dry_run,
        push=args.push,
        prepare_reddit=args.prepare_reddit,
    )


if __name__ == "__main__":
    main()
