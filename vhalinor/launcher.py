# vhalinor/launcher.py
import os
import sys
import logging
from datetime import datetime

def setup_logging():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(module)s | %(message)s',
        handlers=[
            logging.FileHandler(f"{log_dir}/vhalinor_{datetime.now().strftime('%Y%m%d')}.log", encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger(__name__)

def launch_vhalinor():
    logger = setup_logging()
    logger.info("🚀 Iniciando VHALINOR I.A - Modo Headless (sem navegador)")
    logger.info(f"Hora de início: {datetime.now()}")
    logger.info("Plataforma prioritária: Binance Futures (ccxt)")

    # Importa o main da VHALINOR
    try:
        from vhalinor.main import run_vhalinor
        logger.info("✅ Módulos carregados com sucesso. Iniciando loop de trading...")
        run_vhalinor()   # Função principal que você vai criar em main.py
    except Exception as e:
        logger.error(f"❌ Erro fatal ao iniciar VHALINOR: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    launch_vhalinor()