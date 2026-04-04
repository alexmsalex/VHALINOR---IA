#!/bin/bash
echo "================================================"
echo "          Iniciando VHALINOR I.A"
echo "   Modo: Headless (sem navegador)"
echo "================================================"

# Ativa venv se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

export PYTHONIOENCODING=utf-8
export TZ=America/Sao_Paulo

echo "[$(date)] Iniciando VHALINOR..."
python main.py

echo "VHALINOR parou."