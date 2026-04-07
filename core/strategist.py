# strategist.py
import pandas as pd
import pandas_ta as ta
import numpy as np
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from strategies import ALL_STRATEGIES
import logging
from collections import deque

logger = logging.getLogger(__name__)

class MarketRegime(Enum):
    """Tipos de regime de mercado"""
    STRONG_TRENDING = "strong_trending"
    WEAK_TRENDING = "weak_trending"
    RANGING = "ranging"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"
    BREAKOUT = "breakout"
    REVERSAL = "reversal"

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EXTREME = "extreme"

@dataclass
class RegimeAnalysis:
    """Análise completa do regime de mercado"""
    regime: MarketRegime
    trend_strength: float
    volatility: float
    momentum: float
    volume_profile: Dict[str, float]
    support_resistance: Dict[str, float]
    market_phase: str
    risk_level: RiskLevel
    confidence: float
    timestamp: pd.Timestamp
    
@dataclass
class StrategyScore:
    """Pontuação e análise de uma estratégia"""
    strategy_name: str
    base_score: float
    adjusted_score: float
    confidence: float
    risk_adjusted: float
    signal: Dict[str, Any]
    reasoning: List[str]
    regime_fit: str

class EnhancedStrategist:
    """Analista avançado de estratégias com adaptação dinâmica ao mercado"""
    
    def __init__(self, lookback_periods: int = 100, min_history: int = 50):
        self.strategies = ALL_STRATEGIES
        self.lookback_periods = lookback_periods
        self.min_history = min_history
        self.performance_tracker = PerformanceTracker()
        self.regime_history = deque(maxlen=100)
        
        # Pesos para diferentes condições de mercado
        self.strategy_weights = {
            "trending": {
                "Breakout": 1.4,
                "Momentum": 1.3,
                "EMACrossover": 1.3,
                "Scalping": 0.7,
                "MeanReversion": 0.6,
                "VWAP": 0.9
            },
            "ranging": {
                "MeanReversion": 1.5,
                "VWAP": 1.2,
                "Scalping": 1.1,
                "Breakout": 0.5,
                "Momentum": 0.6,
                "EMACrossover": 0.7
            },
            "volatile": {
                "Scalping": 1.4,
                "Breakout": 1.2,
                "Momentum": 1.1,
                "MeanReversion": 0.5,
                "EMACrossover": 0.8
            }
        }
        
    def detect_regime(self, df: pd.DataFrame) -> RegimeAnalysis:
        """Análise completa do regime de mercado"""
        if len(df) < self.min_history:
            logger.warning(f"Dados insuficientes: {len(df)} < {self.min_history}")
            return self._default_regime_analysis(df)
        
        # Indicadores base
        df = self._calculate_market_indicators(df)
        latest = df.iloc[-1]
        
        # Análise de tendência
        trend_analysis = self._analyze_trend(df)
        
        # Análise de volatilidade
        volatility_analysis = self._analyze_volatility(df)
        
        # Análise de volume
        volume_analysis = self._analyze_volume_profile(df)
        
        # Suporte e resistência
        sr_levels = self._find_support_resistance(df)
        
        # Determinar regime
        regime, confidence = self._classify_regime(
            trend_analysis, volatility_analysis, volume_analysis
        )
        
        # Avaliar risco
        risk_level = self._assess_risk(
            trend_analysis, volatility_analysis, volume_analysis
        )
        
        # Identificar fase do mercado
        market_phase = self._identify_market_phase(df)
        
        regime_analysis = RegimeAnalysis(
            regime=regime,
            trend_strength=trend_analysis["strength"],
            volatility=volatility_analysis["current"],
            momentum=trend_analysis["momentum"],
            volume_profile=volume_analysis,
            support_resistance=sr_levels,
            market_phase=market_phase,
            risk_level=risk_level,
            confidence=confidence,
            timestamp=df.index[-1] if df.index[-1] else pd.Timestamp.now()
        )
        
        self.regime_history.append(regime_analysis)
        return regime_analysis
    
    def _calculate_market_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula todos os indicadores necessários para análise de regime"""
        # ADX para força da tendência
        adx_df = ta.adx(df["high"], df["low"], df["close"], length=14)
        df["adx"] = adx_df["ADX_14"]
        df["plus_di"] = adx_df["DMP_14"]
        df["minus_di"] = adx_df["DMN_14"]
        
        # Bandas de Bollinger
        bb_df = ta.bbands(df["close"], length=20, std=2)
        df["bb_width"] = bb_df["BBW_20_2.0"]
        df["bb_percent"] = (df["close"] - bb_df["BBL_20_2.0"]) / (bb_df["BBU_20_2.0"] - bb_df["BBL_20_2.0"])
        
        # RSI
        df["rsi"] = ta.rsi(df["close"], length=14)
        df["rsi_trend"] = ta.sma(df["rsi"], length=5)
        
        # ATR
        df["atr"] = ta.atr(df["high"], df["low"], df["close"], length=14)
        df["atr_percent"] = df["atr"] / df["close"] * 100
        
        # Volume
        df["volume_ma"] = df["volume"].rolling(20).mean()
        df["volume_ratio"] = df["volume"] / df["volume_ma"]
        df["volume_trend"] = ta.sma(df["volume_ratio"], length=5)
        
        # MACD
        macd_df = ta.macd(df["close"])
        df["macd"] = macd_df["MACD_12_26_9"]
        df["macd_signal"] = macd_df["MACDs_12_26_9"]
        df["macd_hist"] = macd_df["MACDh_12_26_9"]
        
        # Ichimoku (opcional)
        df["tenkan"] = (df["high"].rolling(window=9).max() + df["low"].rolling(window=9).min()) / 2
        df["kijun"] = (df["high"].rolling(window=26).max() + df["low"].rolling(window=26).min()) / 2
        
        # Estocástico
        stoch_df = ta.stoch(df["high"], df["low"], df["close"])
        df["stoch_k"] = stoch_df["STOCHk_14_3_3"]
        df["stoch_d"] = stoch_df["STOCHd_14_3_3"]
        
        return df
    
    def _analyze_trend(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Análise detalhada da tendência"""
        latest = df.iloc[-1]
        prev = df.iloc[-2]
        
        # Múltiplas médias móveis
        ma_20 = ta.sma(df["close"], length=20)
        ma_50 = ta.sma(df["close"], length=50)
        ma_200 = ta.sma(df["close"], length=200)
        
        # Análise de inclinação
        slope_20 = (ma_20.iloc[-1] - ma_20.iloc[-5]) / ma_20.iloc[-5] if len(ma_20) >= 5 else 0
        
        # Estrutura de mercado
        higher_highs = df["high"].iloc[-5:].is_monotonic_increasing
        higher_lows = df["low"].iloc[-5:].is_monotonic_increasing
        
        trend_analysis = {
            "strength": latest["adx"],
            "direction": 1 if latest["close"] > ma_20.iloc[-1] else -1,
            "momentum": latest["rsi"] - 50,
            "slope": slope_20,
            "macd_trend": latest["macd_hist"] > 0,
            "price_vs_ma": {
                "ma_20": (latest["close"] - ma_20.iloc[-1]) / ma_20.iloc[-1] * 100,
                "ma_50": (latest["close"] - ma_50.iloc[-1]) / ma_50.iloc[-1] * 100 if len(ma_50) > 0 else 0
            },
            "structure": {
                "higher_highs": higher_highs,
                "higher_lows": higher_lows,
                "trend_strength": "strong" if latest["adx"] > 40 else "moderate" if latest["adx"] > 25 else "weak"
            }
        }
        
        return trend_analysis
    
    def _analyze_volatility(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Análise de volatilidade"""
        latest = df.iloc[-1]
        
        # Volatilidade histórica
        returns = df["close"].pct_change()
        historical_vol = returns.rolling(20).std() * np.sqrt(365)
        
        # Posição percentil da volatilidade
        vol_percentile = (latest["bb_width"] / df["bb_width"].rolling(100).max()).iloc[-1] if len(df) >= 100 else 0.5
        
        volatility_analysis = {
            "current": latest["atr_percent"],
            "historical": historical_vol.iloc[-1],
            "percentile": vol_percentile,
            "bb_width": latest["bb_width"],
            "bb_position": latest["bb_percent"],
            "regime": "high" if vol_percentile > 0.7 else "low" if vol_percentile < 0.3 else "normal"
        }
        
        return volatility_analysis
    
    def _analyze_volume_profile(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Análise do perfil de volume"""
        latest = df.iloc[-1]
        
        # Volume cluster (últimos 5 candles)
        volume_cluster = df["volume"].iloc[-5:].mean()
        volume_trend = "increasing" if latest["volume_trend"] > df["volume_trend"].iloc[-5] else "decreasing"
        
        # Volume price confirmation
        price_up = latest["close"] > df["close"].iloc[-2]
        volume_confirms = (price_up and latest["volume_ratio"] > 1.2) or (not price_up and latest["volume_ratio"] > 1.2)
        
        volume_analysis = {
            "ratio": latest["volume_ratio"],
            "trend": volume_trend,
            "cluster_avg": volume_cluster / df["volume_ma"].iloc[-1] if df["volume_ma"].iloc[-1] > 0 else 1,
            "confirms_move": volume_confirms,
            "divergence": latest["volume_ratio"] > 1.5 and latest["adx"] < 20  # Volume alto sem tendência
        }
        
        return volume_analysis
    
    def _find_support_resistance(self, df: pd.DataFrame, window: int = 50) -> Dict[str, float]:
        """Encontra níveis de suporte e resistência"""
        # Método de picos e vales
        high_peaks = self._find_peaks(df["high"].values, window=10)
        low_valleys = self._find_peaks(-df["low"].values, window=10)
        
        # Agrupar níveis próximos
        resistance_levels = self._cluster_levels(df["high"].iloc[high_peaks].values)
        support_levels = self._cluster_levels(df["low"].iloc[low_valleys].values)
        
        current_price = df["close"].iloc[-1]
        
        # Encontrar suporte e resistência mais próximos
        nearest_resistance = min([r for r in resistance_levels if r > current_price], default=current_price * 1.05)
        nearest_support = max([s for s in support_levels if s < current_price], default=current_price * 0.95)
        
        return {
            "support": nearest_support,
            "resistance": nearest_resistance,
            "all_supports": support_levels[:5],
            "all_resistances": resistance_levels[:5],
            "distance_to_resistance": (nearest_resistance - current_price) / current_price * 100,
            "distance_to_support": (current_price - nearest_support) / current_price * 100
        }
    
    def _find_peaks(self, series: np.ndarray, window: int = 10) -> np.ndarray:
        """Encontra picos em uma série temporal"""
        peaks = []
        for i in range(window, len(series) - window):
            if all(series[i] >= series[i - j] for j in range(1, window + 1)) and \
               all(series[i] >= series[i + j] for j in range(1, window + 1)):
                peaks.append(i)
        return np.array(peaks)
    
    def _cluster_levels(self, levels: np.ndarray, tolerance: float = 0.005) -> List[float]:
        """Agrupa níveis próximos"""
        if len(levels) == 0:
            return []
        
        levels = sorted(levels)
        clusters = []
        current_cluster = [levels[0]]
        
        for level in levels[1:]:
            if abs(level - current_cluster[-1]) / current_cluster[-1] <= tolerance:
                current_cluster.append(level)
            else:
                clusters.append(np.mean(current_cluster))
                current_cluster = [level]
        
        clusters.append(np.mean(current_cluster))
        return clusters
    
    def _classify_regime(self, trend: Dict, volatility: Dict, volume: Dict) -> Tuple[MarketRegime, float]:
        """Classifica o regime atual do mercado"""
        confidence = 0.0
        
        if trend["strength"] > 40:
            regime = MarketRegime.STRONG_TRENDING
            confidence = min(1.0, trend["strength"] / 60)
        elif trend["strength"] > 25:
            regime = MarketRegime.WEAK_TRENDING
            confidence = 0.7
        elif volatility["current"] > volatility["historical"] * 1.5:
            regime = MarketRegime.HIGH_VOLATILITY
            confidence = 0.8
        elif volatility["current"] < volatility["historical"] * 0.5:
            regime = MarketRegime.LOW_VOLATILITY
            confidence = 0.6
        else:
            regime = MarketRegime.RANGING
            confidence = 0.7
        
        # Verificar breakout
        if volume["ratio"] > 1.5 and trend["momentum"] > 30:
            regime = MarketRegime.BREAKOUT
            confidence = 0.9
        
        # Verificar reversão potencial
        if abs(trend["momentum"]) > 40 and volume["ratio"] > 1.3:
            regime = MarketRegime.REVERSAL
            confidence = 0.75
        
        return regime, confidence
    
    def _assess_risk(self, trend: Dict, volatility: Dict, volume: Dict) -> RiskLevel:
        """Avalia o nível de risco do mercado"""
        risk_score = 0
        
        # Volatilidade alta aumenta risco
        if volatility["current"] > volatility["historical"]:
            risk_score += 30
        if volatility["percentile"] > 0.8:
            risk_score += 20
        
        # Tendência fraca aumenta risco
        if trend["strength"] < 20:
            risk_score += 25
        elif trend["strength"] < 25:
            risk_score += 10
        
        # Divergência volume-preço aumenta risco
        if volume["divergence"]:
            risk_score += 20
        
        # Classificar risco
        if risk_score > 70:
            return RiskLevel.EXTREME
        elif risk_score > 50:
            return RiskLevel.HIGH
        elif risk_score > 25:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def _identify_market_phase(self, df: pd.DataFrame) -> str:
        """Identifica a fase atual do mercado (acumulação, markup, distribuição, markdown)"""
        # Implementação baseada em Wyckoff simplificada
        volume_profile = df["volume_ratio"].iloc[-20:].mean()
        price_position = (df["close"].iloc[-1] - df["low"].iloc[-20:].min()) / (df["high"].iloc[-20:].max() - df["low"].iloc[-20:].min())
        
        if volume_profile < 0.8 and price_position < 0.3:
            return "accumulation"
        elif volume_profile > 1.2 and price_position > 0.7:
            return "distribution"
        elif volume_profile > 1.0 and price_position > 0.5:
            return "markup"
        elif volume_profile > 0.9 and price_position < 0.5:
            return "markdown"
        else:
            return "consolidation"
    
    def select_best_strategies(self, df: pd.DataFrame, top_n: int = 3, 
                              risk_tolerance: str = "medium") -> List[StrategyScore]:
        """Seleciona as melhores estratégias baseado na análise do regime"""
        if len(df) < self.min_history:
            logger.warning(f"Dados insuficientes para seleção de estratégias: {len(df)}")
            return []
        
        regime_analysis = self.detect_regime(df)
        logger.info(f"Regime detectado: {regime_analysis.regime.value} (confiança: {regime_analysis.confidence:.2%})")
        
        strategy_scores = []
        
        for strategy in self.strategies:
            # Obter sinal da estratégia
            signal = strategy.get_signal(df)
            
            # Score base
            base_score = signal.get("confidence", 50)
            
            # Ajuste baseado no regime
            regime_fit, adjustment = self._calculate_regime_adjustment(
                strategy.name, regime_analysis
            )
            
            # Ajuste baseado no desempenho histórico
            performance_adjustment = self.performance_tracker.get_adjustment(strategy.name)
            
            # Ajuste baseado no risco
            risk_adjustment = self._calculate_risk_adjustment(
                strategy.name, regime_analysis.risk_level
            )
            
            # Score final ajustado
            adjusted_score = base_score + adjustment + performance_adjustment + risk_adjustment
            adjusted_score = max(0, min(100, adjusted_score))
            
            # Score ajustado pelo risco
            risk_adjusted = adjusted_score * (1 - self._get_risk_penalty(regime_analysis.risk_level))
            
            # Coletar raciocínio da decisão
            reasoning = self._build_reasoning(
                strategy.name, regime_analysis, adjustment, performance_adjustment, risk_adjustment
            )
            
            strategy_scores.append(StrategyScore(
                strategy_name=strategy.name,
                base_score=base_score,
                adjusted_score=adjusted_score,
                confidence=signal.get("confidence", 50) / 100,
                risk_adjusted=risk_adjusted,
                signal=signal,
                reasoning=reasoning,
                regime_fit=regime_fit
            ))
        
        # Ordenar por score ajustado
        strategy_scores.sort(key=lambda x: x.adjusted_score, reverse=True)
        
        # Filtrar por tolerância de risco
        filtered_scores = self._filter_by_risk_tolerance(strategy_scores, risk_tolerance)
        
        logger.info(f"Top {top_n} estratégias selecionadas:")
        for score in filtered_scores[:top_n]:
            logger.info(f"  - {score.strategy_name}: {score.adjusted_score:.1f} (conf: {score.confidence:.1%})")
        
        return filtered_scores[:top_n]
    
    def _calculate_regime_adjustment(self, strategy_name: str, regime: RegimeAnalysis) -> Tuple[str, float]:
        """Calcula ajuste de pontuação baseado no regime de mercado"""
        adjustment = 0
        regime_fit = "neutral"
        
        if regime.regime in [MarketRegime.STRONG_TRENDING, MarketRegime.WEAK_TRENDING]:
            weight = self.strategy_weights["trending"].get(strategy_name, 1.0)
            adjustment = (weight - 1.0) * 50
            regime_fit = "trend_following"
            
        elif regime.regime == MarketRegime.RANGING:
            weight = self.strategy_weights["ranging"].get(strategy_name, 1.0)
            adjustment = (weight - 1.0) * 60
            regime_fit = "mean_reversion"
            
        elif regime.regime in [MarketRegime.HIGH_VOLATILITY, MarketRegime.BREAKOUT]:
            weight = self.strategy_weights["volatile"].get(strategy_name, 1.0)
            adjustment = (weight - 1.0) * 40
            regime_fit = "volatility_based"
        
        # Ajustes específicos
        if regime.volume_profile["confirms_move"] and strategy_name in ["Breakout", "Momentum"]:
            adjustment += 15
        
        if abs(regime.momentum) < 15 and strategy_name == "MeanReversion":
            adjustment += 10
        
        if regime.support_resistance["distance_to_resistance"] < 1.0 and strategy_name == "Breakout":
            adjustment += 10
        
        return regime_fit, adjustment
    
    def _calculate_risk_adjustment(self, strategy_name: str, risk_level: RiskLevel) -> float:
        """Calcula ajuste baseado no nível de risco"""
        risk_penalties = {
            RiskLevel.LOW: 0,
            RiskLevel.MEDIUM: -5,
            RiskLevel.HIGH: -15,
            RiskLevel.EXTREME: -30
        }
        
        # Estratégias de baixo risco em mercados voláteis
        low_risk_strategies = ["MeanReversion", "VWAP"]
        
        if risk_level in [RiskLevel.HIGH, RiskLevel.EXTREME] and strategy_name in low_risk_strategies:
            return risk_penalties[risk_level] / 2  # Penalidade reduzida
        else:
            return risk_penalties[risk_level]
    
    def _get_risk_penalty(self, risk_level: RiskLevel) -> float:
        """Retorna penalidade de risco para score ajustado"""
        penalties = {
            RiskLevel.LOW: 0.0,
            RiskLevel.MEDIUM: 0.1,
            RiskLevel.HIGH: 0.25,
            RiskLevel.EXTREME: 0.5
        }
        return penalties[risk_level]
    
    def _filter_by_risk_tolerance(self, scores: List[StrategyScore], risk_tolerance: str) -> List[StrategyScore]:
        """Filtra estratégias baseado na tolerância de risco"""
        if risk_tolerance == "low":
            # Aceita apenas estratégias com score risk-adjusted > 60
            return [s for s in scores if s.risk_adjusted > 60]
        elif risk_tolerance == "high":
            # Permite estratégias mais agressivas
            return scores
        else:  # medium
            return [s for s in scores if s.risk_adjusted > 40]
    
    def _build_reasoning(self, strategy_name: str, regime: RegimeAnalysis, 
                        adjustment: float, perf_adjustment: float, risk_adjustment: float) -> List[str]:
        """Constrói explicação textual da seleção"""
        reasoning = []
        
        # Regime base
        reasoning.append(f"Mercado em regime {regime.regime.value} (confiança: {regime.confidence:.1%})")
        
        # Ajuste de regime
        if adjustment > 20:
            reasoning.append(f"Estratégia bem adaptada ao regime atual (+{adjustment:.0f} pts)")
        elif adjustment < -20:
            reasoning.append(f"Estratégia não recomendada para regime atual ({adjustment:.0f} pts)")
        
        # Performance
        if perf_adjustment > 10:
            reasoning.append(f"Bom desempenho histórico recente (+{perf_adjustment:.0f} pts)")
        elif perf_adjustment < -10:
            reasoning.append(f"Desempenho histórico abaixo do esperado ({perf_adjustment:.0f} pts)")
        
        # Risco
        if risk_adjustment < 0:
            reasoning.append(f"Alta volatilidade reduz pontuação devido ao risco ({risk_adjustment:.0f} pts)")
        
        # Condições específicas
        if regime.volume_profile["confirms_move"]:
            reasoning.append("Volume confirmando movimento de preço")
        
        if regime.support_resistance["distance_to_resistance"] < 1.0:
            reasoning.append("Próximo à resistência, potencial de breakout")
        
        return reasoning
    
    def _default_regime_analysis(self, df: pd.DataFrame) -> RegimeAnalysis:
        """Retorna análise padrão quando dados insuficientes"""
        return RegimeAnalysis(
            regime=MarketRegime.RANGING,
            trend_strength=25,
            volatility=2.0,
            momentum=0,
            volume_profile={"ratio": 1.0, "trend": "neutral", "confirms_move": False},
            support_resistance={"support": 0, "resistance": 0},
            market_phase="unknown",
            risk_level=RiskLevel.MEDIUM,
            confidence=0.5,
            timestamp=pd.Timestamp.now()
        )


class PerformanceTracker:
    """Rastreia performance histórica das estratégias"""
    
    def __init__(self, max_history: int = 100):
        self.performance_history = {strategy: deque(maxlen=max_history) for strategy in self._get_strategy_names()}
        
    def _get_strategy_names(self) -> List[str]:
        """Retorna nomes de todas as estratégias disponíveis"""
        from strategies import ALL_STRATEGIES
        return [s.name for s in ALL_STRATEGIES]
    
    def update_performance(self, strategy_name: str, profit: float, win: bool):
        """Atualiza performance de uma estratégia"""
        if strategy_name in self.performance_history:
            self.performance_history[strategy_name].append({
                "profit": profit,
                "win": win,
                "timestamp": pd.Timestamp.now()
            })
    
    def get_adjustment(self, strategy_name: str) -> float:
        """Calcula ajuste baseado em performance recente"""
        if strategy_name not in self.performance_history or len(self.performance_history[strategy_name]) < 5:
            return 0
        
        recent_trades = list(self.performance_history[strategy_name])[-20:]
        win_rate = sum(1 for t in recent_trades if t["win"]) / len(recent_trades)
        avg_profit = sum(t["profit"] for t in recent_trades) / len(recent_trades)
        
        # Calcular score de performance
        performance_score = (win_rate - 0.5) * 40 + (avg_profit * 10)
        
        # Limitar ajuste entre -20 e +20
        return max(-20, min(20, performance_score))
    
    def get_statistics(self, strategy_name: str) -> Dict[str, Any]:
        """Retorna estatísticas de performance"""
        if strategy_name not in self.performance_history or len(self.performance_history[strategy_name]) == 0:
            return {}
        
        trades = list(self.performance_history[strategy_name])
        wins = [t for t in trades if t["win"]]
        
        return {
            "total_trades": len(trades),
            "win_rate": len(wins) / len(trades),
            "avg_profit": sum(t["profit"] for t in trades) / len(trades),
            "total_profit": sum(t["profit"] for t in trades),
            "best_trade": max(t["profit"] for t in trades) if trades else 0,
            "worst_trade": min(t["profit"] for t in trades) if trades else 0
        }


# Interface simplificada para compatibilidade com código existente
class Strategist:
    """Wrapper para compatibilidade com código legado"""
    
    def __init__(self):
        self.enhanced = EnhancedStrategist()
        
    def detect_regime(self, df: pd.DataFrame) -> dict:
        """Versão compatível com código antigo"""
        regime_analysis = self.enhanced.detect_regime(df)
        
        # Converter para o formato antigo
        return {
            "trend_strength": regime_analysis.trend_strength,
            "volatility": regime_analysis.volatility,
            "momentum": regime_analysis.momentum,
            "volume_ratio": regime_analysis.volume_profile.get("ratio", 1.0),
            "is_trending": regime_analysis.regime in [MarketRegime.STRONG_TRENDING, MarketRegime.WEAK_TRENDING],
            "is_volatile": regime_analysis.regime == MarketRegime.HIGH_VOLATILITY,
            "risk_level": regime_analysis.risk_level.value,
            "market_phase": regime_analysis.market_phase
        }
    
    def select_best_strategies(self, df: pd.DataFrame, top_n: int = 2, risk_tolerance: str = "medium") -> list:
        """Versão melhorada com seleção avançada"""
        strategy_scores = self.enhanced.select_best_strategies(df, top_n, risk_tolerance)
        
        # Converter para formato legado
        return [
            {
                "strategy": score.strategy_name,
                "score": score.adjusted_score,
                "signal": score.signal,
                "confidence": score.confidence,
                "reasoning": score.reasoning
            }
            for score in strategy_scores
        ]