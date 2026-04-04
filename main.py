import os
import sys
import logging
from datetime import datetime

# Configuração de logging para arquivo (útil em background)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler("vhalinor.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)
logger.info("🚀 VHALINOR I.A iniciada em modo headless")
logger.info(f"Data/Hora: {datetime.now()}")
logger.info(f"Plataforma prioritária: Binance")