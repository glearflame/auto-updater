"""Preparador de post para Reddit (não publica automaticamente por segurança)."""

from typing import List
from updaters.generic import UpdateInfo


class RedditPublisher:
    def __init__(self, config: dict):
        self.config = config
        self.enabled = config.get("prepare_reddit_post", True)
        self.output_file = "reddit_post.md"

    def is_configured(self) -> bool:
        return bool(self.enabled)

    def publish(self, updates: list) -> bool:
        """Gera um arquivo markdown pronto para post no Reddit."""
        if not self.enabled:
            return False

        if not updates:
            return False

        lines = []
        lines.append("# Atualizações de Pacotes - Auto-Updater")
        lines.append("")
        lines.append("Olá pessoal! Atualizei alguns pacotes e queria compartilhar com vocês:")
        lines.append("")

        for u in updates:
            lines.append(f"## {u.name}")
            lines.append("")
            lines.append(f"- **Versão anterior:** {u.current_version or 'não instalada'}")
            lines.append(f"- **Nova versão:** {u.new_version}")
            lines.append(f"- **Fonte:** {u.source}")
            if u.url:
                lines.append(f"- **Link:** {u.url}")
            if u.notes:
                lines.append(f"- **Notas:** {u.notes[:300]}")
            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("Atualizações geradas automaticamente pelo [auto-updater](https://github.com/glearflame/auto-updater).")
        lines.append("")
        lines.append("Se você usa algum desses pacotes, vale a pena atualizar! 🚀")

        content = "\n".join(lines)

        with open(self.output_file, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"Post para Reddit salvo em: {self.output_file}")
        return True
