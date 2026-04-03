"""
VHALINOR Raciocínio Avançado v6.0
=====================================
Sistema de raciocínio avançado com múltiplos tipos de raciocínio:
- Dedução, indução, abdução
- Analogia e metáfora
- Causalidade e correlação
- Pensamento crítico e criativo

@module raciocinio_avancado
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque
import re


class TipoRaciocinio(Enum):
    """Tipos de raciocínio"""
    DEDUCAO = "deducao"           # Do geral ao específico
    INDUCAO = "inducao"           # Do específico ao geral
    ABDUCAO = "abducao"           # Melhor explicação
    ANALOGIA = "analogia"         # Comparação estrutural
    CAUSAL = "causal"             # Causa e efeito
    CORRELACIONAL = "correlacional"  # Padrões estatísticos
    CRITICO = "critico"           # Avaliação rigorosa
    CRIATIVO = "criativo"         # Geração de novas ideias
    SISTEMICO = "sistemico"       # Pensamento sistêmico
    DIVERGENTE = "divergente"     # Múltiplas soluções
    CONVERGENTE = "convergente"   # Melhor solução


@dataclass
class Premissa:
    """Premissa para raciocínio"""
    id: str
    declaracao: str
    tipo: str  # 'fato', 'hipotese', 'axioma', 'evidencia'
    confianca: float = 1.0
    fonte: Optional[str] = None
    dependencias: List[str] = field(default_factory=list)


@dataclass
class Conclusao:
    """Conclusão de raciocínio"""
    id: str
    declaracao: str
    tipo_raciocinio: TipoRaciocinio
    premissas: List[str]
    confianca: float
    evidencia_suporte: List[str] = field(default_factory=list)
    contra_argumentos: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class Argumento:
    """Estrutura de argumento"""
    tese: str
    premissas: List[Premissa]
    conclusao: Conclusao
    falacias: List[str] = field(default_factory=list)
    forca: float = 0.0  # 0.0 a 1.0


class RaciocinioAvancado:
    """
    Motor de raciocínio avançado com múltiplas estratégias.
    """
    
    def __init__(self):
        self.base_conhecimento: Dict[str, Premissa] = {}
        self.conclusoes_geradas: deque = deque(maxlen=1000)
        self.regras_deducao: List[Dict] = []
        self.padroes_inducao: Dict[str, Any] = {}
        self._inicializar_regras()
    
    def _inicializar_regras(self):
        """Inicializar regras de raciocínio"""
        # Regras de dedução para trading
        self.regras_deducao = [
            {
                'nome': 'Tendência de Alta',
                'premissas': ['preco_acima_mm50', 'volume_aumentando', 'rsi_entre_50_70'],
                'conclusao': 'provavel_continuacao_alta',
                'confianca': 0.75
            },
            {
                'nome': 'Sinal de Compra',
                'premissas': ['cruzamento_alta_dourado', 'volume_confirmando', 'sem_resistencia_proxima'],
                'conclusao': 'sinal_compra_forte',
                'confianca': 0.80
            },
            {
                'nome': 'Reversão de Baixa',
                'premissas': ['divergencia_bullish_rsi', 'candle_hammer', 'suporte_historico'],
                'conclusao': 'possivel_reversao_alta',
                'confianca': 0.70
            }
        ]
    
    def deduzir(self, premissas_disponiveis: List[str]) -> List[Conclusao]:
        """Realizar dedução lógica"""
        conclusoes = []
        
        for regra in self.regras_deducao:
            # Verificar se todas as premissas da regra estão disponíveis
            if all(p in premissas_disponiveis for p in regra['premissas']):
                conclusao = Conclusao(
                    id=f"ded_{len(self.conclusoes_geradas)}",
                    declaracao=regra['conclusao'],
                    tipo_raciocinio=TipoRaciocinio.DEDUCAO,
                    premissas=regra['premissas'],
                    confianca=regra['confianca']
                )
                conclusoes.append(conclusao)
                self.conclusoes_geradas.append(conclusao)
        
        return conclusoes
    
    def induzir(self, observacoes: List[Dict[str, Any]]) -> Conclusao:
        """Realizar indução a partir de observações"""
        # Analisar padrões nas observações
        padroes = self._extrair_padroes(observacoes)
        
        # Generalizar padrões
        generalizacao = self._generalizar_padroes(padroes)
        
        conclusao = Conclusao(
            id=f"ind_{len(self.conclusoes_geradas)}",
            declaracao=generalizacao,
            tipo_raciocinio=TipoRaciocinio.INDUCAO,
            premissas=[str(i) for i in range(len(observacoes))],
            confianca=self._calcular_confianca_inducao(padroes)
        )
        
        self.conclusoes_geradas.append(conclusao)
        return conclusao
    
    def abduzir(self, observacao: str, hipoteses: List[str]) -> Conclusao:
        """Realizar abdução - escolher melhor explicação"""
        melhor_hipotese = None
        melhor_pontuacao = 0.0
        
        for hipotese in hipoteses:
            pontuacao = self._avaliar_explicacao(hipotese, observacao)
            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_hipotese = hipotese
        
        conclusao = Conclusao(
            id=f"abd_{len(self.conclusoes_geradas)}",
            declaracao=f"Melhor explicação: {melhor_hipotese}",
            tipo_raciocinio=TipoRaciocinio.ABDUCAO,
            premissas=[observacao],
            confianca=melhor_pontuacao
        )
        
        self.conclusoes_geradas.append(conclusao)
        return conclusao
    
    def raciocinar_por_analogia(
        self,
        caso_conhecido: Dict[str, Any],
        caso_novo: Dict[str, Any]
    ) -> Conclusao:
        """Raciocínio por analogia"""
        # Mapear similaridades
        similaridades = self._mapear_similaridades(caso_conhecido, caso_novo)
        
        # Transferir conclusões do caso conhecido
        grau_analogia = sum(similaridades.values()) / len(similaridades) if similaridades else 0
        
        conclusao = Conclusao(
            id=f"ana_{len(self.conclusoes_geradas)}",
            declaracao=f"Baseado na analogia com caso similar: resultado esperado similar",
            tipo_raciocinio=TipoRaciocinio.ANALOGIA,
            premissas=[str(caso_conhecido), str(caso_novo)],
            confianca=grau_analogia
        )
        
        self.conclusoes_geradas.append(conclusao)
        return conclusao
    
    def pensamento_critico(self, argumento: Argumento) -> Dict[str, Any]:
        """Aplicar pensamento crítico a um argumento"""
        analise = {
            'validade_logica': self._verificar_validade(argumento),
            'forca_evidencia': self._avaliar_evidencia(argumento),
            'vieses_detectados': self._detectar_vieses(argumento),
            'falacias_identificadas': self._identificar_falacias(argumento),
            'qualidade_geral': 0.0,
            'recomendacoes': []
        }
        
        # Calcular qualidade geral
        analise['qualidade_geral'] = (
            analise['validade_logica'] * 0.3 +
            analise['forca_evidencia'] * 0.4 +
            (1.0 - len(analise['falacias_identificadas']) * 0.1) * 0.3
        )
        
        # Gerar recomendações
        if analise['vieses_detectados']:
            analise['recomendacoes'].append("Considerar viéses detectados na análise")
        
        if analise['falacias_identificadas']:
            analise['recomendacoes'].append("Revisar argumentos com falácias lógicas")
        
        return analise
    
    def _extrair_padroes(self, observacoes: List[Dict]) -> Dict[str, Any]:
        """Extrair padrões de observações"""
        # Simplificação: contar frequências
        frequencias = {}
        for obs in observacoes:
            for chave, valor in obs.items():
                if chave not in frequencias:
                    frequencias[chave] = {}
                if valor not in frequencias[chave]:
                    frequencias[chave][valor] = 0
                frequencias[chave][valor] += 1
        
        return frequencias
    
    def _generalizar_padroes(self, padroes: Dict) -> str:
        """Generalizar padrões encontrados"""
        # Simplificação: encontrar valores mais frequentes
        generalizacoes = []
        for chave, valores in padroes.items():
            mais_frequente = max(valores.items(), key=lambda x: x[1])
            generalizacoes.append(f"{chave}: tendência para {mais_frequente[0]}")
        
        return "; ".join(generalizacoes)
    
    def _calcular_confianca_inducao(self, padroes: Dict) -> float:
        """Calcular confiança de uma indução"""
        # Baseado na consistência dos padrões
        if not padroes:
            return 0.0
        
        consistencia = sum(
            max(valores.values()) / sum(valores.values())
            for valores in padroes.values()
        ) / len(padroes)
        
        return consistencia
    
    def _avaliar_explicacao(self, hipotese: str, observacao: str) -> float:
        """Avaliar qualidade de uma explicação"""
        # Simplificação: simular pontuação
        return 0.7  # Placeholder
    
    def _mapear_similaridades(self, caso1: Dict, caso2: Dict) -> Dict[str, float]:
        """Mapear similaridades entre casos"""
        similaridades = {}
        for chave in set(caso1.keys()) & set(caso2.keys()):
            if caso1[chave] == caso2[chave]:
                similaridades[chave] = 1.0
            elif isinstance(caso1[chave], (int, float)) and isinstance(caso2[chave], (int, float)):
                # Similaridade numérica normalizada
                max_val = max(abs(caso1[chave]), abs(caso2[chave]))
                if max_val > 0:
                    similaridades[chave] = 1.0 - abs(caso1[chave] - caso2[chave]) / max_val
                else:
                    similaridades[chave] = 1.0
            else:
                similaridades[chave] = 0.5
        
        return similaridades
    
    def _verificar_validade(self, argumento: Argumento) -> float:
        """Verificar validade lógica"""
        # Simplificação
        return 0.8
    
    def _avaliar_evidencia(self, argumento: Argumento) -> float:
        """Avaliar força da evidência"""
        if not argumento.premissas:
            return 0.0
        
        confiancas = [p.confianca for p in argumento.premissas]
        return sum(confiancas) / len(confiancas)
    
    def _detectar_vieses(self, argumento: Argumento) -> List[str]:
        """Detectar vieses no argumento"""
        vieses = []
        
        # Verificar vieses comuns
        texto = argumento.tese.lower()
        
        if 'sempre' in texto or 'nunca' in texto:
            vieses.append('generalizacao_extrema')
        
        if 'eu acho' in texto or 'parece-me' in texto:
            vieses.append('subjetividade')
        
        return vieses
    
    def _identificar_falacias(self, argumento: Argumento) -> List[str]:
        """Identificar falácias lógicas"""
        falacias = []
        
        texto = argumento.tese.lower()
        
        # Ad hominem
        if any(p in texto for p in ['idiota', 'estúpido', 'ignorante']):
            falacias.append('ad_hominem')
        
        # Falsa dicotomia
        if 'ou' in texto and ('tudo' in texto or 'nada' in texto):
            falacias.append('falsa_dicotomia')
        
        # Apelo à autoridade
        if any(p in texto for p in ['especialista diz', 'estudos mostram']):
            falacias.append('apelo_autoridade_vago')
        
        return falacias
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de raciocínio"""
        return {
            'base_conhecimento_size': len(self.base_conhecimento),
            'conclusoes_geradas': len(self.conclusoes_geradas),
            'regras_deducao': len(self.regras_deducao),
            'padroes_inducao': len(self.padroes_inducao),
            'tipos_raciocinio_suportados': [t.value for t in TipoRaciocinio]
        }
