# strategy_base.py
from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Dict, Optional, Tuple, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class SignalType(Enum):
    """Tipos de sinal possíveis"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"
    CLOSE_LONG = "close_long"
    CLOSE_SHORT = "close_short"

class TimeFrame(Enum):
    """Timeframes suportados"""
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"

@dataclass
class SignalResult:
    """Resultado completo de uma análise de estratégia"""
    signal: SignalType
    confidence: float  # 0-100
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    take_profit_levels: List[float] = field(default_factory=list)  # múltiplos alvos
    risk_reward_ratio: Optional[float] = None
    position_size_pct: Optional[float] = None  # % do capital para esta operação
    entry_price: Optional[float] = None
    expiration: Optional[datetime] = None  # tempo de validade do sinal
    metadata: Dict[str, Any] = field(default_factory=dict)
    reasoning: List[str] = field(default_factory=list)
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário (compatível com versão antiga)"""
        result = {
            "signal": self.signal.value,
            "confidence": self.confidence,
            "stop_loss": self.stop_loss,
            "take_profit": self.take_profit,
            "strategy": "",  # será preenchido depois
        }
        # Adiciona campos extras se existirem
        if self.risk_reward_ratio:
            result["risk_reward_ratio"] = self.risk_reward_ratio
        if self.position_size_pct:
            result["position_size_pct"] = self.position_size_pct
        if self.metadata:
            result["metadata"] = self.metadata
        if self.reasoning:
            result["reasoning"] = self.reasoning
        return result


class Strategy(ABC):
    """
    Classe base abstrata para todas as estratégias de trading.
    
    Attributes:
        name (str): Nome da estratégia
        risk_percent (float): Percentual do capital a arriscar por operação (padrão 1.0%)
        timeframe (TimeFrame): Timeframe preferencial da estratégia
        min_history_bars (int): Mínimo de candles necessários para análise
        require_volume (bool): Se a estratégia precisa de dados de volume
        cooldown_bars (int): Número de barras para esperar após um sinal
    """
    
    def __init__(self, 
                 name: str,
                 risk_percent: float = 1.0,
                 timeframe: TimeFrame = TimeFrame.H1,
                 min_history_bars: int = 100,
                 require_volume: bool = False,
                 cooldown_bars: int = 0):
        self.name = name
        self.risk_percent = max(0.1, min(10.0, risk_percent))  # limitar entre 0.1% e 10%
        self.timeframe = timeframe
        self.min_history_bars = min_history_bars
        self.require_volume = require_volume
        self.cooldown_bars = cooldown_bars
        self._last_signal_bar: Optional[int] = None  # índice da última barra onde sinal foi gerado
        
    @abstractmethod
    def analyze(self, df: pd.DataFrame) -> SignalResult:
        """
        Método principal de análise. Deve ser implementado por cada estratégia.
        
        Args:
            df: DataFrame OHLCV com columns ['open','high','low','close','volume']
            
        Returns:
            SignalResult contendo decisão e parâmetros
        """
        pass
    
    def get_signal(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Interface pública que retorna dicionário compatível com versões antigas.
        Inclui validação, logging e cooldown.
        """
        # Validações básicas
        if not self._validate_dataframe(df):
            logger.warning(f"[{self.name}] DataFrame inválido ou dados insuficientes")
            return self._empty_signal()
        
        # Verificar cooldown
        if self._is_in_cooldown(df):
            logger.debug(f"[{self.name}] Em cooldown, ignorando análise")
            return self._empty_signal()
        
        # Executar análise
        try:
            signal_result = self.analyze(df)
            
            # Pós-processamento do resultado
            signal_result = self._post_process_signal(signal_result, df)
            
            # Atualizar cooldown se houver sinal ativo
            if signal_result.signal in (SignalType.BUY, SignalType.SELL):
                self._last_signal_bar = len(df) - 1
                logger.info(f"[{self.name}] Sinal {signal_result.signal.value} gerado com confiança {signal_result.confidence:.1f}%")
            
            # Converter para dicionário (compatibilidade)
            result_dict = signal_result.to_dict()
            result_dict["strategy"] = self.name
            
            return result_dict
            
        except Exception as e:
            logger.error(f"[{self.name}] Erro na análise: {e}", exc_info=True)
            return self._empty_signal()
    
    def _validate_dataframe(self, df: pd.DataFrame) -> bool:
        """Valida o DataFrame e verifica dados mínimos"""
        required_cols = ['open', 'high', 'low', 'close']
        if self.require_volume:
            required_cols.append('volume')
        
        if not all(col in df.columns for col in required_cols):
            logger.error(f"[{self.name}] Colunas faltando: {set(required_cols) - set(df.columns)}")
            return False
        
        if len(df) < self.min_history_bars:
            logger.warning(f"[{self.name}] Dados insuficientes: {len(df)} < {self.min_history_bars}")
            return False
        
        # Verificar valores nulos nos últimos candles
        if df[required_cols].iloc[-10:].isnull().any().any():
            logger.warning(f"[{self.name}] Valores nulos nos últimos candles")
            return False
        
        return True
    
    def _is_in_cooldown(self, df: pd.DataFrame) -> bool:
        """Verifica se está em período de cooldown após último sinal"""
        if self.cooldown_bars <= 0 or self._last_signal_bar is None:
            return False
        
        current_bar = len(df) - 1
        bars_since_signal = current_bar - self._last_signal_bar
        return bars_since_signal < self.cooldown_bars
    
    def _post_process_signal(self, signal: SignalResult, df: pd.DataFrame) -> SignalResult:
        """Pós-processamento: preenche defaults, valida stops/targets, calcula risk/reward"""
        # Preencher entry price com último close se não definido
        if signal.entry_price is None:
            signal.entry_price = df['close'].iloc[-1]
        
        # Validar stop loss e take profit
        if signal.stop_loss is not None and signal.take_profit is not None:
            # Calcular risk/reward ratio
            if signal.signal == SignalType.BUY:
                risk = signal.entry_price - signal.stop_loss
                reward = signal.take_profit - signal.entry_price
            elif signal.signal == SignalType.SELL:
                risk = signal.stop_loss - signal.entry_price
                reward = signal.entry_price - signal.take_profit
            else:
                risk = reward = 0
            
            if risk > 0:
                signal.risk_reward_ratio = reward / risk
            else:
                signal.risk_reward_ratio = 0.0
                
            # Log de aviso se risk/reward muito baixo
            if signal.risk_reward_ratio is not None and signal.risk_reward_ratio < 1.0:
                logger.debug(f"[{self.name}] Risk/Reward baixo: {signal.risk_reward_ratio:.2f}")
        
        # Definir position size baseado no risco se não especificado
        if signal.position_size_pct is None and signal.stop_loss is not None:
            # Posição padrão = risco percentual / (% de risco por trade)
            # Exemplo: se risk_percent = 1% e stop loss é 2% do entry, position_size_pct = 50%
            risk_pct = abs((signal.stop_loss - signal.entry_price) / signal.entry_price) * 100
            if risk_pct > 0:
                signal.position_size_pct = (self.risk_percent / risk_pct) * 100
                signal.position_size_pct = min(100, max(0, signal.position_size_pct))  # limitar 0-100%
        
        # Confiança mínima (clamp)
        signal.confidence = max(0, min(100, signal.confidence))
        
        return signal
    
    def _empty_signal(self) -> Dict[str, Any]:
        """Retorna sinal vazio (HOLD) para casos de erro ou cooldown"""
        return {
            "signal": "hold",
            "confidence": 0,
            "stop_loss": None,
            "take_profit": None,
            "strategy": self.name
        }
    
    def calculate_atr_stop(self, df: pd.DataFrame, multiplier: float = 2.0, period: int = 14) -> Tuple[float, float]:
        """
        Calcula stop loss e take profit baseados em ATR.
        
        Returns:
            (stop_loss, take_profit) para posição longa
        """
        atr = self._atr(df, period).iloc[-1]
        current_price = df['close'].iloc[-1]
        
        stop_loss = current_price - (atr * multiplier)
        take_profit = current_price + (atr * multiplier * 1.5)  # risk/reward 1.5:1
        return stop_loss, take_profit
    
    def _atr(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Calcula Average True Range"""
        high = df['high']
        low = df['low']
        close = df['close']
        tr1 = high - low
        tr2 = abs(high - close.shift())
        tr3 = abs(low - close.shift())
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr
    
    def calculate_supertrend_stop(self, df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> pd.Series:
        """Calcula SuperTrend para trailing stop"""
        atr = self._atr(df, period)
        hl_avg = (df['high'] + df['low']) / 2
        upper_band = hl_avg + (multiplier * atr)
        lower_band = hl_avg - (multiplier * atr)
        
        supertrend = pd.Series(index=df.index, dtype=float)
        trend = pd.Series(index=df.index, dtype=int)
        
        for i in range(period, len(df)):
            if i == period:
                supertrend.iloc[i] = upper_band.iloc[i]
                trend.iloc[i] = 1
                continue
            
            if df['close'].iloc[i-1] <= supertrend.iloc[i-1]:
                if df['close'].iloc[i] > upper_band.iloc[i]:
                    trend.iloc[i] = 1
                    supertrend.iloc[i] = lower_band.iloc[i]
                else:
                    trend.iloc[i] = -1
                    supertrend.iloc[i] = upper_band.iloc[i]
            else:
                if df['close'].iloc[i] < lower_band.iloc[i]:
                    trend.iloc[i] = -1
                    supertrend.iloc[i] = upper_band.iloc[i]
                else:
                    trend.iloc[i] = 1
                    supertrend.iloc[i] = lower_band.iloc[i]]
        
        return supertrend
    
    def __repr__(self) -> str:
        return f"{self.name} (risk={self.risk_percent}%, tf={self.timeframe.value})"


# Utilitários para facilitar criação de estratégias
class StrategyUtils:
    """Métodos auxiliares comuns para estratégias"""
    
    @staticmethod
    def detect_crossovers(df: pd.DataFrame, fast_ma: pd.Series, slow_ma: pd.Series) -> Tuple[bool, bool]:
        """
        Detecta cruzamentos de médias.
        Returns:
            (golden_cross, death_cross)
        """
        golden = (fast_ma.iloc[-2] <= slow_ma.iloc[-2]) and (fast_ma.iloc[-1] > slow_ma.iloc[-1])
        death = (fast_ma.iloc[-2] >= slow_ma.iloc[-2]) and (fast_ma.iloc[-1] < slow_ma.iloc[-1])
        return golden, death
    
    @staticmethod
    def is_overbought_oversold(rsi: pd.Series, overbought: float = 70, oversold: float = 30) -> Tuple[bool, bool]:
        """Verifica condições de sobrecompra/sobrevenda"""
        current = rsi.iloc[-1]
        return current > overbought, current < oversold
    
    @staticmethod
    def support_resistance_levels(df: pd.DataFrame, window: int = 20) -> Tuple[float, float]:
        """Encontra suporte e resistência recentes usando pivôs"""
        highs = df['high'].rolling(window, center=True).max()
        lows = df['low'].rolling(window, center=True).min()
        resistance = highs.iloc[-1]
        support = lows.iloc[-1]
        return support, resistance