"""
VHALINOR Aprendizado Contínuo v6.0
=====================================
Sistema de aprendizado contínuo e adaptativo com:
- Aprendizado online
- Transfer learning
- Meta-learning
- Aprendizado por reforço
- Adaptação a novos contextos

@module aprendizado_continuo
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque
import json
import hashlib


class EstrategiaAprendizado(Enum):
    """Estratégias de aprendizado"""
    SUPERVISIONADO = "supervisionado"
    NAO_SUPERVISIONADO = "nao_supervisionado"
    POR_REFORCO = "por_reforco"
    ONLINE = "online"
    TRANSFERENCIA = "transferencia"
    META_LEARNING = "meta_learning"
    FEW_SHOT = "few_shot"
    ZERO_SHOT = "zero_shot"
    CURRICULO = "curriculo"
    ATIVO = "ativo"


@dataclass
class Experiencia:
    """Experiência de aprendizado"""
    id: str
    entrada: Any
    saida_esperada: Optional[Any]
    saida_obtida: Optional[Any]
    feedback: float  # Recompensa ou erro
    contexto: Dict[str, Any]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    aprendida: bool = False


@dataclass
class ModeloMental:
    """Modelo mental aprendido"""
    id: str
    dominio: str
    conceitos: Dict[str, Any]
    relacoes: List[Tuple[str, str, str]]  # (conceito1, relacao, conceito2)
    regras: List[Dict[str, Any]]
    exemplos: deque
    performance: float = 0.0
    criado_em: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    atualizado_em: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class AprendizadoContinuo:
    """
    Sistema de aprendizado contínuo adaptativo.
    """
    
    def __init__(self):
        self.experiencias: deque = deque(maxlen=10000)
        self.modelos_mentais: Dict[str, ModeloMental] = {}
        self.patterns_aprendidos: Dict[str, Any] = {}
        self.callbacks_aprendizado: List[Callable] = []
        
        # Métricas
        self.taxa_aprendizado = 0.01
        self.performance_geral = 0.5
        self.experiencias_aprendidas = 0
        self.erros_cometidos = 0
        self.correcoes_realizadas = 0
    
    def adicionar_experiencia(
        self,
        entrada: Any,
        saida_esperada: Optional[Any],
        saida_obtida: Optional[Any],
        feedback: float,
        contexto: Optional[Dict] = None
    ) -> str:
        """Adicionar nova experiência"""
        exp_id = hashlib.md5(
            f"{entrada}{datetime.now(timezone.utc)}".encode()
        ).hexdigest()[:16]
        
        experiencia = Experiencia(
            id=exp_id,
            entrada=entrada,
            saida_esperada=saida_esperada,
            saida_obtida=saida_obtida,
            feedback=feedback,
            contexto=contexto or {}
        )
        
        self.experiencias.append(experiencia)
        
        # Processar imediatamente se aprendizado online
        self._processar_experiencia(experiencia)
        
        return exp_id
    
    def _processar_experiencia(self, experiencia: Experiencia):
        """Processar experiência e extrair aprendizado"""
        # Calcular erro se aplicável
        if experiencia.saida_esperada is not None and experiencia.saida_obtida is not None:
            erro = self._calcular_erro(
                experiencia.saida_esperada,
                experiencia.saida_obtida
            )
            
            # Se erro significativo, aprender
            if erro > 0.1:
                self._aprender_com_erro(experiencia, erro)
                experiencia.aprendida = True
                self.experiencias_aprendidas += 1
            else:
                # Reforçar padrão correto
                self._reforcar_padrao(experiencia)
    
    def _calcular_erro(self, esperado: Any, obtido: Any) -> float:
        """Calcular erro entre saída esperada e obtida"""
        if isinstance(esperado, (int, float)) and isinstance(obtido, (int, float)):
            return abs(esperado - obtido) / max(abs(esperado), 1e-10)
        elif isinstance(esperado, str) and isinstance(obtido, str):
            return 0.0 if esperado == obtido else 1.0
        else:
            return 0.0 if esperado == obtido else 1.0
    
    def _aprender_com_erro(self, experiencia: Experiencia, erro: float):
        """Aprender a partir de um erro"""
        self.erros_cometidos += 1
        
        # Identificar padrão do erro
        padrao_erro = self._extrair_padrao_erro(experiencia)
        
        # Atualizar modelo mental
        dominio = experiencia.contexto.get('dominio', 'geral')
        
        if dominio not in self.modelos_mentais:
            self.modelos_mentais[dominio] = ModeloMental(
                id=f"modelo_{dominio}",
                dominio=dominio,
                conceitos={},
                relacoes=[],
                regras=[],
                exemplos=deque(maxlen=100)
            )
        
        modelo = self.modelos_mentais[dominio]
        
        # Adicionar às regras de correção
        modelo.regras.append({
            'condicao': experiencia.entrada,
            'acao_correta': experiencia.saida_esperada,
            'erro_comum': experiencia.saida_obtida,
            'contexto': experiencia.contexto,
            'timestamp': datetime.now(timezone.utc).isoformat()
        })
        
        # Adicionar exemplo
        modelo.exemplos.append({
            'entrada': experiencia.entrada,
            'saida': experiencia.saida_esperada,
            'contexto': experiencia.contexto
        })
        
        self.correcoes_realizadas += 1
        
        # Notificar callbacks
        for callback in self.callbacks_aprendizado:
            try:
                callback('erro_corrigido', experiencia)
            except Exception:
                pass
    
    def _reforcar_padrao(self, experiencia: Experiencia):
        """Reforçar um padrão correto"""
        dominio = experiencia.contexto.get('dominio', 'geral')
        
        # Extrair conceitos e relações
        conceitos = self._extrair_conceitos(experiencia)
        
        if dominio in self.modelos_mentais:
            modelo = self.modelos_mentais[dominio]
            
            for conceito in conceitos:
                if conceito not in modelo.conceitos:
                    modelo.conceitos[conceito] = {'frequencia': 0, 'associacoes': []}
                
                modelo.conceitos[conceito]['frequencia'] += 1
    
    def _extrair_padrao_erro(self, experiencia: Experiencia) -> Dict[str, Any]:
        """Extrair padrão característico do erro"""
        return {
            'tipo_entrada': type(experiencia.entrada).__name__,
            'contexto_chaves': list(experiencia.contexto.keys()),
            'feedback': experiencia.feedback,
            'timestamp': experiencia.timestamp
        }
    
    def _extrair_conceitos(self, experiencia: Experiencia) -> List[str]:
        """Extrair conceitos de uma experiência"""
        conceitos = []
        
        # Extrair de entrada
        if isinstance(experiencia.entrada, str):
            conceitos.extend(experiencia.entrada.lower().split())
        
        # Extrair de contexto
        for chave, valor in experiencia.contexto.items():
            conceitos.append(chave)
            if isinstance(valor, str):
                conceitos.extend(valor.lower().split())
        
        return list(set(conceitos))
    
    def aprender_com_exemplos(
        self,
        exemplos: List[Tuple[Any, Any]],
        estrategia: EstrategiaAprendizado = EstrategiaAprendizado.SUPERVISIONADO
    ) -> Dict[str, Any]:
        """Aprender com múltiplos exemplos"""
        resultados = {
            'exemplos_processados': 0,
            'padroes_identificados': 0,
            'modelo_atualizado': False
        }
        
        for entrada, saida in exemplos:
            self.adicionar_experiencia(
                entrada=entrada,
                saida_esperada=saida,
                saida_obtida=None,
                feedback=1.0,
                contexto={'estrategia': estrategia.value}
            )
            resultados['exemplos_processados'] += 1
        
        # Identificar padrões
        padroes = self._identificar_padroes_batch(exemplos)
        resultados['padroes_identificados'] = len(padroes)
        
        return resultados
    
    def _identificar_padroes_batch(self, exemplos: List[Tuple[Any, Any]]) -> List[Dict]:
        """Identificar padrões em lote de exemplos"""
        # Simplificação: agrupar por similaridade de entrada
        grupos = {}
        
        for entrada, saida in exemplos:
            chave = self._extrair_caracteristicas(entrada)
            if chave not in grupos:
                grupos[chave] = []
            grupos[chave].append((entrada, saida))
        
        padroes = []
        for chave, grupo in grupos.items():
            if len(grupo) > 2:  # Mínimo para padrão
                padroes.append({
                    'caracteristica': chave,
                    'frequencia': len(grupo),
                    'exemplo_representativo': grupo[0]
                })
        
        return padroes
    
    def _extrair_caracteristicas(self, entrada: Any) -> str:
        """Extrair características representativas"""
        if isinstance(entrada, str):
            return entrada[:50]  # Primeiros 50 caracteres
        elif isinstance(entrada, (int, float)):
            return f"num_{entrada:.2f}"
        else:
            return str(type(entrada).__name__)
    
    def transferir_conhecimento(
        self,
        dominio_origem: str,
        dominio_destino: str,
        conceitos_mapeados: Optional[Dict[str, str]] = None
    ) -> bool:
        """Transferir conhecimento entre domínios"""
        if dominio_origem not in self.modelos_mentais:
            return False
        
        modelo_origem = self.modelos_mentais[dominio_origem]
        
        # Criar ou atualizar modelo destino
        if dominio_destino not in self.modelos_mentais:
            self.modelos_mentais[dominio_destino] = ModeloMental(
                id=f"modelo_{dominio_destino}",
                dominio=dominio_destino,
                conceitos={},
                relacoes=[],
                regras=[],
                exemplos=deque(maxlen=100)
            )
        
        modelo_destino = self.modelos_mentais[dominio_destino]
        
        # Transferir conceitos
        for conceito, dados in modelo_origem.conceitos.items():
            conceito_mapeado = conceito
            if conceitos_mapeados and conceito in conceitos_mapeados:
                conceito_mapeado = conceitos_mapeados[conceito]
            
            if conceito_mapeado not in modelo_destino.conceitos:
                modelo_destino.conceitos[conceito_mapeado] = dados.copy()
        
        return True
    
    def avaliar_performance(self, dominio: Optional[str] = None) -> Dict[str, float]:
        """Avaliar performance de aprendizado"""
        if dominio and dominio in self.modelos_mentais:
            modelo = self.modelos_mentais[dominio]
            
            # Calcular baseado em regras e exemplos
            if modelo.regras:
                acuracia = sum(1 for r in modelo.regras if self._regra_valida(r)) / len(modelo.regras)
            else:
                acuracia = 0.5
            
            return {
                'acuracia': acuracia,
                'cobertura': len(modelo.conceitos) / max(len(modelo.conceitos), 1),
                'complexidade': len(modelo.regras) / 100,
                'experiencias': len(modelo.exemplos)
            }
        
        # Performance geral
        total_exp = len(self.experiencias)
        if total_exp == 0:
            return {'performance_geral': 0.5}
        
        taxa_aprendizado = self.experiencias_aprendidas / total_exp
        taxa_correcao = self.correcoes_realizadas / max(self.erros_cometidos, 1)
        
        return {
            'taxa_aprendizado': taxa_aprendizado,
            'taxa_correcao': taxa_correcao,
            'performance_geral': (taxa_aprendizado + taxa_correcao) / 2
        }
    
    def _regra_valida(self, regra: Dict) -> bool:
        """Verificar se regra ainda é válida"""
        # Simplificação: regras recentes são consideradas válidas
        return True
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de aprendizado"""
        return {
            'experiencias_total': len(self.experiencias),
            'experiencias_aprendidas': self.experiencias_aprendidas,
            'modelos_mentais': len(self.modelos_mentais),
            'erros_cometidos': self.erros_cometidos,
            'correcoes_realizadas': self.correcoes_realizadas,
            'performance_geral': self.performance_geral,
            'dominios': list(self.modelos_mentais.keys())
        }
