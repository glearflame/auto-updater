# Auto-Updater

Sistema automatizado para verificar e publicar atualizações de pacotes de diferentes fontes (Flathub, GitHub Releases, etc.) com publicação automática no GitHub e preparação para Reddit.

## Estrutura

```
auto-updater/
├── main.py              # Ponto de entrada
├── config.yaml          # Configuração de repositórios e fontes
├── updaters/            # Lógica de verificação por fonte
│   ├── __init__.py
│   ├── flathub.py       # Verifica atualizações no Flathub
│   ├── github_releases.py  # Verifica releases do GitHub
│   └── generic.py       # Base para outras fontes
├── publishers/          # Publicação de resultados
│   ├── __init__.py
│   ├── github.py        # Commit e push no GitHub
│   └── reddit.py        # Preparação para post no Reddit
├── requirements.txt     # Dependências Python
├── .env.example         # Exemplo de variáveis de ambiente
└── CHANGELOG.md         # Registro de atualizações automáticas
```

## Funcionalidades

- [x] Verificação automática de atualizações no Flathub
- [x] Verificação de novas releases no GitHub
- [x] Geração automática de changelog
- [x] Commit e push automático no GitHub
- [x] Preparação de post para Reddit (texto pronto, não publica automaticamente)
- [x] Logs detalhados de cada execução

## Configuração

1. Crie um arquivo `.env` baseado no `.env.example`:
```bash
cp .env.example .env
```

2. Edite o `config.yaml` com os repositórios que deseja monitorar:
```yaml
repositories:
  - name: "despertador"
    type: "github_release"
    owner: "glearflame"
    repo: "despertador"
    check_installed: true  # Verifica se está instalado localmente via flatpak

  - name: "org.gnome.Notes"
    type: "flathub"
    flatpak_id: "org.gnome.Notes"

  - name: "com.spotify.Client"
    type: "flathub"
    flatpak_id: "com.spotify.Client"
```

## Execução

### Teste seco (não altera nada)
```bash
python3 main.py --dry-run
```

### Execução completa (commit e push)
```bash
python3 main.py --push
```

### Apenas preparar post para Reddit
```bash
python3 main.py --prepare-reddit
```

## Variáveis de ambiente

Crie um arquivo `.env` com:

```
GITHUB_TOKEN=seu_token_github
REDDIT_TOKEN=seu_token_reddit  # Opcional, para post automático
GITHUB_USER=seu_usuario
GITHUB_EMAIL=seu_email
```

## Flathub

O updater do Flathub usa a API pública do Flathub ou o comando `flatpak remote-ls` para verificar versões instaladas vs disponíveis.

## GitHub Releases

Verifica a tag mais recente de um repositório e compara com a versão local (se houver um arquivo de versão ou se o pacote estiver instalado via flatpak).

## Publicação

- **GitHub**: Commit automático no branch `main` com mensagem descritiva e tag opcional
- **Reddit**: Gera um arquivo `reddit_post.md` pronto para copiar e colar (não publica automaticamente por segurança)