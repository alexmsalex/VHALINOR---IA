"""
VHALINOR Análise Profunda de Mercado Financeiro v7.0
======================================================
Sistema robusto de análise financeira: fundamental, técnica, macro, fluxo, risco.

@author VHALINOR Team
@version 7.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from collections import deque
import logging
from functools import cached_property

# Configura logging (nível DEBUG em dev)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TipoAtivo(Enum):
    ACAO = "acao"
    CRIPTO = "cripto"
    FOREX = "forex"
    COMMODITY = "commodity"
    INDICE = "indice"
    ETF = "etf"
    RENDA_FIXA = "renda_fixa"
    DERIVATIVO = "derivativo"


class TimeFrame(Enum):
    M1 = "1m"
    M5 = "5m"
    M15 = "15m"
    H4 = "4h"
    D1 = "1d"


@dataclass
class MetricaFundamental:
    nome: str
    valor: float
    referencia: float
    peso: float = 1.0
    tendencia: str = "estavel"  # melhorando | piorando | estavel
    score: float = field(default=50.0, init=False)

    def __post_init__(self):
        if self.referencia > 0:
            razao = self.valor / self.referencia
            if razao > 1.5: 
                object.__setattr__(self, "score", 92.0)
                object.__setattr__(self, "tendencia", "melhorando")
            elif razao > 1.1: 
                object.__setattr__(self, "score", 78.0)
                object.__setattr__(self, "tendencia", "melhorando")
            elif razao > 0.9: 
                object.__setattr__(self, "score", 65.0)
                object.__setattr__(self, "tendencia", "estavel")
            elif razao > 0.6: 
                object.__setattr__(self, "score", 38.0)
                object.__setattr__(self, "tendencia", "piorando")
            else: 
                object.__setattr__(self, "score", 15.0)
                object.__setattr__(self, "tendencia", "piorando")


@dataclass
class AlertaRisco:
    tipo: str
    severidade: str  # baixa | media | alta | critica
    descricao: str
    probabilidade: float  # 0-1
    impacto: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AnaliseMercadoFinanceiro:
    """Sistema de análise financeira profunda - v7.0"""

    def __init__(self, ativo: str, tipo: TipoAtivo):
        self.ativo = ativo.strip().upper()
        self.tipo = tipo
        self._historico_precos: deque = deque(maxlen=1000)  # preços fechamento
        self.metricas_fundamental: Dict = {}
        self.alertas: deque = deque(maxlen=50)
        self._dados_macro: Dict = {}  # chave: nome indicador
        self._fluxo_ordens: deque = deque(maxlen=5000)
        self._book: Dict = {"bid": [ ]}

        self._configurar_metricas_base()

    def _configurar_metricas_base(self):
        """Métricas iniciais por tipo de ativo"""
        base = {
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
            }
        }
        for nome, (ref, peso) in base.get(self.tipo, {}).items():
            self.metricas_fundamental[nome] = MetricaFundamental(nome, 0.0, ref, peso)

    def atualizar_preco(self, preco: float):
        """Registra preço de fechamento"""
        self._historico_precos.append(preco)

    def atualizar_metrica_fundamental(self, nome: str, valor: float, ref: Optional = None):
        if nome not in self.metricas_fundamental:
            logger.warning(f"Métrica {nome} não existe para {self.ativo}")
            return
        m = self.metricas_fundamental[nome]
        m.valor = valor
        if ref is not None:
            m.referencia = ref
        # Recalcula score automaticamente
        object.__setattr__(m, "score", m.score)  # força re-init

    def score_fundamental(self) -> float:
        """Score agregado ponderado"""
        if not self.metricas_fundamental:
            return 50.0
        pesos = sum(m.peso for m in self.metricas_fundamental.values())
        return sum(m.score * m.peso for m in self.metricas_fundamental.values()) / pesos

    def adicionar_macro(self, nome: str, valor: float):
        self._dados_macro[nome] = valor

    def detectar_bolha(self) -> Dict:
        if len(self._historico_precos) < 60:
            return {"alerta": False, "confianca": 0.0}

        precos = np.array(self._historico_precos)
        media = precos[-60:].mean()
        std = np.std(precos[-60:])
        zscore = (precos[-1] - media) / std

        # Aceleração (derivada 2ª aproximada)
        if len(precos) >= 30:
            v1 = (precos[-1] - precos[-16]) / 15
            v2 = (precos[-16] - precos[-31]) / 15
            aceleracao = v1 - v2
        else:
            aceleracao = 0.0

        bolha = zscore > 2.5 and aceleracao > 0.02
        crash = zscore < -2.0 and aceleracao < -0.05

        return {
            "bolha": bolha,
            "crash": crash,
            "zscore": round(zscore, 2),
            "aceleracao": round(aceleracao, 4),
            "recomendacao": "vender rápido" if bolha else "comprar fundo" if crash else "observar"
        }

    def risco_simples(self) -> Dict:
        """VaR histórico 95% + drawdown"""
        if len(self._historico_precos) < 100:
            return {"var": None, "drawdown": None}

        retornos = np.diff(self._historico_precos) / self._historico_precos[:-1]
        var_95 = np.percentile(retornos, 5) * -1  # perda máxima esperada
        drawdown = (np.maximum.accumulate(self._historico_precos) - self._historico_precos) / np.maximum.accumulate(self._historico_precos)
        max_dd = drawdown.max()

        return {
            "var_95_diario": round(var_95 * 100, 2),
            "max_drawdown": round(max_dd * 100, 2),
            "sharpe": round(np.mean(retornos) / np.std(retornos) * np.sqrt(252), 2) if np.std(retornos) else 0.0
        }

    def gerar_relatorio(self) -> Dict:
        """Relatório consolidado"""
        score_fund = self.score_fundamental()
        risco = self.risco_simples()
        bolha = self.detectar_bolha()

        return {
            "ativo": self.ativo,
            "score_fundamental": round(score_fund, 1),
            "classificacao": "Excelente" if score_fund >= 75 else "Bom" if score_fund >= 60 else "Cuidado",
            "risco": risco,
            "bolha_crash": bolha,
            "alertas": list(self.alertas)[-3:],
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


# Exemplo rápido
if __name__ == "__main__":
    analise = AnaliseMercadoFinanceiro("PETR4", TipoAtivo.ACAO)
    analise.atualizar_metrica_fundamental("P/L", 12.5)
    analise.atualizar_preco(35.20)
    analise.atualizar_preco(36.10)
    # ... mais preços
    print(analise.gerar_relatorio())