"""
VHALINOR Tomada de Decisão v6.0
==================================
Sistema de tomada de decisão com:
- Análise multi-critério
- Árvore de decisões
- Otimização de escolhas
- Decisão sob incerteza
- Decisão em grupo

@module tomada_decisao
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import defaultdict
import random


class TipoDecisao(Enum):
    """Tipos de decisão"""
    DETERMINISTICA = "deterministica"
    PROBABILISTICA = "probabilistica"
    MULTI_CRITERIO = "multi_criterio"
    SEQUENCIAL = "sequencial"
    GRUPO = "grupo"
    EMERGENCIAL = "emergencial"


class RiscoDecisao(Enum):
    """Níveis de risco de decisão"""
    MUITO_BAIXO = 0.1
    BAIXO = 0.3
    MEDIO = 0.5
    ALTO = 0.7
    MUITO_ALTO = 0.9


@dataclass
class Alternativa:
    """Alternativa de decisão"""
    id: str
    descricao: str
    atributos: Dict[str, Any]
    avaliacoes: Dict[str, float] = field(default_factory=dict)
    risco: float = 0.5
    custo: float = 0.0
    beneficio: float = 0.0
    
    @property
    def utilidade(self) -> float:
        """Calcular utilidade da alternativa"""
        if not self.avaliacoes:
            return 0.5
        return sum(self.avaliacoes.values()) / len(self.avaliacoes)


@dataclass
class Criterio:
    """Critério de avaliação"""
    nome: str
    peso: float
    tipo: str  # 'maximizar' ou 'minimizar'
    funcao_utilidade: Optional[Callable] = None


@dataclass
class ResultadoDecisao:
    """Resultado de processo decisório"""
    alternativa_selecionada: Optional[Alternativa]
    ranking: List[Tuple[Alternativa, float]]
    tipo_decisao: TipoDecisao
    confianca: float
    razao: str
    risco_total: float
    alternativas_consideradas: int
    tempo_decisao_ms: float
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class TomadaDecisao:
    """
    Sistema avançado de tomada de decisão.
    """
    
    def __init__(self):
        self.historico_decisoes: List[ResultadoDecisao] = []
        self.criterios_padrao: List[Criterio] = []
        self.matriz_decisao: Dict[str, Any] = {}
        self._inicializar_criterios()
    
    def _inicializar_criterios(self):
        """Inicializar critérios padrão"""
        self.criterios_padrao = [
            Criterio('rentabilidade', 0.3, 'maximizar'),
            Criterio('risco', 0.25, 'minimizar'),
            Criterio('liquidez', 0.2, 'maximizar'),
            Criterio('custo', 0.15, 'minimizar'),
            Criterio('tempo', 0.1, 'minimizar')
        ]
    
    def decisao_multi_criterio(
        self,
        alternativas: List[Alternativa],
        criterios: Optional[List[Criterio]] = None,
        metodo: str = 'saw'  # Simple Additive Weighting
    ) -> ResultadoDecisao:
        """Tomar decisão usando análise multi-critério"""
        inicio = datetime.now(timezone.utc)
        
        criterios = criterios or self.criterios_padrao
        
        # Normalizar avaliações
        for alt in alternativas:
            self._normalizar_avaliacoes(alt, criterios)
        
        # Calcular scores
        scores = []
        for alt in alternativas:
            score = self._calcular_score_mcdm(alt, criterios)
            scores.append((alt, score))
        
        # Ordenar por score
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # Selecionar melhor alternativa
        melhor = scores[0][0] if scores else None
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoDecisao(
            alternativa_selecionada=melhor,
            ranking=scores,
            tipo_decisao=TipoDecisao.MULTI_CRITERIO,
            confianca=scores[0][1] if scores else 0.0,
            razao=f"Melhor score usando {metodo}",
            risco_total=melhor.risco if melhor else 1.0,
            alternativas_consideradas=len(alternativas),
            tempo_decisao_ms=tempo
        )
    
    def _normalizar_avaliacoes(self, alternativa: Alternativa, criterios: List[Criterio]):
        """Normalizar avaliações da alternativa"""
        # Simplificação: normalização básica
        for criterio in criterios:
            if criterio.nome in alternativa.avaliacoes:
                valor = alternativa.avaliacoes[criterio.nome]
                # Normalizar para [0, 1]
                alternativa.avaliacoes[criterio.nome] = max(0.0, min(1.0, valor))
    
    def _calcular_score_mcdm(
        self,
        alternativa: Alternativa,
        criterios: List[Criterio]
    ) -> float:
        """Calcular score usando MCDM"""
        score = 0.0
        
        for criterio in criterios:
            if criterio.nome in alternativa.avaliacoes:
                valor = alternativa.avaliacoes[criterio.nome]
                
                # Aplicar peso
                if criterio.tipo == 'maximizar':
                    score += valor * criterio.peso
                else:  # minimizar
                    score += (1 - valor) * criterio.peso
        
        return score
    
    def arvore_decisao(
        self,
        contexto: Dict[str, Any],
        arvore: Dict[str, Any]
    ) -> ResultadoDecisao:
        """Navegar árvore de decisão"""
        inicio = datetime.now(timezone.utc)
        
        resultado = self._avaliar_arvore(contexto, arvore)
        
        alternativa = Alternativa(
            id=resultado['id'],
            descricao=resultado['descricao'],
            atributos=resultado.get('atributos', {}),
            risco=resultado.get('risco', 0.5)
        )
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoDecisao(
            alternativa_selecionada=alternativa,
            ranking=[(alternativa, 1.0)],
            tipo_decisao=TipoDecisao.DETERMINISTICA,
            confianca=resultado.get('confianca', 0.8),
            razao=resultado.get('caminho', 'Árvore de decisão'),
            risco_total=alternativa.risco,
            alternativas_consideradas=resultado.get('nos_avaliados', 1),
            tempo_decisao_ms=tempo
        )
    
    def _avaliar_arvore(self, contexto: Dict, no: Dict) -> Dict:
        """Avaliar nó da árvore de decisão"""
        # Verificar condição do nó atual
        if 'condicao' in no:
            condicao = no['condicao']
            atende = self._avaliar_condicao(contexto, condicao)
            
            if atende and 'sim' in no:
                resultado = self._avaliar_arvore(contexto, no['sim'])
                resultado['caminho'] = f"{no.get('id', 'node')} -> sim -> {resultado.get('caminho', '')}"
                return resultado
            elif not atende and 'nao' in no:
                resultado = self._avaliar_arvore(contexto, no['nao'])
                resultado['caminho'] = f"{no.get('id', 'node')} -> nao -> {resultado.get('caminho', '')}"
                return resultado
        
        # Nó folha
        return {
            'id': no.get('id', 'decision'),
            'descricao': no.get('acao', 'Decisão final'),
            'atributos': no.get('atributos', {}),
            'risco': no.get('risco', 0.5),
            'confianca': no.get('confianca', 0.8),
            'nos_avaliados': 1,
            'caminho': no.get('id', 'folha')
        }
    
    def _avaliar_condicao(self, contexto: Dict, condicao: Dict) -> bool:
        """Avaliar uma condição"""
        chave = condicao.get('chave')
        operador = condicao.get('operador', '==')
        valor_ref = condicao.get('valor')
        
        if chave not in contexto:
            return False
        
        valor_ctx = contexto[chave]
        
        if operador == '==':
            return valor_ctx == valor_ref
        elif operador == '>':
            return valor_ctx > valor_ref
        elif operador == '<':
            return valor_ctx < valor_ref
        elif operador == '>=':
            return valor_ctx >= valor_ref
        elif operador == '<=':
            return valor_ctx <= valor_ref
        elif operador == 'in':
            return valor_ctx in valor_ref
        
        return False
    
    def decisao_probabilistica(
        self,
        alternativas: List[Alternativa],
        probabilidades: Optional[Dict[str, float]] = None,
        utilidade_esperada: bool = True
    ) -> ResultadoDecisao:
        """Tomar decisão sob incerteza"""
        inicio = datetime.now(timezone.utc)
        
        # Se não houver probabilidades, assumir equiprobabilidade
        if probabilidades is None:
            prob = 1.0 / len(alternativas)
            probabilidades = {alt.id: prob for alt in alternativas}
        
        # Calcular utilidade esperada
        utilidades = []
        for alt in alternativas:
            prob = probabilidades.get(alt.id, 0.0)
            utilidade = alt.utilidade * prob if utilidade_esperada else alt.utilidade
            utilidades.append((alt, utilidade))
        
        # Ordenar por utilidade esperada
        utilidades.sort(key=lambda x: x[1], reverse=True)
        
        melhor = utilidades[0][0] if utilidades else None
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoDecisao(
            alternativa_selecionada=melhor,
            ranking=utilidades,
            tipo_decisao=TipoDecisao.PROBABILISTICA,
            confianca=probabilidades.get(melhor.id, 0.0) if melhor else 0.0,
            razao="Maximização da utilidade esperada",
            risco_total=melhor.risco if melhor else 1.0,
            alternativas_consideradas=len(alternativas),
            tempo_decisao_ms=tempo
        )
    
    def decisao_grupo(
        self,
        alternativas: List[Alternativa],
        votos: Dict[str, List[str]],  # {votante: [ordem de preferência]}
        metodo: str = 'borda'  # Borda count
    ) -> ResultadoDecisao:
        """Tomar decisão em grupo"""
        inicio = datetime.now(timezone.utc)
        
        if metodo == 'borda':
            scores = self._metodo_borda(alternativas, votos)
        elif metodo == 'pluralidade':
            scores = self._metodo_pluralidade(alternativas, votos)
        else:
            scores = [(alt, 0.0) for alt in alternativas]
        
        scores.sort(key=lambda x: x[1], reverse=True)
        melhor = scores[0][0] if scores else None
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoDecisao(
            alternativa_selecionada=melhor,
            ranking=scores,
            tipo_decisao=TipoDecisao.GRUPO,
            confianca=scores[0][1] / sum(s[1] for s in scores) if scores and sum(s[1] for s in scores) > 0 else 0.0,
            razao=f"Decisão em grupo usando método {metodo}",
            risco_total=melhor.risco if melhor else 1.0,
            alternativas_consideradas=len(alternativas),
            tempo_decisao_ms=tempo
        )
    
    def _metodo_borda(
        self,
        alternativas: List[Alternativa],
        votos: Dict[str, List[str]]
    ) -> List[Tuple[Alternativa, float]]:
        """Contagem de Borda"""
        scores = {alt.id: 0 for alt in alternativas}
        n = len(alternativas)
        
        for votante, preferencias in votos.items():
            for posicao, alt_id in enumerate(preferencias):
                if alt_id in scores:
                    scores[alt_id] += (n - posicao - 1)
        
        return [(alt, scores[alt.id]) for alt in alternativas]
    
    def _metodo_pluralidade(
        self,
        alternativas: List[Alternativa],
        votos: Dict[str, List[str]]
    ) -> List[Tuple[Alternativa, float]]:
        """Método da pluralidade (primeira escolha)"""
        contagem = {alt.id: 0 for alt in alternativas}
        
        for votante, preferencias in votos.items():
            if preferencias:
                contagem[preferencias[0]] += 1
        
        return [(alt, contagem[alt.id]) for alt in alternativas]
    
    def avaliar_risco(
        self,
        alternativa: Alternativa,
        cenarios: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Avaliar risco de alternativa"""
        riscos = []
        retornos = []
        
        for cenario in cenarios:
            probabilidade = cenario.get('probabilidade', 0.5)
            retorno = cenario.get('retorno', 0.0)
            
            riscos.append(probabilidade)
            retornos.append(retorno)
        
        # Calcular métricas
        if retornos:
            retorno_esperado = sum(r * p for r, p in zip(retornos, riscos)) / sum(riscos)
            variancia = sum(p * (r - retorno_esperado)**2 for r, p in zip(retornos, riscos)) / sum(riscos)
        else:
            retorno_esperado = 0.0
            variancia = 0.0
        
        return {
            'retorno_esperado': retorno_esperado,
            'variancia': variancia,
            'desvio_padrao': variancia ** 0.5,
            'risco_total': alternativa.risco,
            'sharpe_ratio': retorno_esperado / (variancia ** 0.5) if variancia > 0 else 0.0
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de decisão"""
        return {
            'total_decisoes': len(self.historico_decisoes),
            'criterios_configurados': len(self.criterios_padrao),
            'tipos_decisao_suportados': [t.value for t in TipoDecisao],
            'ultimas_decisoes': len(self.historico_decisoes[-5:])
        }
