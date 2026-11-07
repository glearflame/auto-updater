# Changelog - Auto-Updater

## v1.0.0 (2026-10-30)

### Novos recursos
- Suporte a 5 fontes diferentes: GitHub Releases, Flathub, PyPI, npm, Docker Hub, AUR
- Detecção automática de novas versões
- Salvamento de versões locais em `versions/`
- Geração automática de CHANGELOG.md
- Commit e push automático no GitHub
- Preparação de post para Reddit (`reddit_post.md`)
- Suporte a múltiplos repositórios no `config.yaml`

### Mudanças
- Adicionado suporte a PyPI (pacotes Python)
- Adicionado suporte a npm (pacotes Node.js)
- Adicionado suporte a Docker Hub (imagens de container)
- Adicionado suporte a AUR (Arch Linux User Repository)
- Corrigido parsing de versão do Flatpak (suporte a múltiplos idiomas: PT, EN, etc.)
- Adicionado script `run_daily.sh` para execução via cron
- Adicionado exemplo de crontab

### Repositórios monitorados (20 no total)

**GitHub Releases (8):**
- despertador, pentest-kit, My-system-auto-analise-, bot-de-vendas-, topdirs, price-radar-br, auto-updater, site-de-videos

**Flatpak (15):**
- org.gnome.Notes, com.spotify.Client, org.mozilla.firefox, org.chromium.Chromium, com.valvesoftware.Steam, org.libreoffice.LibreOffice, org.videolan.VLC, org.gimp.GIMP, org.inkscape.Inkscape, com.discordapp.Discord, com.slack.Slack, org.telegram.desktop, net.lutris.Lutris, org.winehq.Wine

**PyPI (4):**
- requests, flask, django, numpy, pandas

**npm (4):**
- vue, react, typescript, eslint

**Docker Hub (5):**
- nginx, postgres, redis, ubuntu, alpine

**AUR (2):**
- yay, google-chrome
