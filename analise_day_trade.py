"""
VHALINOR Análise Day Trade v6.0
=================================
Sistema de análise especializado para day trading com:
- Scalping automatizado
- Análise de momentum intraday
- Perfil de volume (Volume Profile)
- Análise de fluxo de ordens (Order Flow)
- VWAP e desvios
- Suportes e resistências dinâmicos
- Detecção de breakouts/breakdowns
- Range trading
- Gerenciamento de risco intraday
- Timing de mercado (abertura/fechamento)
- Análise de liquidez
- Heatmap de preço

@module analise_day_trade
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from collections import deque, defaultdict
import hashlib


class EstrategiaDayTrade(Enum):
    """Estratégias de day trading"""
    SCALPING = "scalping"
    MOMENTUM = "momentum"
    REVERSAO = "reversao"
    RANGE = "range"
    BREAKOUT = "breakout"
    VWAP = "vwap"
    OPEN_DRIVE = "open_drive"
    ORB = "opening_range_breakout"
    FADE = "fade"
    PULLBACK = "pullback"


class MomentoDia(Enum):
    """Momentos do dia de trading"""
    PRE_MARKET = "pre_market"
    OPEN = "open"
    MORNING = "morning"
    MIDDAY = "midday"
    AFTERNOON = "afternoon"
    CLOSE = "close"
    AFTER_HOURS = "after_hours"


class TipoSetup(Enum):
    """Tipos de setup day trade"""
    COMPRA_AGRESSIVA = "compra_agressiva"
    VENDA_AGRESSIVA = "venda_agressiva"
    COMPRA_CONSERVADORA = "compra_conservadora"
    VENDA_CONSERVADORA = "venda_conservadora"
    NEUTRO = "neutro"


@dataclass
class NivelVolume:
    """Nível do volume profile"""
    preco: float
    volume_total: float
    volume_compra: float
    volume_venda: float
    numero_candles: int
    poc: bool = False  # Point of Control
    va: bool = False   # Value Area
    
    @property
    def delta(self) -> float:
        return self.volume_compra - self.volume_venda


@dataclass
class SetupDayTrade:
    """Setup de day trade identificado"""
    id: str
    estrategia: EstrategiaDayTrade
    tipo: TipoSetup
    entrada: float
    stop_loss: float
    alvo_1: float
    alvo_2: float
    alvo_3: float
    risco_recompensa: float
    confianca: float
    tempo_expiracao: int  # minutos
    motivacao: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    @property
    def potencial_pontos(self) -> float:
        return abs(self.alvo_1 - self.entrada)


@dataclass
class SinalVWAP:
    """Sinal baseado em VWAP"""
    preco_atual: float
    vwap: float
    desvio_std: float
    distancia_vwap_percent: float
    tendencia: str  # "acima", "abaixo", "testando"
    sinal: str  # "compra", "venda", "neutro"
    forca: float


@dataclass
class AnaliseLiquidez:
    """Análise de liquidez do ativo"""
    spread_atual: float
    spread_medio_24h: float
    volume_ultima_hora: float
    depth_compra: float
    depth_venda: float
    impacto_1k: float  # Impacto de ordem de 1k
    impacto_10k: float
    qualidade_liquidez: str  # "alta", "media", "baixa"


@dataclass
class EstatisticasIntraday:
    """Estatísticas intraday do ativo"""
    abertura: float
    maxima_dia: float
    minima_dia: float
    fechamento_anterior: float
    variacao_abertura_percent: float
    variacao_maxima_percent: float
    variacao_minima_percent: float
    amplitude_atr: float
    volume_acumulado: float
    volume_medio_hora: float
    candles_acima_vwap: int
    candles_abaixo_vwap: int


class AnaliseDayTrade:
    """
    Sistema de análise especializado para day trading.
    
    Focado em operações de curto prazo com análise técnica
    avançada, volume profile, order flow e timing de mercado.
    """
    
    def __init__(self, ativo: str, capital_por_trade: float = 1000.0):
        self.ativo = ativo
        self.capital_por_trade = capital_por_trade
        self.risco_maximo_percent = 1.0  # 1% por trade
        
        # Históricos
        self.historico_setups: deque = deque(maxlen=100)
        self.operacoes_hoje: deque = deque(maxlen=50)
        self.volume_profile: Dict[float, NivelVolume] = {}
        self.estatisticas_intraday: Optional[EstatisticasIntraday] = None
        
        # Níveis dinâmicos
        self.vwap_atual: float = 0.0
        self.desvios_vwap: Dict[int, float] = {}  # +/- 1, 2, 3 std
        self.suportes_intraday: List[float] = []
        self.resistencias_intraday: List[float] = []
        self.poc: Optional[float] = None  # Point of Control
        
        # Estado atual
        self.operacao_atual: Optional[SetupDayTrade] = None
        self.hora_ultimo_setup: Optional[datetime] = None
    
    def atualizar_estatisticas_intraday(self, dados: EstatisticasIntraday):
        """Atualizar estatísticas intraday"""
        self.estatisticas_intraday = dados
    
    def calcular_vwap(self, candles: List[Dict[str, Any]]) -> float:
        """Calcular VWAP (Volume Weighted Average Price)"""
        if not candles:
            return 0.0
        
        tpv_total = 0.0  # Typical Price * Volume
        volume_total = 0.0
        
        for candle in candles:
            typical_price = (candle['high'] + candle['low'] + candle['close']) / 3
            volume = candle['volume']
            
            tpv_total += typical_price * volume
            volume_total += volume
        
        vwap = tpv_total / volume_total if volume_total > 0 else 0.0
        self.vwap_atual = vwap
        
        # Calcular desvios padrão
        prices = [(c['high'] + c['low'] + c['close']) / 3 for c in candles]
        std = np.std(prices)
        
        self.desvios_vwap = {
            -3: vwap - 3 * std,
            -2: vwap - 2 * std,
            -1: vwap - std,
            0: vwap,
            1: vwap + std,
            2: vwap + 2 * std,
            3: vwap + 3 * std
        }
        
        return vwap
    
    def analisar_vwap(self, preco_atual: float) -> SinalVWAP:
        """Analisar posição atual em relação ao VWAP"""
        if self.vwap_atual == 0:
            return SinalVWAP(preco_atual, 0, 0, 0, "neutro", "neutro", 0)
        
        distancia = preco_atual - self.vwap_atual
        distancia_percent = (distancia / self.vwap_atual) * 100
        
        # Determinar tendência
        if distancia_percent > 0.5:
            tendencia = "acima"
        elif distancia_percent < -0.5:
            tendencia = "abaixo"
        else:
            tendencia = "testando"
        
        # Gerar sinal
        if distancia_percent > 1.5:
            sinal = "venda"
            forca = min(1.0, abs(distancia_percent) / 3)
        elif distancia_percent < -1.5:
            sinal = "compra"
            forca = min(1.0, abs(distancia_percent) / 3)
        else:
            sinal = "neutro"
            forca = 0.5
        
        # Calcular desvio padrão atual
        std_atual = self.desvios_vwap.get(1, self.vwap_atual) - self.vwap_atual
        
        return SinalVWAP(
            preco_atual=preco_atual,
            vwap=self.vwap_atual,
            desvio_std=std_atual,
            distancia_vwap_percent=distancia_percent,
            tendencia=tendencia,
            sinal=sinal,
            forca=forca
        )
    
    def construir_volume_profile(
        self,
        candles: List[Dict[str, Any]],
        niveis: int = 24
    ) -> Dict[float, NivelVolume]:
        """Construir perfil de volume"""
        if not candles:
            return {}
        
        # Encontrar range
        min_price = min(c['low'] for c in candles)
        max_price = max(c['high'] for c in candles)
        range_price = max_price - min_price
        
        if range_price == 0:
            return {}
        
        step = range_price / niveis
        
        # Inicializar níveis
        profile = {}
        for i in range(niveis + 1):
            preco = min_price + i * step
            profile[preco] = NivelVolume(
                preco=preco,
                volume_total=0,
                volume_compra=0,
                volume_venda=0,
                numero_candles=0
            )
        
        # Preencher com dados
        for candle in candles:
            preco_representativo = round((candle['low'] + candle['high']) / 2 / step) * step + min_price
            if preco_representativo in profile:
                profile[preco_representativo].volume_total += candle['volume']
                profile[preco_representativo].numero_candles += 1
                
                # Estimar delta (compra vs venda)
                if candle['close'] > candle['open']:
                    profile[preco_representativo].volume_compra += candle['volume'] * 0.6
                    profile[preco_representativo].volume_venda += candle['volume'] * 0.4
                else:
                    profile[preco_representativo].volume_compra += candle['volume'] * 0.4
                    profile[preco_representativo].volume_venda += candle['volume'] * 0.6
        
        # Encontrar POC (nível com maior volume)
        max_volume = max(nv.volume_total for nv in profile.values())
        for nv in profile.values():
            if nv.volume_total == max_volume:
                nv.poc = True
                self.poc = nv.preco
        
        # Definir Value Area (70% do volume)
        volumes_ordenados = sorted([nv.volume_total for nv in profile.values()], reverse=True)
        volume_total = sum(volumes_ordenados)
        volume_va = 0
        indices_va = []
        
        for i, vol in enumerate(volumes_ordenados):
            volume_va += vol
            indices_va.append(i)
            if volume_va >= volume_total * 0.7:
                break
        
        self.volume_profile = profile
        
        return profile
    
    def identificar_suportes_resistencias(self, min_touch: int = 2) -> Dict[str, List[float]]:
        """Identificar suportes e resistências dinâmicos"""
        if not self.volume_profile:
            return {'suportes': [], 'resistencias': []}
        
        # Níveis com alto volume são suportes/resistências potenciais
        niveis_relevantes = [
            nv.preco for nv in self.volume_profile.values()
            if nv.volume_total > 0 and nv.numero_candles >= min_touch
        ]
        
        # Separar em suportes (abaixo do preço atual) e resistências (acima)
        preco_atual = self.estatisticas_intraday.abertura if self.estatisticas_intraday else 0
        
        suportes = sorted([n for n in niveis_relevantes if n < preco_atual], reverse=True)[:3]
        resistencias = sorted([n for n in niveis_relevantes if n > preco_atual])[:3]
        
        self.suportes_intraday = suportes
        self.resistencias_intraday = resistencias
        
        return {'suportes': suportes, 'resistencias': resistencias}
    
    def detectar_breakout(
        self,
        preco_atual: float,
        volume_atual: float,
        lookback: int = 20
    ) -> Dict[str, Any]:
        """Detectar possível breakout/breakdown"""
        if not self.resistencias_intraday or not self.suportes_intraday:
            return {'breakout': False, 'breakdown': False}
        
        # Volume acima da média
        volume_acima_media = False
        if self.estatisticas_intraday:
            volume_acima_media = volume_atual > self.estatisticas_intraday.volume_medio_hora * 1.5
        
        # Testar resistências
        breakout = False
        for res in self.resistencias_intraday:
            if preco_atual > res * 1.005:  # 0.5% acima
                breakout = True
                break
        
        # Testar suportes
        breakdown = False
        for sup in self.suportes_intraday:
            if preco_atual < sup * 0.995:  # 0.5% abaixo
                breakdown = True
                break
        
        return {
            'breakout': breakout and volume_acima_media,
            'breakdown': breakdown and volume_acima_media,
            'volume_confirmado': volume_acima_media,
            'forca': 0.8 if volume_acima_media else 0.4
        }
    
    def analisar_momentum(self, candles: List[Dict[str, Any]], periodo: int = 14) -> Dict[str, Any]:
        """Analisar momentum do ativo"""
        if len(candles) < periodo:
            return {'momentum': 0, 'direcao': 'neutro'}
        
        closes = [c['close'] for c in candles[-periodo:]]
        
        # RSI simplificado
        ganhos = []
        perdas = []
        
        for i in range(1, len(closes)):
            variacao = closes[i] - closes[i-1]
            if variacao > 0:
                ganhos.append(variacao)
                perdas.append(0)
            else:
                ganhos.append(0)
                perdas.append(abs(variacao))
        
        media_ganhos = np.mean(ganhos) if ganhos else 0
        media_perdas = np.mean(perdas) if perdas else 0
        
        if media_perdas == 0:
            rsi = 100
        else:
            rs = media_ganhos / media_perdas
            rsi = 100 - (100 / (1 + rs))
        
        # Direção
        if rsi > 70:
            direcao = "sobrecomprado"
        elif rsi < 30:
            direcao = "sobrevendido"
        elif rsi > 50:
            direcao = "alta"
        else:
            direcao = "baixa"
        
        return {
            'rsi': rsi,
            'momentum': (rsi - 50) / 50,  # Normalizado -1 a 1
            'direcao': direcao,
            'forca': abs(rsi - 50) / 50
        }
    
    def gerar_setup_scalping(
        self,
        preco_atual: float,
        momentum: Dict[str, Any],
        vwap_signal: SinalVWAP,
        liquidez: AnaliseLiquidez
    ) -> Optional[SetupDayTrade]:
        """Gerar setup de scalping"""
        # Verificar liquidez mínima
        if liquidez.qualidade_liquidez == "baixa":
            return None
        
        setup_id = hashlib.md5(f"scalp_{preco_atual}{datetime.now(timezone.utc)}".encode()).hexdigest()[:12]
        
        # Lógica de entrada
        if vwap_signal.sinal == "compra" and momentum['direcao'] == "sobrevendido":
            tipo = TipoSetup.COMPRA_AGRESSIVA
            entrada = preco_atual
            stop = entrada - (entrada * 0.002)  # 0.2% de stop
            alvo1 = entrada + (entrada * 0.004)  # 0.4% alvo 1
            alvo2 = entrada + (entrada * 0.006)  # 0.6% alvo 2
            alvo3 = entrada + (entrada * 0.008)  # 0.8% alvo 3
            
        elif vwap_signal.sinal == "venda" and momentum['direcao'] == "sobrecomprado":
            tipo = TipoSetup.VENDA_AGRESSIVA
            entrada = preco_atual
            stop = entrada + (entrada * 0.002)
            alvo1 = entrada - (entrada * 0.004)
            alvo2 = entrada - (entrada * 0.006)
            alvo3 = entrada - (entrada * 0.008)
        else:
            return None
        
        rr = abs(alvo1 - entrada) / abs(stop - entrada) if stop != entrada else 0
        
        setup = SetupDayTrade(
            id=setup_id,
            estrategia=EstrategiaDayTrade.SCALPING,
            tipo=tipo,
            entrada=entrada,
            stop_loss=stop,
            alvo_1=alvo1,
            alvo_2=alvo2,
            alvo_3=alvo3,
            risco_recompensa=rr,
            confianca=vwap_signal.forca * momentum['forca'],
            tempo_expiracao=15,  # 15 minutos
            motivacao=f"VWAP: {vwap_signal.tendencia}, Momentum: {momentum['direcao']}"
        )
        
        self.historico_setups.append(setup)
        self.hora_ultimo_setup = datetime.now(timezone.utc)
        
        return setup
    
    def analisar_liquidez(
        self,
        book: Dict[str, List[Dict]],
        volume_24h: float,
        trades_ultimo_minuto: int
    ) -> AnaliseLiquidez:
        """Analisar liquidez do ativo"""
        bids = book.get('bids', [])
        asks = book.get('asks', [])
        
        if not bids or not asks:
            return AnaliseLiquidez(0, 0, 0, 0, 0, 0, 0, "baixa")
        
        best_bid = bids[0]['price'] if bids else 0
        best_ask = asks[0]['price'] if asks else 0
        
        spread = ((best_ask - best_bid) / best_bid) * 100 if best_bid > 0 else 0
        
        # Depth
        depth_compra = sum(b['volume'] for b in bids[:10])
        depth_venda = sum(a['volume'] for a in asks[:10])
        
        # Impacto estimado
        impacto_1k = 0.1 if depth_compra > 10000 else 0.5
        impacto_10k = 0.5 if depth_compra > 100000 else 2.0
        
        # Qualidade
        if spread < 0.1 and volume_24h > 1000000 and trades_ultimo_minuto > 50:
            qualidade = "alta"
        elif spread < 0.5 and volume_24h > 100000:
            qualidade = "media"
        else:
            qualidade = "baixa"
        
        return AnaliseLiquidez(
            spread_atual=spread,
            spread_medio_24h=spread * 1.2,  # Estimado
            volume_ultima_hora=volume_24h / 24,
            depth_compra=depth_compra,
            depth_venda=depth_venda,
            impacto_1k=impacto_1k,
            impacto_10k=impacto_10k,
            qualidade_liquidez=qualidade
        )
    
    def calcular_tamanho_posicao(self, stop_loss_points: float) -> Dict[str, Any]:
        """Calcular tamanho ideal da posição baseado no risco"""
        risco_maximo = self.capital_por_trade * (self.risco_maximo_percent / 100)
        
        if stop_loss_points <= 0:
            return {'tamanho': 0, 'risco': 0}
        
        tamanho = risco_maximo / stop_loss_points
        risco_real = tamanho * stop_loss_points
        
        return {
            'tamanho': tamanho,
            'risco_monetario': risco_real,
            'risco_percentual': (risco_real / self.capital_por_trade) * 100,
            'alavancagem_sugerida': min(10, 1000 / stop_loss_points)  # Máx 10x
        }
    
    def identificar_momento_dia(self) -> MomentoDia:
        """Identificar momento atual do dia de trading"""
        agora = datetime.now(timezone.utc)
        hora = agora.hour
        minuto = agora.minute
        
        # Ajustar para horário de Brasília (UTC-3)
        hora_br = (hora - 3) % 24
        
        if hora_br < 9:
            return MomentoDia.PRE_MARKET
        elif hora_br == 9 and minuto < 30:
            return MomentoDia.OPEN
        elif hora_br < 12:
            return MomentoDia.MORNING
        elif hora_br < 14:
            return MomentoDia.MIDDAY
        elif hora_br < 17:
            return MomentoDia.AFTERNOON
        elif hora_br < 18:
            return MomentoDia.CLOSE
        else:
            return MomentoDia.AFTER_HOURS
    
    def avaliar_contexto_temporal(self) -> Dict[str, Any]:
        """Avaliar contexto temporal atual"""
        momento = self.identificar_momento_dia()
        
        contextos = {
            MomentoDia.PRE_MARKET: {
                'volatilidade_esperada': 'alta',
                'liquidez': 'baixa',
                'estrategia_sugerida': 'aguardar_abertura'
            },
            MomentoDia.OPEN: {
                'volatilidade_esperada': 'muito_alta',
                'liquidez': 'alta',
                'estrategia_sugerida': 'opening_range_breakout'
            },
            MomentoDia.MORNING: {
                'volatilidade_esperada': 'alta',
                'liquidez': 'alta',
                'estrategia_sugerida': 'momentum'
            },
            MomentoDia.MIDDAY: {
                'volatilidade_esperada': 'baixa',
                'liquidez': 'media',
                'estrategia_sugerida': 'range'
            },
            MomentoDia.AFTERNOON: {
                'volatilidade_esperada': 'media',
                'liquidez': 'alta',
                'estrategia_sugerida': 'trend_continuation'
            },
            MomentoDia.CLOSE: {
                'volatilidade_esperada': 'alta',
                'liquidez': 'muito_alta',
                'estrategia_sugerida': 'close_positions'
            }
        }
        
        return {
            'momento': momento.value,
            **contextos.get(momento, {})
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status da análise day trade"""
        return {
            'ativo': self.ativo,
            'capital_por_trade': self.capital_por_trade,
            'risco_maximo_percent': self.risco_maximo_percent,
            'vwap_atual': self.vwap_atual,
            'poc': self.poc,
            'suportes_intraday': self.suportes_intraday,
            'resistencias_intraday': self.resistencias_intraday,
            'setups_gerados_hoje': len([s for s in self.historico_setups 
                                       if datetime.fromisoformat(s.timestamp).date() == datetime.now(timezone.utc).date()]),
            'operacoes_hoje': len(self.operacoes_hoje),
            'momento_atual': self.identificar_momento_dia().value,
            'operacao_ativa': self.operacao_atual is not None
        }
