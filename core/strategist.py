import pandas as pd
import pandas_ta as ta
from strategies import ALL_STRATEGIES

class Strategist:
    def __init__(self):
        self.strategies = ALL_STRATEGIES

    def detect_regime(self, df: pd.DataFrame) -> dict:
        """Analisa o regime atual do mercado"""
        # Indicadores de regime
        df["adx"] = ta.adx(df["high"], df["low"], df["close"], length=14)["ADX_14"]
        df["bb_width"] = ta.bbands(df["close"])["BBW_5_2.0"]  # largura das bandas
        df["rsi"] = ta.rsi(df["close"], length=14)
        df["volume_ma"] = df["volume"].rolling(20).mean()

        latest = df.iloc[-1]

        regime = {
            "trend_strength": latest["adx"],
            "volatility": latest["bb_width"],
            "momentum": latest["rsi"] - 50,
            "volume_ratio": latest["volume"] / latest["volume_ma"],
            "is_trending": latest["adx"] > 25,
            "is_volatile": latest["bb_width"] > df["bb_width"].quantile(0.7),
        }
        return regime

    def select_best_strategies(self, df: pd.DataFrame, top_n: int = 2) -> list:
        regime = self.detect_regime(df)
        
        scores = []
        for strategy in self.strategies:
            signal = strategy.get_signal(df)
            base_score = signal.get("confidence", 50)
            
            # Ajuste de score conforme regime
            if regime["is_trending"]:
                if strategy.name in ["Breakout", "Momentum", "EMACrossover"]:
                    base_score += 25
            else:
                if strategy.name in ["MeanReversion", "VWAP"]:
                    base_score += 25

            if regime["is_volatile"] and strategy.name == "Scalping":
                base_score += 15

            if regime["volume_ratio"] > 1.5:
                base_score += 10  # volume alto favorece breakout/momentum

            scores.append({
                "strategy": strategy.name,
                "score": max(0, min(100, base_score)),
                "signal": signal
            })

        # Ordena e pega as melhores
        scores.sort(key=lambda x: x["score"], reverse=True)
        return scores[:top_n]