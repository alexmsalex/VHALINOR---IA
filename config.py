"""
Arquivo de configuração centralizado para o bot VHALINOR-IA
Carrega variáveis de ambiente e gerencia chaves de API com segurança
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Carrega variáveis do arquivo .env
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class BinanceConfig:
    """Configuração segura para API da Binance"""
    
    # Modo de operação
    TESTNET = os.getenv('BINANCE_TESTNET', 'True').lower() == 'true'
    
    # Chaves de API (seleciona automaticamente baseado no modo)
    @property
    def API_KEY(self):
        if self.TESTNET:
            return os.getenv('BINANCE_API_KEY_TEST')
        return os.getenv('BINANCE_API_KEY_PROD')
    
    @property
    def API_SECRET(self):
        if self.TESTNET:
            return os.getenv('BINANCE_API_SECRET_TEST')
        return os.getenv('BINANCE_API_SECRET_PROD')
    
    # Parâmetros de trading
    SYMBOL = os.getenv('BINANCE_SYMBOL', 'BTCUSDT')
    INTERVAL = os.getenv('BINANCE_INTERVAL', '1m')
    QUANTITY = float(os.getenv('BINANCE_QUANTITY', '0.001'))
    RISK_PER_TRADE = float(os.getenv('BINANCE_RISK_PER_TRADE', '0.01'))
    
    # Validação
    def validate(self):
        """Verifica se as chaves estão configuradas corretamente"""
        if not self.API_KEY or not self.API_SECRET:
            raise ValueError(
                f"API keys não configuradas para {'TESTNET' if self.TESTNET else 'PRODUÇÃO'}\n"
                f"Verifique o arquivo .env"
            )
        return True

# Instância global da configuração
config = BinanceConfig()

# Exemplo de uso no seu código principal
if __name__ == "__main__":
    print(f"Modo: {'TESTNET' if config.TESTNET else 'PRODUÇÃO'}")
    print(f"Símbolo: {config.SYMBOL}")
    print(f"Intervalo: {config.INTERVAL}")
    print(f"Quantidade: {config.QUANTITY} BTC")
    
    # Validação segura
    try:
        config.validate()
        print("✅ Configuração válida!")
    except ValueError as e:
        print(f"❌ Erro: {e}")