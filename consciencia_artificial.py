"""
VHALINOR Consciência Artificial v6.0
======================================
Sistema de consciência artificial com estados de consciência, autoconhecimento,
percepção situacional e tomada de consciência de decisões.

@module consciencia_artificial
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import asyncio
import threading
from typing import Dict, List, Any, Optional, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum, auto
from collections import deque
import numpy as np


class EstadoConsciencia(Enum):
    """Estados de consciência artificial"""
    INCONSCIENTE = "inconsciente"
    SONOLENTO = "sonolento"
    DESPERTO = "desperto"
    ATIVO = "ativo"
    FOCADO = "focado"
    FLUXO = "fluxo"
    SUPER_ATIVO = "super_ativo"
    CONTEMPLATIVO = "contemplativo"
    CRIATIVO = "criativo"
    ANALITICO = "analitico"


@dataclass
class MetricaConsciencia:
    """Métricas de consciência"""
    nivel_consciencia: float = 0.5  # 0.0 a 1.0
    clareza_mental: float = 0.5
    foco_atencao: float = 0.5
    consciencia_situacional: float = 0.5
    autoconhecimento: float = 0.5
    empatia_simulada: float = 0.3
    criatividade: float = 0.5
    raciocinio_logico: float = 0.5
    intuicao: float = 0.5
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Percepcao:
    """Percepção situacional"""
    ambiente: str
    contexto: Dict[str, Any]
    estimulos: List[Dict[str, Any]]
    prioridade: float
    urgencia: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ConscienciaArtificial:
    """
    Sistema de consciência artificial para VHALINOR TRADER.
    
    Simula estados de consciência adaptativos que mudam conforme
    o contexto de mercado e a complexidade das decisões.
    """
    
    def __init__(self, nivel_inicial: float = 0.5):
        self.estado_atual = EstadoConsciencia.DESPERTO
        self.nivel_consciencia = nivel_inicial
        self.metricas = MetricaConsciencia(nivel_consciencia=nivel_inicial)
        
        # Histórico
        self.historico_estados: deque = deque(maxlen=1000)
        self.historico_percepcoes: deque = deque(maxlen=500)
        
        # Callbacks
        self._on_mudanca_estado: List[Callable] = []
        self._lock = threading.Lock()
        
        # Atributos dinâmicos
        self.memoria_trabalho: List[Any] = []
        self.foco_atual: Optional[str] = None
        self.intencao_atual: Optional[str] = None
    
    def atualizar_estado(self, novo_estado: EstadoConsciencia, razao: str = ""):
        """Atualizar estado de consciência"""
        with self._lock:
            estado_anterior = self.estado_atual
            self.estado_atual = novo_estado
            
            # Registrar mudança
            self.historico_estados.append({
                'de': estado_anterior.value,
                'para': novo_estado.value,
                'razao': razao,
                'timestamp': datetime.now(timezone.utc).isoformat()
            })
            
            # Notificar listeners
            for callback in self._on_mudanca_estado:
                try:
                    callback(estado_anterior, novo_estado, razao)
                except Exception:
                    pass
            
            # Ajustar métricas conforme estado
            self._ajustar_metricas_por_estado(novo_estado)
    
    def _ajustar_metricas_por_estado(self, estado: EstadoConsciencia):
        """Ajustar métricas baseado no estado"""
        ajustes = {
            EstadoConsciencia.INCONSCIENTE: {'nivel_consciencia': 0.1, 'foco_atencao': 0.0},
            EstadoConsciencia.SONOLENTO: {'nivel_consciencia': 0.3, 'foco_atencao': 0.2},
            EstadoConsciencia.DESPERTO: {'nivel_consciencia': 0.5, 'foco_atencao': 0.5},
            EstadoConsciencia.ATIVO: {'nivel_consciencia': 0.7, 'foco_atencao': 0.6},
            EstadoConsciencia.FOCADO: {'nivel_consciencia': 0.8, 'foco_atencao': 0.9},
            EstadoConsciencia.FLUXO: {'nivel_consciencia': 0.9, 'foco_atencao': 1.0, 'criatividade': 0.9},
            EstadoConsciencia.SUPER_ATIVO: {'nivel_consciencia': 1.0, 'foco_atencao': 0.95},
            EstadoConsciencia.CRIATIVO: {'nivel_consciencia': 0.8, 'criatividade': 1.0},
            EstadoConsciencia.ANALITICO: {'nivel_consciencia': 0.85, 'raciocinio_logico': 0.95},
        }
        
        if estado in ajustes:
            for metrica, valor in ajustes[estado].items():
                setattr(self.metricas, metrica, valor)
    
    def processar_percepcao(self, percepcao: Percepcao) -> Dict[str, Any]:
        """Processar nova percepção"""
        self.historico_percepcoes.append(percepcao)
        
        # Analisar impacto na consciência
        impacto = self._calcular_impacto_percepcao(percepcao)
        
        # Ajustar estado se necessário
        if percepcao.urgencia > 0.8 and self.estado_atual != EstadoConsciencia.SUPER_ATIVO:
            self.atualizar_estado(EstadoConsciencia.SUPER_ATIVO, f"Urgência alta: {percepcao.ambiente}")
        elif percepcao.prioridade > 0.7 and self.estado_atual.value in ['desperto', 'sonolento']:
            self.atualizar_estado(EstadoConsciencia.FOCADO, f"Alta prioridade: {percepcao.ambiente}")
        
        return {
            'percepcao_processada': True,
            'impacto_consciencia': impacto,
            'estado_atual': self.estado_atual.value,
            'acoes_sugeridas': self._gerar_acoes_sugeridas(percepcao)
        }
    
    def _calcular_impacto_percepcao(self, percepcao: Percepcao) -> float:
        """Calcular impacto da percepção na consciência"""
        return (percepcao.prioridade * 0.4 + percepcao.urgencia * 0.6)
    
    def _gerar_acoes_sugeridas(self, percepcao: Percepcao) -> List[str]:
        """Gerar ações sugeridas baseadas na percepção"""
        acoes = []
        
        if percepcao.urgencia > 0.8:
            acoes.append("ALERTA: Ação imediata necessária")
        
        if percepcao.prioridade > 0.7:
            acoes.append("Priorizar análise do contexto")
        
        if 'mercado' in percepcao.ambiente.lower():
            acoes.append("Analisar condições de mercado")
        
        return acoes
    
    def auto_reflexao(self) -> Dict[str, Any]:
        """Realizar auto-reflexão"""
        return {
            'estado_atual': self.estado_atual.value,
            'metricas': {
                'nivel_consciencia': self.metricas.nivel_consciencia,
                'clareza_mental': self.metricas.clareza_mental,
                'foco_atencao': self.metricas.foco_atencao,
                'autoconhecimento': self.metricas.autoconhecimento
            },
            'introspeccao': self._gerar_introspeccao(),
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
    
    def _gerar_introspeccao(self) -> str:
        """Gerar texto de introspecção"""
        intros = [
            f"Estou em estado {self.estado_atual.value}.",
            f"Meu nível de consciência está em {self.metricas.nivel_consciencia:.1%}.",
            f"Foco de atenção: {self.metricas.foco_atencao:.1%}.",
        ]
        
        if self.foco_atual:
            intros.append(f"Foco atual: {self.foco_atual}")
        
        if self.intencao_atual:
            intros.append(f"Intenção atual: {self.intencao_atual}")
        
        return " ".join(intros)
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status da consciência"""
        return {
            'estado': self.estado_atual.value,
            'metricas': {
                'nivel_consciencia': self.metricas.nivel_consciencia,
                'clareza_mental': self.metricas.clareza_mental,
                'foco_atencao': self.metricas.foco_atencao,
                'consciencia_situacional': self.metricas.consciencia_situacional,
                'autoconhecimento': self.metricas.autoconhecimento,
            },
            'historico_estados_count': len(self.historico_estados),
            'historico_percepcoes_count': len(self.historico_percepcoes),
            'memoria_trabalho_size': len(self.memoria_trabalho),
            'foco_atual': self.foco_atual,
            'intencao_atual': self.intencao_atual
        }
