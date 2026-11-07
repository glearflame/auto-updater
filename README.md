# Auto-Updater

Sistema automatizado para verificar e publicar atualizações de pacotes de diferentes fontes com publicação automática no GitHub e preparação para Reddit.

## Fontes suportadas

| Fonte | Tipo | O que monitora |
|-------|------|----------------|
| GitHub Releases | `github_release` | Novas tags/releases de repositórios |
| Flathub | `flathub` | Novas versões de pacotes Flatpak |
| PyPI | `pypi` | Novas versões de pacotes Python |
| npm | `npm` | Novas versões de pacotes Node.js |
| Docker Hub | `dockerhub` | Novas tags de imagens Docker |
| AUR | `arch` | Novas versões de pacotes Arch Linux |

## Estrutura

```
auto-updater/
├── main.py              # Ponto de entrada
├── config.yaml          # Configuração de repositórios e fontes
├── requirements.txt     # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
├── .gitignore           # Arquivos ignorados pelo git
├── CHANGELOG.md         # Registro de atualizações automáticas
├── crontab.example      # Exemplo de crontab
├── run_daily.sh         # Script para execução via cron
├── updaters/            # Lógica de verificação por fonte
│   ├── __init__.py
│   ├── generic.py       # Classe base
│   ├── flathub.py       # Flatpak/Flathub
│   ├── github_releases.py # GitHub Releases
│   ├── pypi.py          # PyPI
│   ├── npm.py           # npm
│   ├── dockerhub.py     # Docker Hub
│   └── arch.py          # AUR (Arch Linux)
├── publishers/          # Publicação de resultados
│   ├── __init__.py
│   ├── github.py        # Commit e push no GitHub
│   └── reddit.py        # Preparação para post no Reddit
└── versions/            # Versões salvas localmente (criado automaticamente)
```

## Instalação

```bash
cd /home/spingat/projetos/auto-updater
pip3 install -r requirements.txt
cp .env.example .env
```

Edite o `.env` com suas credenciais:
```
GITHUB_TOKEN=seu_token_github
GITHUB_USER=seu_usuario
GITHUB_EMAIL=seu_email@exemplo.com
REDDIT_TOKEN=seu_token_reddit  # Opcional
```

## Uso

### Teste seco (não altera nada)
```bash
python3 main.py --dry-run
```

### Execução completa
```bash
python3 main.py --push --prepare-reddit
```

### Via cron (recomendado)
Adicione ao crontab:
```bash
crontab crontab.example
```

Ou edite manualmente:
```bash
crontab -e
```
Adicione:
```
0 8 * * * /home/spingat/projetos/auto-updater/run_daily.sh
```

## Como funciona

1. O auto-updater lê o `config.yaml` para saber quais repositórios monitorar
2. Para cada repositório, consulta a API correspondente (GitHub, Flathub, PyPI, etc.)
3. Compara a versão remota com a versão salva localmente em `versions/`
4. Se houver atualização, salva a nova versão e adiciona ao changelog
5. Faz commit e push automático no GitHub
6. Gera `reddit_post.md` pronto para postar no Reddit

## Exemplos de configuração no config.yaml

```yaml
# GitHub Release
- name: "meu-projeto"
  type: "github_release"
  owner: "meu-usuario"
  repo: "meu-repo"
  asset_name: "meu-arquivo.AppImage"

# Flatpak
- name: "org.mozilla.firefox"
  type: "flathub"
  flatpak_id: "org.mozilla.firefox"
  check_installed: true

# PyPI
- name: "requests"
  type: "pypi"
  package_name: "requests"

# npm
- name: "vue"
  type: "npm"
  package_name: "vue"

# Docker Hub
- name: "nginx"
  type: "dockerhub"
  repository: "library/nginx"

# AUR
- name: "yay"
  type: "arch"
  package_name: "yay"