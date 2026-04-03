"""
VHALINOR Análise Profunda de Padrões v6.0
=============================================
Sistema de análise profunda de padrões com:
- Reconhecimento de padrões complexos
- Mineração de dados sequenciais
- Detecção de anomalias em padrões
- Análise de séries temporais
- Padrões gráficos e técnicos
- Clustering de padrões
- Predição de padrões futuros
- Análise de frequência e ciclos
- Padrões de mercado (candlestick, formações)
- Similaridade de padrões

@module analise_profunda_padroes
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque, defaultdict
import hashlib
import math
from scipy import signal
from scipy.fft import fft, fftfreq
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import StandardScaler


class TipoPadrao(Enum):
    """Tipos de padrões analisáveis"""
    TENDENCIA = "tendencia"
    REVERSAO = "reversao"
    CONSOLIDACAO = "consolidacao"
    VOLATILIDADE = "volatilidade"
    CICLO = "ciclo"
    SEQUENCIAL = "sequencial"
    GRAFICO = "grafico"
    CANDLESTICK = "candlestick"
    INDICADOR = "indicador"
    CORRELACAO = "correlacao"
    ANOMALIA = "anomalia"
    FREQUENCIA = "frequencia"


class FormacaoGrafica(Enum):
    """Formações gráficas de análise técnica"""
    TRIANGULO_ASCENDENTE = "triangulo_ascendente"
    TRIANGULO_DESCENDENTE = "triangulo_descendente"
    TRIANGULO_SIMETRICO = "triangulo_simetrico"
    CABECA_OMBROS = "cabeca_ombros"
    CABECA_OMBROS_INVERTIDO = "cabeca_ombros_invertido"
    W = "w"
    M = "m"
    BANDEIRA = "bandeira"
    BANDEIRA_BAIXA = "bandeira_baixa"
    RETANGULO = "retangulo"
    CANAL_ASCENDENTE = "canal_ascendente"
    CANAL_DESCENDENTE = "canal_descendente"
    TOPO_DUPLO = "topo_duplo"
    FUNDO_DUPLO = "fundo_duplo"


class PadraoCandlestick(Enum):
    """Padrões de candlestick"""
    MARTELO = "martelo"
    MARTELO_INVERTIDO = "martelo_invertido"
    ENGOLFO_ALTA = "engolfo_alta"
    ENGOLFO_BAIXA = "engolfo_baixa"
    ESTRELA_MORNING = "estrela_morning"
    ESTRELA_EVENING = "estrela_evening"
    DOJI = "doji"
    DOJI_DRAGONFLY = "doji_dragonfly"
    DOJI_GRAVESTONE = "doji_gravestone"
    HAMMER = "hammer"
    HANGING_MAN = "hanging_man"
    SHOOTING_STAR = "shooting_star"
    THREE_WHITE_SOLDIERS = "three_white_soldiers"
    THREE_BLACK_CROWS = "three_black_crows"


@dataclass
class PadraoDetectado:
    """Padrão detectado na análise"""
    id: str
    tipo: TipoPadrao
    nome: str
    posicao_inicio: int
    posicao_fim: int
    dados: np.ndarray
    confianca: float
    forca: float  # 0.0 a 1.0
    descricao: str
    implicacao: str  # "bullish", "bearish", "neutra"
    alvo_preco: Optional[float] = None
    stop_loss: Optional[float] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    @property
    def duracao(self) -> int:
        return self.posicao_fim - self.posicao_inicio


@dataclass
class CicloDetectado:
    """Ciclo detectado em série temporal"""
    frequencia: float
    periodo: float
    amplitude: float
    fase: float
    potencia: float
    significancia: float


@dataclass
class AnomaliaPadrao:
    """Anomalia detectada em padrão"""
    posicao: int
    tipo: str
    severidade: float
    valor_esperado: float
    valor_observado: float
    desvio: float
    descricao: str


class AnaliseProfundaPadroes:
    """
    Sistema de análise profunda de padrões para trading.
    """
    
    def __init__(self, window_size: int = 50):
        self.window_size = window_size
        self.historico_padroes: deque = deque(maxlen=1000)
        self.padroes_catalogados: Dict[str, Dict] = self._inicializar_catalogo_padroes()
        self.clusters_padroes: Optional[Any] = None
        self.scaler = StandardScaler()
    
    def _inicializar_catalogo_padroes(self) -> Dict[str, Dict]:
        """Inicializar catálogo de padrões conhecidos"""
        return {
            # Padrões de candlestick
            'martelo': {
                'tipo': TipoPadrao.CANDLESTICK,
                'condicoes': ['corpo_pequeno', 'sombra_inferior_grande', 'sombra_superior_pequena'],
                'implicacao': 'bullish',
                'confianca_minima': 0.7
            },
            'engolfo_alta': {
                'tipo': TipoPadrao.CANDLESTICK,
                'condicoes': ['candle_atual_maior', 'fecha_acima_anterior', 'abre_abaixo_anterior'],
                'implicacao': 'bullish',
                'confianca_minima': 0.75
            },
            'estrela_cadente': {
                'tipo': TipoPadrao.CANDLESTICK,
                'condicoes': ['corpo_pequeno', 'sombra_superior_grande', 'sombra_inferior_pequena'],
                'implicacao': 'bearish',
                'confianca_minima': 0.7
            },
            # Formações gráficas
            'cabeca_ombros': {
                'tipo': TipoPadrao.GRAFICO,
                'topos': 3,
                'topo_central_maior': True,
                'implicacao': 'bearish',
                'confianca_minima': 0.8,
                'pontos_chave': ['ombro_esquerdo', 'cabeca', 'ombro_direito', 'linha_pescoco']
            },
            'fundo_duplo': {
                'tipo': TipoPadrao.GRAFICO,
                'fundos': 2,
                'aproximadamente_iguais': True,
                'implicacao': 'bullish',
                'confianca_minima': 0.75
            }
        }
    
    def analisar_candlestick(self, dados: np.ndarray) -> List[PadraoDetectado]:
        """Analisar padrões de candlestick"""
        padroes = []
        n = len(dados)
        
        for i in range(2, n):  # Precisa de pelo menos 3 candles
            open_c = dados[i, 0]
            high = dados[i, 1]
            low = dados[i, 2]
            close = dados[i, 3]
            
            # Candle anterior
            open_prev = dados[i-1, 0]
            close_prev = dados[i-1, 3]
            
            corpo = abs(close - open_c)
            sombra_superior = high - max(open_c, close)
            sombra_inferior = min(open_c, close) - low
            range_total = high - low
            
            # Martelo
            if (corpo < 0.3 * range_total and 
                sombra_inferior > 2 * corpo and 
                sombra_superior < 0.1 * range_total):
                
                padroes.append(PadraoDetectado(
                    id=f"cs_{i}_martelo",
                    tipo=TipoPadrao.CANDLESTICK,
                    nome=PadraoCandlestick.MARTELO.value,
                    posicao_inicio=i,
                    posicao_fim=i,
                    dados=dados[i:i+1],
                    confianca=0.7 + (sombra_inferior / range_total) * 0.2,
                    forca=sombra_inferior / range_total,
                    descricao=f"Martelo detectado em índice {i}",
                    implicacao="bullish"
                ))
            
            # Engolfo de alta
            if (close > open_c and  # Candle atual bullish
                close > open_prev and close > close_prev and  # Engolfe anterior
                open_c < close_prev):  # Abriu abaixo do fechamento anterior
                
                padroes.append(PadraoDetectado(
                    id=f"cs_{i}_engolfo_alta",
                    tipo=TipoPadrao.CANDLESTICK,
                    nome=PadraoCandlestick.ENGOLFO_ALTA.value,
                    posicao_inicio=i-1,
                    posicao_fim=i,
                    dados=dados[i-1:i+1],
                    confianca=0.75,
                    forca=0.7,
                    descricao=f"Engolfo de alta detectado em índice {i}",
                    implicacao="bullish"
                ))
            
            # Doji
            if corpo < 0.1 * range_total:
                padroes.append(PadraoDetectado(
                    id=f"cs_{i}_doji",
                    tipo=TipoPadrao.CANDLESTICK,
                    nome=PadraoCandlestick.DOJI.value,
                    posicao_inicio=i,
                    posicao_fim=i,
                    dados=dados[i:i+1],
                    confianca=0.8,
                    forca=0.5,
                    descricao=f"Doji detectado em índice {i}",
                    implicacao="neutra"
                ))
        
        return padroes
    
    def detectar_formacao_grafica(
        self,
        dados: np.ndarray,
        formacao: FormacaoGrafica
    ) -> Optional[PadraoDetectado]:
        """Detectar formação gráfica específica"""
        highs = dados[:, 1]
        lows = dados[:, 2]
        
        if formacao == FormacaoGrafica.CABECA_OMBROS:
            return self._detectar_cabeca_ombros(highs, lows, dados)
        elif formacao == FormacaoGrafica.FUNDO_DUPLO:
            return self._detectar_fundo_duplo(highs, lows, dados)
        elif formacao == FormacaoGrafica.TOPO_DUPLO:
            return self._detectar_topo_duplo(highs, lows, dados)
        
        return None
    
    def _detectar_cabeca_ombros(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        dados: np.ndarray
    ) -> Optional[PadraoDetectado]:
        """Detectar padrão cabeça e ombros"""
        # Encontrar máximos locais
        maximos = []
        for i in range(5, len(highs) - 5):
            if highs[i] > max(highs[i-5:i]) and highs[i] > max(highs[i+1:i+6]):
                maximos.append((i, highs[i]))
        
        if len(maximos) < 3:
            return None
        
        # Procurar configuração cabeça e ombros
        for i in range(len(maximos) - 2):
            ombro_esq = maximos[i]
            cabeca = maximos[i+1]
            ombro_dir = maximos[i+2]
            
            # Verificar se cabeça é maior que ombros
            if (cabeca[1] > ombro_esq[1] and cabeca[1] > ombro_dir[1] and
                abs(ombro_esq[1] - ombro_dir[1]) / cabeca[1] < 0.15):  # Ombros aproximadamente iguais
                
                return PadraoDetectado(
                    id=f"cg_cabeca_ombros_{ombro_esq[0]}",
                    tipo=TipoPadrao.GRAFICO,
                    nome=FormacaoGrafica.CABECA_OMBROS.value,
                    posicao_inicio=ombro_esq[0],
                    posicao_fim=ombro_dir[0],
                    dados=dados[ombro_esq[0]:ombro_dir[0]+1],
                    confianca=0.8,
                    forca=0.75,
                    descricao="Cabeça e ombros detectado",
                    implicacao="bearish",
                    alvo_preco=ombro_dir[1] - (cabeca[1] - min(lows[ombro_esq[0]:ombro_dir[0]+1])),
                    stop_loss=cabeca[1] * 1.02
                )
        
        return None
    
    def _detectar_fundo_duplo(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        dados: np.ndarray
    ) -> Optional[PadraoDetectado]:
        """Detectar padrão fundo duplo"""
        # Encontrar mínimos locais
        minimos = []
        for i in range(5, len(lows) - 5):
            if lows[i] < min(lows[i-5:i]) and lows[i] < min(lows[i+1:i+6]):
                minimos.append((i, lows[i]))
        
        if len(minimos) < 2:
            return None
        
        # Procurar fundo duplo
        for i in range(len(minimos) - 1):
            fundo1 = minimos[i]
            fundo2 = minimos[i+1]
            
            # Verificar se fundos são aproximadamente iguais
            diferenca_relativa = abs(fundo1[1] - fundo2[1]) / fundo1[1]
            
            if diferenca_relativa < 0.05:  # 5% de tolerância
                pico_meio = max(highs[fundo1[0]:fundo2[0]])
                
                return PadraoDetectado(
                    id=f"cg_fundo_duplo_{fundo1[0]}",
                    tipo=TipoPadrao.GRAFICO,
                    nome=FormacaoGrafica.FUNDO_DUPLO.value,
                    posicao_inicio=fundo1[0],
                    posicao_fim=fundo2[0],
                    dados=dados[fundo1[0]:fundo2[0]+1],
                    confianca=0.75,
                    forca=1.0 - diferenca_relativa,
                    descricao="Fundo duplo detectado",
                    implicacao="bullish",
                    alvo_preco=pico_meio + (pico_meio - fundo1[1]),
                    stop_loss=min(fundo1[1], fundo2[1]) * 0.98
                )
        
        return None
    
    def _detectar_topo_duplo(
        self,
        highs: np.ndarray,
        lows: np.ndarray,
        dados: np.ndarray
    ) -> Optional[PadraoDetectado]:
        """Detectar padrão topo duplo"""
        maximos = []
        for i in range(5, len(highs) - 5):
            if highs[i] > max(highs[i-5:i]) and highs[i] > max(highs[i+1:i+6]):
                maximos.append((i, highs[i]))
        
        if len(maximos) < 2:
            return None
        
        for i in range(len(maximos) - 1):
            topo1 = maximos[i]
            topo2 = maximos[i+1]
            
            diferenca_relativa = abs(topo1[1] - topo2[1]) / topo1[1]
            
            if diferenca_relativa < 0.05:
                vale_meio = min(lows[topo1[0]:topo2[0]])
                
                return PadraoDetectado(
                    id=f"cg_topo_duplo_{topo1[0]}",
                    tipo=TipoPadrao.GRAFICO,
                    nome=FormacaoGrafica.TOPO_DUPLO.value,
                    posicao_inicio=topo1[0],
                    posicao_fim=topo2[0],
                    dados=dados[topo1[0]:topo2[0]+1],
                    confianca=0.75,
                    forca=1.0 - diferenca_relativa,
                    descricao="Topo duplo detectado",
                    implicacao="bearish",
                    alvo_preco=vale_meio - (topo1[1] - vale_meio),
                    stop_loss=max(topo1[1], topo2[1]) * 1.02
                )
        
        return None
    
    def analisar_ciclos(self, dados: np.ndarray) -> List[CicloDetectado]:
        """Analisar ciclos em série temporal usando FFT"""
        closes = dados[:, 3]
        n = len(closes)
        
        # Remover tendência
        detrended = signal.detrend(closes)
        
        # FFT
        yf = fft(detrended)
        xf = fftfreq(n, 1)
        
        # Potência
        potencia = np.abs(yf)**2
        
        # Encontrar picos
        picos_indices = signal.find_peaks(potencia[:n//2], height=np.max(potencia)*0.1)[0]
        
        ciclos = []
        for idx in picos_indices[:5]:  # Top 5 ciclos
            frequencia = xf[idx]
            periodo = 1 / frequencia if frequencia != 0 else float('inf')
            
            ciclo = CicloDetectado(
                frequencia=frequencia,
                periodo=periodo,
                amplitude=np.abs(yf[idx]) / n * 2,
                fase=np.angle(yf[idx]),
                potencia=potencia[idx],
                significancia=potencia[idx] / np.sum(potencia)
            )
            ciclos.append(ciclo)
        
        return sorted(ciclos, key=lambda x: x.potencia, reverse=True)
    
    def detectar_anomalias_padrao(
        self,
        dados: np.ndarray,
        threshold: float = 2.5
    ) -> List[AnomaliaPadrao]:
        """Detectar anomalias em padrões"""
        anomalias = []
        closes = dados[:, 3]
        
        # Estatísticas
        media = np.mean(closes)
        desvio = np.std(closes)
        
        # Z-score
        z_scores = np.abs((closes - media) / desvio)
        
        for i, z in enumerate(z_scores):
            if z > threshold:
                valor_esperado = media
                valor_observado = closes[i]
                
                anomalias.append(AnomaliaPadrao(
                    posicao=i,
                    tipo="outlier_estatistico",
                    severidade=min(1.0, z / 5),
                    valor_esperado=valor_esperado,
                    valor_observado=valor_observado,
                    desvio=abs(valor_observado - valor_esperado),
                    descricao=f"Anomalia estatística em índice {i} (z-score: {z:.2f})"
                ))
        
        return anomalias
    
    def clusterizar_padroes(
        self,
        padroes: List[PadraoDetectado],
        n_clusters: int = 5
    ) -> Dict[int, List[PadraoDetectado]]:
        """Clusterizar padrões similares"""
        if len(padroes) < n_clusters:
            return {i: [p] for i, p in enumerate(padroes)}
        
        # Extrair features
        features = []
        for padrao in padroes:
            feat = [
                padrao.forca,
                padrao.confianca,
                float(padrao.duracao),
                1.0 if padrao.implicacao == "bullish" else 0.0,
                1.0 if padrao.implicacao == "bearish" else 0.5
            ]
            features.append(feat)
        
        features = np.array(features)
        features_scaled = self.scaler.fit_transform(features)
        
        # Clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        labels = kmeans.fit_predict(features_scaled)
        
        # Agrupar
        clusters = defaultdict(list)
        for padrao, label in zip(padroes, labels):
            clusters[label].append(padrao)
        
        return dict(clusters)
    
    def calcular_similaridade_padroes(
        self,
        padrao1: PadraoDetectado,
        padrao2: PadraoDetectado
    ) -> float:
        """Calcular similaridade entre dois padrões"""
        # Similaridade de forma (correlação)
        if len(padrao1.dados) == len(padrao2.dados):
            corr = np.corrcoef(
                padrao1.dados[:, 3],  # Close
                padrao2.dados[:, 3]
            )[0, 1]
            similaridade_forma = (corr + 1) / 2  # Normalizar para [0, 1]
        else:
            similaridade_forma = 0.5
        
        # Similaridade de tipo
        similaridade_tipo = 1.0 if padrao1.tipo == padrao2.tipo else 0.0
        
        # Similaridade de implicação
        similaridade_implicacao = 1.0 if padrao1.implicacao == padrao2.implicacao else 0.0
        
        # Média ponderada
        return (
            similaridade_forma * 0.5 +
            similaridade_tipo * 0.3 +
            similaridade_implicacao * 0.2
        )
    
    def prever_proximo_padrao(
        self,
        historico_padroes: List[PadraoDetectado],
        dados_atuais: np.ndarray
    ) -> Dict[str, Any]:
        """Prever próximo padrão baseado em histórico"""
        if len(historico_padroes) < 3:
            return {'predicao': 'insuficiente_dados', 'confianca': 0.0}
        
        # Analisar sequência de padrões
        sequencia = [p.implicacao for p in historico_padroes[-10:]]
        
        # Contar frequências
        contagem = {}
        for imp in sequencia:
            contagem[imp] = contagem.get(imp, 0) + 1
        
        # Predição baseada em frequência
        total = len(sequencia)
        probabilidades = {k: v/total for k, v in contagem.items()}
        
        mais_provavel = max(probabilidades, key=probabilidades.get)
        
        return {
            'predicao': mais_provavel,
            'confianca': probabilidades[mais_provavel],
            'probabilidades': probabilidades,
            'baseado_em': len(sequencia)
        }
    
    def analise_completa(self, dados: np.ndarray) -> Dict[str, Any]:
        """Realizar análise completa de padrões"""
        # 1. Análise de candlestick
        padroes_cs = self.analisar_candlestick(dados)
        
        # 2. Análise de ciclos
        ciclos = self.analisar_ciclos(dados)
        
        # 3. Detecção de anomalias
        anomalias = self.detectar_anomalias_padrao(dados)
        
        # 4. Formações gráficas
        formacoes = []
        for formacao in [FormacaoGrafica.CABECA_OMBROS, FormacaoGrafica.FUNDO_DUPLO]:
            padrao = self.detectar_formacao_grafica(dados, formacao)
            if padrao:
                formacoes.append(padrao)
        
        # 5. Todos os padrões
        todos_padroes = padroes_cs + formacoes
        
        # 6. Clustering
        clusters = self.clusterizar_padroes(todos_padroes)
        
        # 7. Predição
        predicao = self.prever_proximo_padrao(todos_padroes, dados)
        
        return {
            'padroes_candlestick': len(padroes_cs),
            'padroes_graficos': len(formacoes),
            'total_padroes': len(todos_padroes),
            'ciclos_detectados': len(ciclos),
            'anomalias': len(anomalias),
            'clusters': len(clusters),
            'predicao_proximo_padrao': predicao,
            'padroes_bullish': len([p for p in todos_padroes if p.implicacao == 'bullish']),
            'padroes_bearish': len([p for p in todos_padroes if p.implicacao == 'bearish']),
            'analise_timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de análise de padrões"""
        return {
            'window_size': self.window_size,
            'padroes_catalogados': len(self.padroes_catalogados),
            'historico_padroes': len(self.historico_padroes),
            'tipos_padroes_suportados': [t.value for t in TipoPadrao],
            'formacoes_graficas_suportadas': [f.value for f in FormacaoGrafica],
            'padroes_candlestick_suportados': [p.value for p in PadraoCandlestick]
        }
