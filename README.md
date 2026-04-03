# VHALINOR-IA
from binance.client import Client
from binance.exceptions import BinanceAPIException
import pandas as pd
import ta  # pip install ta-lib ou use pandas_ta
import time
import logging

# Configura logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Vhalinor - a IA
class Vhalinor:
    def __init__(self):
        self.nome = "Vhalinor"
        self.energia = 100.0  # Simula "consciência"
        self.curiosidade = 0.8

    def decidir(self, sinal: str, preco: float):
        if sinal == "BUY":
            return f"{self.nome} detectou oportunidade: Comprando BTC a {preco:.2f} USDT. Energia: {self.energia:.1f}%"
        elif sinal == "SELL":
            return f"{self.nome} vendeu: Lucro/trava em {preco:.2f}. Curiosidade alta!"
        return "Observando... sem sinal forte."

# Config Binance (use testnet primeiro!)
API_KEY = "SUA_API_KEY"  # do testnet: https://testnet.binance.vision/
API_SECRET = "SUA_SECRET"
client = Client(API_KEY, API_SECRET, testnet=True)  # Mude pra False pra live!

SYMBOL = "BTCUSDT"
INTERVAL = "1m"  # 1 minuto pro day trade
QUANTIDADE = 0.001  # BTC por trade (ajuste pro seu saldo)
RISK_PER_TRADE = 0.01  # 1% do capital

def get_data():
    klines = client.get_klines(symbol=SYMBOL, interval=INTERVAL, limit=100)
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore'])
    df = pd.to_numeric(df )
    return df

def calculate_indicators(df):
    df['rsi'] = ta.momentum.RSIIndicator(df , window=14).rsi()
    macd = ta.trend.MACD(df )
    df = macd.macd()
    df = macd.macd_signal()
    df = macd.macd_diff()
    return df

def get_signal(df):
    last = df.iloc[-1]
    prev = df.iloc[-2 'rsi'] < 30 and prev >= 30:
        # MACD cruzamento bullish
        if prev < prev and last > last :
            return "BUY"

    if last > 70 and prev <= 70:
        if prev['macd'] > prev and last < last :
            return "SELL"

    return None

# Loop principal
vhalinor = Vhalinor()

while True:
    try:
        df = get_data()
        df = calculate_indicators(df)
        sinal = get_signal(df)

        if sinal:
            preco_atual = float(client.get_symbol_ticker(symbol=SYMBOL)['price'])
            msg = vhalinor.decidir(sinal, preco_atual)
            logging.info(msg)

            # Executa ordem (testnet só)
            if sinal == "BUY":
                order = client.order_market_buy(symbol=SYMBOL, quantity=QUANTIDADE)
                logging.info(f"Compra executada: {order}")
            elif sinal == "SELL":
                order = client.order_market_sell(symbol=SYMBOL, quantity=QUANTIDADE)
                logging.info(f"Venda executada: {order}")

        time.sleep(60)  # 1 minuto

    except BinanceAPIException as e:
        logging.error(f"Erro API: {e}")
        time.sleep(300)  # Espera 5 min se falhar

    except Exception as e:
        logging.error(f"Erro geral: {e}")
        time.sleep(60)
        
