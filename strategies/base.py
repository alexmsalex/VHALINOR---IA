from abc import ABC, abstractmethod
import pandas as pd

class Strategy(ABC):
    name: str
    risk_percent: float = 1.0  # % do capital operacional por operação

    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> dict:
        """Retorna dict com: signal, confidence, stop_loss, take_profit"""
        pass

    def get_signal(self, df: pd.DataFrame) -> dict:
        result = self.analyze(df)
        result["strategy"] = self.name
        return result