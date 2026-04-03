"""
VHALINOR Visão Computacional v6.0
=====================================
Sistema de visão computacional com:
- Análise de padrões visuais
- Reconhecimento de imagens
- Detecção de anomalias visuais
- Processamento de gráficos e charts
- Análise técnica visual

@module visao_computacional
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque
import numpy as np


class TipoVisao(Enum):
    """Tipos de análise visual"""
    PADRAO = "padrao"
    ANOMALIA = "anomalia"
    CLASSIFICACAO = "classificacao"
    DETECCAO = "deteccao"
    SEGMENTACAO = "segmentacao"
    RECONHECIMENTO = "reconhecimento"
    ANALISE_TECNICA = "analise_tecnica"
    OCR = "ocr"  # Reconhecimento de caracteres


@dataclass
class PadraoVisual:
    """Padrão visual detectado"""
    nome: str
    tipo: str
    coordenadas: List[Tuple[int, int]]
    confianca: float
    caracteristicas: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AnomaliaVisual:
    """Anomalia visual detectada"""
    tipo: str
    localizacao: Tuple[int, int, int, int]  # x, y, w, h
    severidade: float  # 0.0 a 1.0
    descricao: str
    confianca: float


@dataclass
class ResultadoVisao:
    """Resultado de análise visual"""
    tipo_analise: TipoVisao
    imagem_id: str
    dimensoes: Tuple[int, int]
    padroes: List[PadraoVisual] = field(default_factory=list)
    anomalias: List[AnomaliaVisual] = field(default_factory=list)
    classificacoes: List[Dict[str, Any]] = field(default_factory=list)
    texto_extraido: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class VisaoComputacional:
    """
    Sistema de visão computacional para análise de imagens e padrões visuais.
    """
    
    def __init__(self):
        self.modelos_carregados: Dict[str, Any] = {}
        self.historico_analises: deque = deque(maxlen=1000)
        
        # Padrões técnicos conhecidos
        self.padroes_tecnicos = self._carregar_padroes_tecnicos()
        
        # Biblioteca de formas
        self.formas_geometricas = self._carregar_formas_geometricas()
    
    def _carregar_padroes_tecnicos(self) -> Dict[str, Any]:
        """Carregar padrões técnicos de análise"""
        return {
            'candlestick': {
                'martelo': 'reversao_alta',
                'estrela_cadente': 'reversao_baixa',
                'doji': 'indecisao',
                'engolfo_alta': 'continuacao_alta',
                'engolfo_baixa': 'continuacao_baixa'
            },
            'chart': {
                'triangulo_ascendente': 'continuacao_alta',
                'triangulo_descendente': 'continuacao_baixa',
                'cabeca_ombros': 'reversao_baixa',
                'w': 'reversao_alta',
                'bandeira': 'continuacao'
            },
            'indicador': {
                'divergencia_bullish': 'reversao_alta',
                'divergencia_bearish': 'reversao_baixa',
                'cruzamento_dourado': 'compra',
                'cruzamento_morte': 'venda'
            }
        }
    
    def _carregar_formas_geometricas(self) -> Dict[str, Any]:
        """Carregar definições de formas geométricas"""
        return {
            'triangulo': {
                'vertices': 3,
                'angulos': [60, 60, 60],
                'descricao': 'Forma com três lados'
            },
            'retangulo': {
                'vertices': 4,
                'angulos': [90, 90, 90, 90],
                'descricao': 'Forma com quatro lados e ângulos retos'
            },
            'circulo': {
                'vertices': 0,
                'descricao': 'Forma arredondada'
            }
        }
    
    def analisar_chart(
        self,
        dados_precos: np.ndarray,
        tipo: str = 'candlestick'
    ) -> ResultadoVisao:
        """Analisar padrões em gráfico de preços"""
        padroes = []
        
        if tipo == 'candlestick' and len(dados_precos) >= 5:
            # Analisar padrões de candlestick
            padroes.extend(self._detectar_padroes_candlestick(dados_precos))
        
        # Analisar tendência
        tendencia = self._analisar_tendencia(dados_precos)
        
        # Analisar suporte e resistência
        niveis = self._detectar_suporte_resistencia(dados_precos)
        
        padroes.append(PadraoVisual(
            nome=f"tendencia_{tendencia['direcao']}",
            tipo='tendencia',
            coordenadas=[(0, 0)],
            confianca=tendencia['forca'],
            caracteristicas=tendencia
        ))
        
        for nivel in niveis:
            padroes.append(PadraoVisual(
                nome=f"nivel_{nivel['tipo']}",
                tipo='nivel_chave',
                coordenadas=[(int(nivel['posicao']), int(nivel['valor']))],
                confianca=nivel['forca'],
                caracteristicas=nivel
            ))
        
        return ResultadoVisao(
            tipo_analise=TipoVisao.ANALISE_TECNICA,
            imagem_id=f"chart_{datetime.now(timezone.utc).timestamp()}",
            dimensoes=(len(dados_precos), 1),
            padroes=padroes,
            anomalias=[]
        )
    
    def _detectar_padroes_candlestick(
        self,
        dados: np.ndarray
    ) -> List[PadraoVisual]:
        """Detectar padrões de candlestick"""
        padroes = []
        
        # Analisar últimos 5 candles
        n = len(dados)
        if n < 5:
            return padroes
        
        ultimos = dados[-5:]
        
        # Verificar martelo
        for i, candle in enumerate(ultimos):
            open_p, high, low, close = candle[:4]
            
            corpo = abs(close - open_p)
            sombra_inferior = min(open_p, close) - low
            sombra_superior = high - max(open_p, close)
            
            # Martelo: sombra inferior grande, corpo pequeno no topo
            if sombra_inferior > 2 * corpo and sombra_superior < corpo:
                padroes.append(PadraoVisual(
                    nome='martelo',
                    tipo='candlestick',
                    coordenadas=[(n-5+i, int(close))],
                    confianca=0.7,
                    caracteristicas={'direcao': 'alta'}
                ))
            
            # Doji: corpo muito pequeno
            if corpo < 0.1 * (high - low):
                padroes.append(PadraoVisual(
                    nome='doji',
                    tipo='candlestick',
                    coordenadas=[(n-5+i, int(close))],
                    confianca=0.6,
                    caracteristicas={'direcao': 'indecisao'}
                ))
        
        return padroes
    
    def _analisar_tendencia(self, dados: np.ndarray) -> Dict[str, Any]:
        """Analisar tendência dos dados"""
        if len(dados) < 10:
            return {'direcao': 'indefinida', 'forca': 0.0}
        
        # Calcular médias móveis
        closes = dados[:, 3]  # Preços de fechamento
        
        mm7 = np.mean(closes[-7:]) if len(closes) >= 7 else closes[-1]
        mm20 = np.mean(closes[-20:]) if len(closes) >= 20 else mm7
        
        # Determinar direção
        if mm7 > mm20 * 1.02:
            direcao = 'alta'
            forca = min(1.0, (mm7 / mm20 - 1) * 50)
        elif mm7 < mm20 * 0.98:
            direcao = 'baixa'
            forca = min(1.0, (1 - mm7 / mm20) * 50)
        else:
            direcao = 'lateral'
            forca = 0.3
        
        return {
            'direcao': direcao,
            'forca': forca,
            'mm7': mm7,
            'mm20': mm20
        }
    
    def _detectar_suporte_resistencia(
        self,
        dados: np.ndarray
    ) -> List[Dict[str, Any]]:
        """Detectar níveis de suporte e resistência"""
        niveis = []
        
        if len(dados) < 20:
            return niveis
        
        # Extrair highs e lows
        highs = dados[:, 1]
        lows = dados[:, 2]
        
        # Encontrar máximos e mínimos locais
        for i in range(2, len(dados) - 2):
            # Máximo local
            if highs[i] > highs[i-1] and highs[i] > highs[i-2] and \
               highs[i] > highs[i+1] and highs[i] > highs[i+2]:
                niveis.append({
                    'tipo': 'resistencia',
                    'valor': float(highs[i]),
                    'posicao': i,
                    'forca': 0.6 + (highs[i] - np.mean(highs)) / np.std(highs) * 0.1
                })
            
            # Mínimo local
            if lows[i] < lows[i-1] and lows[i] < lows[i-2] and \
               lows[i] < lows[i+1] and lows[i] < lows[i+2]:
                niveis.append({
                    'tipo': 'suporte',
                    'valor': float(lows[i]),
                    'posicao': i,
                    'forca': 0.6 + (np.mean(lows) - lows[i]) / np.std(lows) * 0.1
                })
        
        # Ordenar por força e limitar
        niveis.sort(key=lambda x: x['forca'], reverse=True)
        return niveis[:5]
    
    def detectar_anomalias(
        self,
        dados: np.ndarray,
        threshold: float = 2.0
    ) -> List[AnomaliaVisual]:
        """Detectar anomalias visuais nos dados"""
        anomalias = []
        
        if len(dados) < 10:
            return anomalias
        
        closes = dados[:, 3]
        
        # Calcular estatísticas
        media = np.mean(closes)
        desvio = np.std(closes)
        
        # Detectar outliers
        for i, valor in enumerate(closes):
            z_score = abs(valor - media) / desvio if desvio > 0 else 0
            
            if z_score > threshold:
                anomalias.append(AnomaliaVisual(
                    tipo='outlier_preco',
                    localizacao=(i-2, int(valor)-10, 4, 20),
                    severidade=min(1.0, z_score / 5),
                    descricao=f'Preço anormal: {valor:.2f} (z-score: {z_score:.2f})',
                    confianca=min(1.0, z_score / 3)
                ))
        
        # Detectar gaps
        for i in range(1, len(dados)):
            gap = dados[i, 0] - dados[i-1, 3]  # Open atual - Close anterior
            gap_pct = abs(gap) / dados[i-1, 3] if dados[i-1, 3] > 0 else 0
            
            if gap_pct > 0.02:  # Gap maior que 2%
                anomalias.append(AnomaliaVisual(
                    tipo='gap',
                    localizacao=(i-1, int(dados[i-1, 3]), 2, int(abs(gap))),
                    severancia=min(1.0, gap_pct * 10),
                    descricao=f'Gap de {gap_pct:.1%} detectado',
                    confianca=0.8
                ))
        
        return anomalias
    
    def classificar_imagem(
        self,
        caracteristicas: Dict[str, Any],
        categorias: Optional[List[str]] = None
    ) -> ResultadoVisao:
        """Classificar imagem baseada em características"""
        # Simplificação: classificação baseada em regras
        classificacoes = []
        
        if categorias is None:
            categorias = ['chart', 'indicador', 'tabela', 'texto', 'outro']
        
        # Detectar tipo baseado em características
        if 'dados_precos' in caracteristicas:
            classificacoes.append({
                'categoria': 'chart',
                'confianca': 0.9,
                'subtipo': caracteristicas.get('tipo_chart', 'desconhecido')
            })
        
        if 'linhas' in caracteristicas and caracteristicas['linhas'] > 0:
            classificacoes.append({
                'categoria': 'indicador',
                'confianca': 0.7,
                'subtipo': 'linha'
            })
        
        if 'texto_detectado' in caracteristicas:
            classificacoes.append({
                'categoria': 'texto',
                'confianca': caracteristicas.get('confianca_texto', 0.5),
                'subtipo': 'ocr'
            })
        
        return ResultadoVisao(
            tipo_analise=TipoVisao.CLASSIFICACAO,
            imagem_id=caracteristicas.get('id', 'unknown'),
            dimensoes=caracteristicas.get('dimensoes', (0, 0)),
            classificacoes=classificacoes
        )
    
    def extrair_texto(
        self,
        dados_imagem: Any
    ) -> ResultadoVisao:
        """Extrair texto de imagem (OCR simplificado)"""
        # Simplificação: simulação de OCR
        # Em implementação real, usaria Tesseract ou similar
        
        return ResultadoVisao(
            tipo_analise=TipoVisao.OCR,
            imagem_id='ocr_simulado',
            dimensoes=(100, 100),
            texto_extraido='Texto extraído (simulação)'
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de visão"""
        return {
            'modelos_carregados': len(self.modelos_carregados),
            'padroes_tecnicos': len(self.padroes_tecnicos),
            'formas_geometricas': len(self.formas_geometricas),
            'analises_realizadas': len(self.historico_analises),
            'tipos_analise_suportados': [t.value for t in TipoVisao]
        }
