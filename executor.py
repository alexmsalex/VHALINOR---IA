# core/executor.py (estrutura inicial)
class Executor:
    def __init__(self, platform: str = "binance"):
        self.platform = platform.lower()
        if self.platform == "binance":
            from binance.client import Client  # ou ccxt
            self.client = Client(api_key, api_secret)
        elif self.platform == "ctrader":
            # Integração via cTrader Python API ou OpenAPI
            pass
        # Pionex e WillTrader: mais limitado (Pionex foca em grids, WillTrader app-focused)

    def place_order(self, symbol, side, quantity, order_type="MARKET", **kwargs):
        if self.platform == "binance":
            if "futures" in symbol:  # ou use futures endpoint
                return self.client.futures_create_order(...)
            else:
                return self.client.create_order(...)