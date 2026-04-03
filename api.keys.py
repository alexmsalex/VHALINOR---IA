"""
Arquivo de chaves de API - NÃO COMMITAR ESTE ARQUIVO!
Adicione api_keys.py ao .gitignore
"""

import os
import sys
from typing import Tuple

class APIKeys:
    """Classe segura para gerenciar chaves de API"""
    
    # ============================================
    # CONFIGURE SUAS CHAVES AQUI
    # ============================================
    
    # Para TESTNET (recomendado para desenvolvimento)
    TESTNET_API_KEY = "coloque_sua_chave_testnet_aqui"
    TESTNET_API_SECRET = "coloque_seu_secret_testnet_aqui"
    
    # Para PRODUÇÃO (use com EXTREMO CUIDADO!)
    PRODUCTION_API_KEY = "coloque_sua_chave_producao_aqui"
    PRODUCTION_API_SECRET = "coloque_seu_secret_producao_aqui"
    
    # ============================================
    # CONFIGURAÇÕES DO BOT
    # ============================================
    
    USE_TESTNET = True  # Mude para False APENAS quando estiver pronto!
    
    SYMBOL = "BTCUSDT"
    INTERVAL = "1m"
    QUANTITY = 0.001  # Quantidade em BTC por trade
    
    @classmethod
    def get_keys(cls) -> Tuple[str, str]:
        """
        Retorna as chaves de API baseado no modo selecionado
        """
        if cls.USE_TESTNET:
            api_key = cls.TESTNET_API_KEY
            api_secret = cls.TESTNET_API_SECRET
            mode = "TESTNET"
        else:
            api_key = cls.PRODUCTION_API_KEY
            api_secret = cls.PRODUCTION_API_SECRET
            mode = "PRODUÇÃO (CAPITAL REAL!)"
        
        # Validação básica
        if not api_key or not api_secret:
            print(f"❌ ERRO: Chaves de API não configuradas para {mode}")
            print("Por favor, configure suas chaves no arquivo api_keys.py")
            sys.exit(1)
        
        if "coloque_sua_chave" in api_key.lower():
            print(f"⚠️  AVISO: Você ainda não configurou suas chaves de {mode}")
            print(f"Edite o arquivo api_keys.py e substitua os valores de exemplo")
            sys.exit(1)
        
        print(f"✅ Chaves carregadas: {mode}")
        return api_key, api_secret
    
    @classmethod
    def get_settings(cls) -> dict:
        """Retorna as configurações do bot"""
        return {
            'symbol': cls.SYMBOL,
            'interval': cls.INTERVAL,
            'quantity': cls.QUANTITY,
            'use_testnet': cls.USE_TESTNET
        }

# Exporta as chaves para uso
API_KEY, API_SECRET = APIKeys.get_keys()