"""
VHALINOR Análise Profunda de Mercado Financeiro v8.0
======================================================
Sistema robusto de análise: fundamental, técnica, macro, fluxo, risco, sentimento.

@author VHALINOR Team
@version 8.0.0
@since 2026-04-06
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from collections import deque
import logging
from functools import cached_property, lru_cache
import json
import hashlib

# Configura logging estruturado
logger = logging.getLogger(__name__)


# ============================================================================
# Enums e tipos refinados
# ============================================================================

class TipoAtivo(Enum):
    ACAO = "acao"
    CRIPTO = "cripto"
    FOREX = "forex"
    COMMODITY = "commodity"
    INDICE = "indice"
    ETF = "etf"
    RENDA_FIXA = "renda_fixa"
    DERIVATIVO = "derivativo"
    
    @property
    def moeda_base(self) -> str:
        mapping = {
            TipoAtivo.ACAO: "BRL",
            TipoAtivo.CRIPTO: "USDT",
            TipoAtivo.FOREX: "USD",
            TipoAtivo.COMMODITY: "USD",
            TipoAtivo.INDICE: "pontos",
            TipoAtivo.ETF: "USD",
            TipoAtivo.RENDA_FIXA: "BRL",
            TipoAtivo.DERIVATIVO: "USD"
        }
        return mapping.get(self, "USD")


class TimeFrame(Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    M30 = "30m"
    H1 = "1h"
    H4 = "4h"
    D1 = "1d"
    W1 = "1w"
    
    def segundos(self) -> int:
        mapping = {
            TimeFrame.M1: 60, TimeFrame.M5: 300, TimeFrame.M15: 900,
            TimeFrame.M30: 1800, TimeFrame.H1: 3600, TimeFrame.H4: 14400,
            TimeFrame.D1: 86400, TimeFrame.W1: 604800
        }
        return mapping[self]


class Severidade(Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
    CRITICA = "critica"


class SinalMercado(Enum):
    FORTEMENTE_COMPRA = "forte_compra"
    COMPRA = "compra"
    NEUTRO = "neutro"
    VENDA = "venda"
    FORTEMENTE_VENDA = "forte_venda"


# ============================================================================
# Dataclasses otimizadas
# ============================================================================

@dataclass
class MetricaFundamental:
    """Métrica fundamental com validação e cálculo de score aprimorado."""
    nome: str
    valor: float
    referencia: float
    peso: float = 1.0
    tendencia: str = "estavel"
    score: float = field(default=50.0, init=False)
    ultima_atualizacao: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    
    def __post_init__(self):
        self._recalcular_score()
    
    def _recalcular_score(self):
        """Recalcula score baseado na razão valor/referência."""
        if self.referencia <= 0:
            self.score = 50.0
            self.tendencia = "estavel"
            return
        
        razao = self.valor / self.referencia
        if razao > 1.5:
            self.score = 92.0
            self.tendencia = "melhorando"
        elif razao > 1.1:
            self.score = 78.0
            self.tendencia = "melhorando"
        elif razao > 0.9:
            self.score = 65.0
            self.tendencia = "estavel"
        elif razao > 0.6:
            self.score = 38.0
            self.tendencia = "piorando"
        else:
            self.score = 15.0
            self.tendencia = "piorando"
    
    def atualizar(self, novo_valor: float, nova_ref: Optional[float] = None):
        self.valor = novo_valor
        if nova_ref is not None:
            self.referencia = nova_ref
        self.ultima_atualizacao = datetime.now(timezone.utc)
        self._recalcular_score()


@dataclass
class AlertaRisco:
    """Alerta de risco com metadados."""
    tipo: str
    severidade: Severidade
    descricao: str
    probabilidade: float  # 0-1
    impacto: float        # 0-1
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolvido: bool = False
    
    @property
    def score_risco(self) -> float:
        """Pontuação composta de risco (probabilidade * impacto)."""
        return self.probabilidade * self.impacto * 100
    
    def to_dict(self) -> Dict:
        return {
            "tipo": self.tipo,
            "severidade": self.severidade.value,
            "descricao": self.descricao,
            "probabilidade": self.probabilidade,
            "impacto": self.impacto,
            "timestamp": self.timestamp.isoformat(),
            "score_risco": round(self.score_risco, 2)
        }


@dataclass
class BookOferta:
    """Nível de book de ofertas (bid/ask)."""
    preco: float
    quantidade: float
    exchange: str = "binance"
    
    def valor_total(self) -> float:
        return self.preco * self.quantidade


# ============================================================================
# Classe principal melhorada
# ============================================================================

class AnaliseMercadoFinanceiro:
    """
    Sistema de análise financeira profunda - v8.0.
    Integra análise fundamental, técnica, macro, fluxo e risco.
    """
    
    def __init__(self, ativo: str, tipo: TipoAtivo, timeframe: TimeFrame = TimeFrame.D1):
        self.ativo = ativo.strip().upper()
        self.tipo = tipo
        self.timeframe = timeframe
        self._historico_precos: deque = deque(maxlen=5000)  # preços de fechamento
        self._historico_ohlcv: List[Dict] = []  # OHLCV completo
        self.metricas_fundamental: Dict[str, MetricaFundamental] = {}
        self.alertas: deque = deque(maxlen=100)
        self._dados_macro: Dict[str, float] = {}
        self._fluxo_ordens: deque = deque(maxlen=10000)  # ordens executadas simuladas
        self._book: Dict[str, List[BookOferta]] = {"bid": [], "ask": []}
        
        # Indicadores técnicos calculados sob demanda
        self._indicadores_cache: Dict[str, Any] = {}
        
        # Inicializa métricas base
        self._configurar_metricas_base()
        
        logger.info(f"AnaliseMercadoFinanceiro inicializado para {self.ativo} ({self.tipo.value})")
    
    def _configurar_metricas_base(self):
        """Define métricas fundamentais padrão por tipo de ativo."""
        metricas_por_tipo = {
            TipoAtivo.ACAO: {
                "P/L": (18.0, 0.25),
                "P/VPA": (2.0, 0.20),
                "ROE": (12.0, 0.20),
                "Margem Líquida": (8.0, 0.15),
                "Dívida/EBITDA": (3.0, 0.10),
                "Dividend Yield": (4.0, 0.10)
            },
            TipoAtivo.CRIPTO: {
                "Market Cap": (2e9, 0.30),
                "Volume 24h": (5e8, 0.25),
                "Dominância BTC": (0.45, 0.20),
                "Correlação BTC": (0.75, 0.15),
                "Endereços Ativos": (5e5, 0.10)
            },
            TipoAtivo.FOREX: {
                "Taxa de Juros": (2.5, 0.30),
                "PIB": (2.0, 0.25),
                "Balança Comercial": (0.0, 0.20),
                "Inflação": (2.0, 0.25)
            },
            TipoAtivo.COMMODITY: {
                "Estoques": (30, 0.30),
                "Demanda Global": (100, 0.25),
                "Custo de Produção": (50, 0.25),
                "Geopolítica": (0.5, 0.20)
            },
            TipoAtivo.INDICE: {
                "P/E Médio": (20.0, 0.35),
                "Dividend Yield": (3.0, 0.25),
                "Volatilidade": (15.0, 0.20),
                "Correlação VIX": (0.6, 0.20)
            },
            TipoAtivo.ETF: {
                "TER": (0.5, 0.30),
                "Liquidez": (1e6, 0.25),
                "Tracking Error": (0.5, 0.25),
                "AUM": (1e8, 0.20)
            },
            TipoAtivo.RENDA_FIXA: {
                "Duration": (5.0, 0.30),
                "Spread": (2.0, 0.25),
                "Rating": (0.7, 0.25),
                "Liquidez": (0.8, 0.20)
            },
            TipoAtivo.DERIVATIVO: {
                "Open Interest": (1000, 0.30),
                "Volume": (500, 0.25),
                "Basis": (0.5, 0.25),
                "Implied Vol": (20.0, 0.20)
            }
        }
        
        metricas = metricas_por_tipo.get(self.tipo, {})
        for nome, (ref, peso) in metricas.items():
            self.metricas_fundamental[nome] = MetricaFundamental(nome, 0.0, ref, peso)
    
    # ========================================================================
    # Atualização de dados
    # ========================================================================
    
    def atualizar_preco(self, preco: float, timestamp: Optional[datetime] = None):
        """Registra preço de fechamento (série temporal)."""
        self._historico_precos.append(preco)
        # Opcional: adiciona OHLCV simplificado
        if timestamp is None:
            timestamp = datetime.now(timezone.utc)
        self._historico_ohlcv.append({
            "timestamp": timestamp,
            "open": preco, "high": preco, "low": preco, "close": preco,
            "volume": 0.0
        })
        # Limita tamanho do histórico
        if len(self._historico_ohlcv) > 5000:
            self._historico_ohlcv = self._historico_ohlcv[-5000:]
    
    def atualizar_ohlcv(self, df: pd.DataFrame):
        """
        Atualiza com DataFrame OHLCV completo.
        Espera colunas: timestamp, open, high, low, close, volume
        """
        required = ["timestamp", "open", "high", "low", "close", "volume"]
        if not all(c in df.columns for c in required):
            raise ValueError(f"DataFrame deve conter colunas: {required}")
        
        for _, row in df.iterrows():
            ts = row["timestamp"] if isinstance(row["timestamp"], datetime) else pd.to_datetime(row["timestamp"])
            self._historico_ohlcv.append({
                "timestamp": ts,
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row["volume"])
            })
            self._historico_precos.append(float(row["close"]))
        
        # Mantém apenas últimos 5000
        if len(self._historico_ohlcv) > 5000:
            self._historico_ohlcv = self._historico_ohlcv[-5000:]
        if len(self._historico_precos) > 5000:
            # Converte deque para lista e recria
            self._historico_precos = deque(list(self._historico_precos)[-5000:], maxlen=5000)
        
        # Limpa cache de indicadores
        self._indicadores_cache.clear()
    
    def atualizar_metrica_fundamental(self, nome: str, valor: float, referencia: Optional[float] = None):
        """Atualiza uma métrica fundamental."""
        if nome not in self.metricas_fundamental:
            logger.warning(f"Métrica '{nome}' não existe para {self.ativo}. Criando dinamicamente.")
            self.metricas_fundamental[nome] = MetricaFundamental(nome, valor, referencia or 1.0, peso=0.1)
        else:
            self.metricas_fundamental[nome].atualizar(valor, referencia)
    
    def adicionar_macro(self, nome: str, valor: float):
        """Adiciona ou atualiza indicador macroeconômico."""
        self._dados_macro[nome] = valor
    
    def adicionar_alerta(self, alerta: AlertaRisco):
        """Adiciona um alerta de risco."""
        self.alertas.append(alerta)
        if alerta.severidade in (Severidade.ALTA, Severidade.CRITICA):
            logger.warning(f"ALERTA {alerta.severidade.value.upper()}: {alerta.descricao}")
    
    def adicionar_ordem(self, preco: float, quantidade: float, lado: str):
        """Registra uma ordem executada (fluxo)."""
        self._fluxo_ordens.append({
            "timestamp": datetime.now(timezone.utc),
            "preco": preco,
            "quantidade": quantidade,
            "lado": lado  # "buy" ou "sell"
        })
    
    def atualizar_book(self, bids: List[Tuple[float, float]], asks: List[Tuple[float, float]]):
        """Atualiza o book de ofertas."""
        self._book["bid"] = [BookOferta(p, q) for p, q in bids[:20]]
        self._book["ask"] = [BookOferta(p, q) for p, q in asks[:20]]
    
    # ========================================================================
    # Análises técnicas aprimoradas
    # ========================================================================
    
    @cached_property
    def df_ohlcv(self) -> pd.DataFrame:
        """Retorna DataFrame OHLCV para análises técnicas."""
        if not self._historico_ohlcv:
            return pd.DataFrame()
        df = pd.DataFrame(self._historico_ohlcv)
        df.set_index("timestamp", inplace=True)
        return df
    
    def _get_price_series(self) -> np.ndarray:
        """Retorna array de preços para cálculos numéricos."""
        return np.array(self._historico_precos, dtype=float)
    
    def calcular_indicadores_tecnicos(self) -> Dict:
        """Calcula conjunto de indicadores técnicos."""
        if len(self._historico_precos) < 50:
            return {}
        
        precos = self._get_price_series()
        retornos = np.diff(precos) / precos[:-1]
        
        # Médias móveis
        sma_20 = np.mean(precos[-20:]) if len(precos) >= 20 else precos[-1]
        sma_50 = np.mean(precos[-50:]) if len(precos) >= 50 else precos[-1]
        ema_12 = self._ema(precos, 12)
        ema_26 = self._ema(precos, 26)
        
        # RSI
        rsi = self._rsi(precos, 14)
        
        # MACD
        macd, signal, histogram = self._macd(precos)
        
        # Bandas de Bollinger
        bb_upper, bb_middle, bb_lower = self._bollinger_bands(precos, 20, 2)
        
        # ATR
        atr = self._atr(14) if len(self._historico_ohlcv) >= 15 else 0
        
        # Volume (se disponível)
        volume_medio = np.mean([c.get("volume", 0) for c in self._historico_ohlcv[-20:]]) if self._historico_ohlcv else 0
        
        return {
            "preco_atual": precos[-1],
            "sma_20": round(sma_20, 2),
            "sma_50": round(sma_50, 2),
            "ema_12": round(ema_12, 2),
            "ema_26": round(ema_26, 2),
            "rsi_14": round(rsi, 1),
            "macd": round(macd, 4),
            "macd_signal": round(signal, 4),
            "macd_histogram": round(histogram, 4),
            "bb_upper": round(bb_upper, 2),
            "bb_middle": round(bb_middle, 2),
            "bb_lower": round(bb_lower, 2),
            "bb_width_pct": round((bb_upper - bb_lower) / bb_middle * 100, 2) if bb_middle > 0 else 0,
            "atr": round(atr, 4),
            "volume_medio_20": round(volume_medio, 2),
            "volatilidade_anual": round(np.std(retornos) * np.sqrt(252) * 100, 2) if len(retornos) > 0 else 0
        }
    
    def _ema(self, data: np.ndarray, periodo: int) -> float:
        """Exponencial moving average do último valor."""
        if len(data) < periodo:
            return data[-1]
        alpha = 2 / (periodo + 1)
        ema = data[0]
        for val in data[1:]:
            ema = alpha * val + (1 - alpha) * ema
        return ema
    
    def _rsi(self, data: np.ndarray, periodo: int = 14) -> float:
        """RSI clássico."""
        if len(data) < periodo + 1:
            return 50.0
        deltas = np.diff(data)
        ganhos = np.where(deltas > 0, deltas, 0)
        perdas = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(ganhos[-periodo:])
        avg_loss = np.mean(perdas[-periodo:])
        if avg_loss == 0:
            return 100.0
        rs = avg_gain / avg_loss
        return 100 - (100 / (1 + rs))
    
    def _macd(self, data: np.ndarray, fast=12, slow=26, signal=9):
        """MACD: linha, sinal, histograma."""
        ema_fast = self._ema(data, fast)
        ema_slow = self._ema(data, slow)
        macd_line = ema_fast - ema_slow
        
        # Para sinal, precisaríamos de série. Aproximação: usa último valor de EMA da linha
        # Versão simplificada: retorna apenas valor atual (para uso em sinal)
        # Em produção, seria melhor calcular série completa
        # Como temos apenas último valor, usamos uma estimativa
        return macd_line, macd_line * 0.9, macd_line * 0.1
    
    def _bollinger_bands(self, data: np.ndarray, periodo=20, num_std=2):
        """Bandas de Bollinger."""
        if len(data) < periodo:
            media = data[-1]
            std = 0
        else:
            ultimos = data[-periodo:]
            media = np.mean(ultimos)
            std = np.std(ultimos)
        upper = media + (std * num_std)
        lower = media - (std * num_std)
        return upper, media, lower
    
    def _atr(self, periodo=14) -> float:
        """Average True Range usando OHLCV."""
        if len(self._historico_ohlcv) < periodo + 1:
            return 0.0
        df = self.df_ohlcv
        if df.empty:
            return 0.0
        high = df['high'].values
        low = df['low'].values
        close = df['close'].values
        tr = np.maximum(high - low, 
                        np.abs(high - np.roll(close, 1)),
                        np.abs(low - np.roll(close, 1)))
        tr[0] = high[0] - low[0]
        atr = np.mean(tr[-periodo:])
        return atr
    
    # ========================================================================
    # Análises de risco e bolha
    # ========================================================================
    
    def detectar_bolha(self) -> Dict:
        """Detecta bolha ou crash iminente usando múltiplos indicadores."""
        if len(self._historico_precos) < 60:
            return {"alerta": False, "confianca": 0.0, "recomendacao": "dados insuficientes"}
        
        precos = self._get_price_series()
        media = np.mean(precos[-60:])
        std = np.std(precos[-60:])
        zscore = (precos[-1] - media) / std if std > 0 else 0
        
        # Aceleração (derivada segunda)
        if len(precos) >= 30:
            v1 = (precos[-1] - precos[-16]) / 15
            v2 = (precos[-16] - precos[-31]) / 15
            aceleracao = v1 - v2
        else:
            aceleracao = 0.0
        
        # RSI extremo
        rsi = self._rsi(precos, 14)
        rsi_extremo = rsi > 85 or rsi < 15
        
        # Volume anormal
        volume_anormal = False
        if len(self._historico_ohlcv) >= 20:
            volumes = [c.get("volume", 0) for c in self._historico_ohlcv[-20:]]
            vol_medio = np.mean(volumes)
            vol_ultimo = volumes[-1]
            volume_anormal = vol_ultimo > 2.5 * vol_medio
        
        bolha = (zscore > 2.5 and aceleracao > 0.02) or (rsi > 85 and volume_anormal)
        crash = (zscore < -2.0 and aceleracao < -0.05) or (rsi < 15 and volume_anormal)
        
        if bolha:
            recomendacao = "vender rápido" if rsi > 80 else "cautela"
        elif crash:
            recomendacao = "comprar fundo" if rsi < 20 else "observar oportunidade"
        else:
            recomendacao = "manter"
        
        return {
            "alerta_bolha": bolha,
            "alerta_crash": crash,
            "zscore": round(zscore, 2),
            "aceleracao": round(aceleracao, 4),
            "rsi": round(rsi, 1),
            "volume_anormal": volume_anormal,
            "recomendacao": recomendacao,
            "confianca": min(100, max(0, (abs(zscore) * 20 + (rsi if bolha else 100-rsi) * 0.5)))
        }
    
    def risco_simples(self) -> Dict:
        """Métricas de risco: VaR, CVaR, drawdown, Sharpe, beta."""
        if len(self._historico_precos) < 100:
            return {"var_95": None, "cvar_95": None, "max_drawdown": None, "sharpe": None}
        
        precos = self._get_price_series()
        retornos = np.diff(precos) / precos[:-1]
        
        # VaR histórico 95%
        var_95 = np.percentile(retornos, 5)
        cvar_95 = np.mean(retornos[retornos <= var_95]) if any(retornos <= var_95) else var_95
        
        # Drawdown máximo
        peak = np.maximum.accumulate(precos)
        drawdown = (peak - precos) / peak
        max_dd = np.max(drawdown)
        
        # Sharpe ratio (assumindo taxa livre 0%)
        sharpe = np.mean(retornos) / np.std(retornos) * np.sqrt(252) if np.std(retornos) > 0 else 0
        
        # Beta (em relação ao benchmark genérico - aqui simulado)
        # Em produção, buscar dados de benchmark externo
        beta = 1.0
        
        return {
            "var_95_diario": round(var_95 * 100, 2),
            "cvar_95_diario": round(cvar_95 * 100, 2),
            "max_drawdown": round(max_dd * 100, 2),
            "sharpe_anualizado": round(sharpe, 2),
            "beta": round(beta, 2),
            "volatilidade_anual": round(np.std(retornos) * np.sqrt(252) * 100, 2)
        }
    
    def analise_sentimento(self) -> Dict:
        """Análise de sentimento baseada em fluxo de ordens e book."""
        if len(self._fluxo_ordens) < 10:
            return {"sentimento": "neutro", "score": 0.5}
        
        # Calcula delta de fluxo (compras - vendas)
        compras = sum(o["quantidade"] for o in self._fluxo_ordens if o["lado"] == "buy")
        vendas = sum(o["quantidade"] for o in self._fluxo_ordens if o["lado"] == "sell")
        delta_volume = (compras - vendas) / (compras + vendas + 1e-9)
        
        # Assimetria do book
        bid_depth = sum(b.quantidade for b in self._book["bid"][:5]) if self._book["bid"] else 0
        ask_depth = sum(a.quantidade for a in self._book["ask"][:5]) if self._book["ask"] else 0
        book_imbalance = (bid_depth - ask_depth) / (bid_depth + ask_depth + 1e-9)
        
        # Sentimento combinado
        score = (delta_volume * 0.6 + book_imbalance * 0.4 + 1) / 2  # normalizado [0,1]
        score = max(0, min(1, score))
        
        if score > 0.7:
            sentimento = SinalMercado.FORTEMENTE_COMPRA.value
        elif score > 0.55:
            sentimento = SinalMercado.COMPRA.value
        elif score > 0.45:
            sentimento = SinalMercado.NEUTRO.value
        elif score > 0.3:
            sentimento = SinalMercado.VENDA.value
        else:
            sentimento = SinalMercado.FORTEMENTE_VENDA.value
        
        return {
            "sentimento": sentimento,
            "score": round(score, 3),
            "delta_volume": round(delta_volume, 3),
            "book_imbalance": round(book_imbalance, 3),
            "total_compras": round(compras, 2),
            "total_vendas": round(vendas, 2)
        }
    
    def score_fundamental(self) -> float:
        """Score agregado ponderado das métricas fundamentais."""
        if not self.metricas_fundamental:
            return 50.0
        total_peso = sum(m.peso for m in self.metricas_fundamental.values())
        if total_peso == 0:
            return 50.0
        return sum(m.score * m.peso for m in self.metricas_fundamental.values()) / total_peso
    
    def classificacao_fundamental(self) -> str:
        """Classificação textual do score fundamental."""
        score = self.score_fundamental()
        if score >= 80:
            return "Excelente"
        elif score >= 65:
            return "Bom"
        elif score >= 45:
            return "Neutro"
        elif score >= 30:
            return "Fraco"
        else:
            return "Crítico"
    
    # ========================================================================
    # Relatórios e recomendações
    # ========================================================================
    
    def gerar_sinal_unificado(self) -> Dict:
        """Combina análises fundamental, técnica, risco e sentimento em um sinal."""
        fund_score = self.score_fundamental()
        tecnicos = self.calcular_indicadores_tecnicos()
        risco = self.risco_simples()
        bolha = self.detectar_bolha()
        sentimento = self.analise_sentimento()
        
        # Ponderações
        peso_fund = 0.30 if self.tipo in (TipoAtivo.ACAO, TipoAtivo.CRIPTO) else 0.20
        peso_tec = 0.35
        peso_risco = 0.20
        peso_sent = 0.15
        
        # Score técnico (baseado em RSI, MACD, bandas)
        tec_score = 50
        if tecnicos:
            rsi = tecnicos.get("rsi_14", 50)
            if rsi < 30:
                tec_score = 80  # sobrevendido -> compra
            elif rsi > 70:
                tec_score = 20  # sobrecomprado -> venda
            else:
                tec_score = 50 + (40 - rsi) * 0.5  # mapeia 30-70 para 70-30
            
            # Ajuste por MACD
            if tecnicos.get("macd_histogram", 0) > 0:
                tec_score += 5
            else:
                tec_score -= 5
        
        # Score de risco (invertido: menor risco melhor)
        var = risco.get("var_95_diario", 2.0) if risco.get("var_95_diario") else 2.0
        risco_score = max(0, min(100, 100 - (var * 10)))
        
        # Score de sentimento já está em 0-1, converter para 0-100
        sent_score = sentimento["score"] * 100
        
        # Score final
        score_final = (fund_score * peso_fund + 
                      tec_score * peso_tec + 
                      risco_score * peso_risco + 
                      sent_score * peso_sent)
        
        # Determinar sinal
        if score_final >= 70:
            sinal = SinalMercado.FORTEMENTE_COMPRA.value
        elif score_final >= 55:
            sinal = SinalMercado.COMPRA.value
        elif score_final >= 45:
            sinal = SinalMercado.NEUTRO.value
        elif score_final >= 30:
            sinal = SinalMercado.VENDA.value
        else:
            sinal = SinalMercado.FORTEMENTE_VENDA.value
        
        return {
            "ativo": self.ativo,
            "sinal": sinal,
            "score_total": round(score_final, 1),
            "score_fundamental": round(fund_score, 1),
            "score_tecnico": round(tec_score, 1),
            "score_risco": round(risco_score, 1),
            "score_sentimento": round(sent_score, 1),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def gerar_relatorio(self) -> Dict:
        """Relatório consolidado completo."""
        return {
            "ativo": self.ativo,
            "tipo": self.tipo.value,
            "timeframe": self.timeframe.value,
            "score_fundamental": round(self.score_fundamental(), 1),
            "classificacao_fundamental": self.classificacao_fundamental(),
            "metricas_fundamentais": {nome: asdict(m) for nome, m in self.metricas_fundamental.items()},
            "indicadores_tecnicos": self.calcular_indicadores_tecnicos(),
            "risco": self.risco_simples(),
            "bolha_crash": self.detectar_bolha(),
            "sentimento": self.analise_sentimento(),
            "sinal_unificado": self.gerar_sinal_unificado(),
            "alertas_ativos": [a.to_dict() for a in self.alertas if not a.resolvido][-10:],
            "macro_indicadores": self._dados_macro.copy(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def salvar_relatorio(self, caminho: str):
        """Salva relatório em JSON."""
        relatorio = self.gerar_relatorio()
        with open(caminho, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False, default=str)
        logger.info(f"Relatório salvo em {caminho}")
    
    def __repr__(self) -> str:
        return f"AnaliseMercadoFinanceiro(ativo={self.ativo}, tipo={self.tipo.value})"


# ============================================================================
# Utilitário de cache para múltiplos ativos
# ============================================================================

class AnaliseMercadoCache:
    """Cache singleton para gerenciar análises de múltiplos ativos."""
    
    _instances: Dict[str, 'AnaliseMercadoCache'] = {}
    _analises: Dict[str, AnaliseMercadoFinanceiro] = {}
    
    def __new__(cls, nome_cache: str = "default"):
        if nome_cache not in cls._instances:
            cls._instances[nome_cache] = super().__new__(cls)
        return cls._instances[nome_cache]
    
    def get_analise(self, ativo: str, tipo: TipoAtivo, criar_se_nao_existir: bool = True) -> Optional[AnaliseMercadoFinanceiro]:
        """Obtém análise para um ativo, cria se não existir."""
        key = f"{ativo}_{tipo.value}"
        if key not in self._analises and criar_se_nao_existir:
            self._analises[key] = AnaliseMercadoFinanceiro(ativo, tipo)
        return self._analises.get(key)
    
    def remover_analise(self, ativo: str, tipo: TipoAtivo):
        key = f"{ativo}_{tipo.value}"
        if key in self._analises:
            del self._analises[key]
    
    def listar_ativos(self) -> List[str]:
        return list(self._analises.keys())


# ============================================================================
# Exemplo de uso
# ============================================================================

if __name__ == "__main__":
    # Exemplo com PETR4
    analise = AnaliseMercadoFinanceiro("PETR4", TipoAtivo.ACAO, TimeFrame.D1)
    
    # Alimenta com dados simulados
    preco_base = 35.0
    for i in range(200):
        variacao = np.random.normal(0, 0.02)
        preco_base *= (1 + variacao)
        analise.atualizar_preco(preco_base)
    
    # Atualiza métricas fundamentais
    analise.atualizar_metrica_fundamental("P/L", 12.5, 18.0)
    analise.atualizar_metrica_fundamental("ROE", 14.2, 12.0)
    analise.atualizar_metrica_fundamental("Dividend Yield", 5.5, 4.0)
    
    # Adiciona alerta de exemplo
    analise.adicionar_alerta(AlertaRisco(
        tipo="volatilidade",
        severidade=Severidade.MEDIA,
        descricao="Aumento repentino de volatilidade",
        probabilidade=0.6,
        impacto=0.4
    ))
    
    # Gera relatório
    relatorio = analise.gerar_relatorio()
    print(json.dumps(relatorio, indent=2, default=str))
    
    # Sinal unificado
    sinal = analise.gerar_sinal_unificado()
    print(f"\nSinal para {sinal['ativo']}: {sinal['sinal'].upper()} (score {sinal['score_total']})")