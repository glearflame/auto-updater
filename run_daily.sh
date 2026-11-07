#!/bin/bash
# Script para rodar o auto-updater diariamente via cron
# Adicione ao crontab com: crontab -e
# Exemplo: 0 8 * * * /home/spingat/projetos/auto-updater/run_daily.sh

cd /home/spingat/projetos/auto-updater || exit 1

# Carrega variáveis de ambiente
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -v '^$' | xargs)
fi

# Executa o auto-updater
python3 main.py --push --prepare-reddit >> logs/auto-updater.log 2>&1

echo "[$(date)] Execução concluída" >> logs/auto-updater.log
