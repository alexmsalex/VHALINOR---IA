"""
VHALINOR Evolução de Aprendizado v6.0
=======================================
Sistema de evolução de aprendizado com:
- Evolução de modelos ao longo do tempo
- Tracking de performance histórica
- Adaptação de estratégias
- Seleção natural de algoritmos
- Memória de longo prazo de aprendizado
- Transferência de conhecimento entre gerações
- Métricas de evolução
- Linhagem de modelos
- Adaptação a mudanças de regime de mercado

@module evolucao_aprendizado
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from collections import deque
import hashlib
import json


class TipoEvolucao(Enum):
    """Tipos de evolução de aprendizado"""
    MUTACAO = "mutacao"           # Pequenas alterações no modelo
    CROSSOVER = "crossover"       # Combinação de modelos
    SELECAO = "selecao"           # Seleção natural
    EPIFANIA = "epifania"         # Grande insight/mudança
    CONSOLIDACAO = "consolidacao" # Refinamento gradual
    ADAPTACAO = "adaptacao"       # Adaptação a mudanças


class EstagioEvolucao(Enum):
    """Estágios de evolução"""
    GERMINACAO = "germinacao"     # Início, aprendizado básico
    CRESCIMENTO = "crescimento"   # Desenvolvimento rápido
    MATURIDADE = "maturidade"     # Performance estável
    ESPECIALIZACAO = "especializacao"  # Foco em nicho
    FLORACAO = "floracao"         # Pico de performance
    ADAPTACAO = "adaptacao"       # Mudança de estratégia


class TipoAdaptacao(Enum):
    """Tipos de adaptação a mudanças"""
    REGIME_VOLATILIDADE = "regime_volatilidade"
    REGIME_TENDENCIA = "regime_tendencia"
    REGIME_RANGE = "regime_range"
    MUDANCA_MACRO = "mudanca_macro"
    EVENTO_EXTERNO = "evento_externo"


@dataclass
class GenomaModelo:
    """Genoma representando características de um modelo"""
    id: str
    geracao: int
    caracteristicas: Dict[str, float]  # Pesos, thresholds, etc.
    arquitetura: str
    hiperparametros: Dict[str, Any]
    ancestral_id: Optional[str] = None
    mutacoes: List[str] = field(default_factory=list)
    timestamp_criacao: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class FitnessSnapshot:
    """Snapshot de fitness de um modelo"""
    timestamp: str
    fitness_score: float
    sharpe_ratio: float
    win_rate: float
    profit_factor: float
    max_drawdown: float
    trades_realizados: int
    ambiente: str  # "bull", "bear", "sideways", "volatile"


@dataclass
class EventoEvolucao:
    """Evento de evolução registrado"""
    id: str
    tipo: TipoEvolucao
    geracao: int
    descricao: str
    modelo_origem: str
    modelo_destino: Optional[str]
    impacto_fitness: float
    motivacao: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


@dataclass
class LinhagemModelo:
    """Linhagem de um modelo através das gerações"""
    modelo_id: str
    geracao: int
    ancestral_direto: Optional[str]
    descendentes: List[str] = field(default_factory=list)
    irmaos: List[str] = field(default_factory=list)
    caminho_evolucao: List[str] = field(default_factory=list)  # IDs de eventos


class EvolucaoAprendizado:
    """
    Sistema de evolução de aprendizado para VHALINOR.
    
    Implementa conceitos de evolução natural para melhorar
    continuamente os modelos de trading através de gerações.
    """
    
    def __init__(self, populacao_maxima: int = 20):
        self.populacao_maxima = populacao_maxima
        self.geracao_atual = 0
        
        # População de modelos
        self.genomas: Dict[str, GenomaModelo] = {}
        self.fitness_historico: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        self.linhagens: Dict[str, LinhagemModelo] = {}
        
        # Histórico de evolução
        self.eventos_evolucao: deque = deque(maxlen=1000)
        self.adaptacoes_realizadas: deque = deque(maxlen=100)
        
        # Regimes de mercado detectados
        self.regime_atual: str = "desconhecido"
        self.historico_regimes: deque = deque(maxlen=50)
        
        # Melhores performers por regime
        self.campeoes_por_regime: Dict[str, str] = {}
        
        # Taxas de evolução
        self.taxa_mutacao = 0.1
        self.taxa_crossover = 0.3
        self.pressao_selecao = 0.5
    
    def criar_genoma_inicial(
        self,
        caracteristicas: Dict[str, float],
        arquitetura: str,
        hiperparametros: Dict[str, Any]
    ) -> str:
        """Criar genoma da primeira geração"""
        genoma_id = hashlib.md5(f"gen0_{datetime.now(timezone.utc)}".encode()).hexdigest()[:16]
        
        genoma = GenomaModelo(
            id=genoma_id,
            geracao=0,
            caracteristicas=caracteristicas,
            arquitetura=arquitetura,
            hiperparametros=hiperparametros
        )
        
        self.genomas[genoma_id] = genoma
        self.linhagens[genoma_id] = LinhagemModelo(
            modelo_id=genoma_id,
            geracao=0,
            ancestral_direto=None
        )
        
        return genoma_id
    
    def registrar_fitness(self, genoma_id: str, snapshot: FitnessSnapshot):
        """Registrar snapshot de fitness"""
        if genoma_id not in self.fitness_historico:
            self.fitness_historico[genoma_id] = deque(maxlen=100)
        
        self.fitness_historico[genoma_id].append(snapshot)
        
        # Verificar se é campeão do regime
        if snapshot.ambiente not in self.campeoes_por_regime:
            self.campeoes_por_regime[snapshot.ambiente] = genoma_id
        else:
            campeao_atual = self.campeoes_por_regime[snapshot.ambiente]
            fitness_campeao = self._get_ultimo_fitness(campeao_atual)
            
            if snapshot.fitness_score > fitness_campeao * 1.05:  # 5% melhor
                self.campeoes_por_regime[snapshot.ambiente] = genoma_id
    
    def _get_ultimo_fitness(self, genoma_id: str) -> float:
        """Obter último fitness registrado"""
        if genoma_id in self.fitness_historico and self.fitness_historico[genoma_id]:
            return self.fitness_historico[genoma_id][-1].fitness_score
        return 0.0
    
    def calcular_fitness_medio(self, genoma_id: str, janela: int = 10) -> float:
        """Calcular fitness médio de um genoma"""
        if genoma_id not in self.fitness_historico:
            return 0.0
        
        snapshots = list(self.fitness_historico[genoma_id])[-janela:]
        if not snapshots:
            return 0.0
        
        return np.mean([s.fitness_score for s in snapshots])
    
    def selecionar_pais(self, n_pais: int = 2) -> List[str]:
        """Selecionar pais para reprodução usando seleção por torneio"""
        if len(self.genomas) < n_pais:
            return list(self.genomas.keys())
        
        # Seleção por torneio
        selecionados = []
        genoma_ids = list(self.genomas.keys())
        
        for _ in range(n_pais):
            # Selecionar 3 aleatórios
            torneio = np.random.choice(genoma_ids, min(3, len(genoma_ids)), replace=False)
            
            # Melhor fitness vence
            melhor = max(torneio, key=lambda g: self.calcular_fitness_medio(g))
            selecionados.append(melhor)
        
        return selecionados
    
    def crossover(
        self,
        pai1_id: str,
        pai2_id: str,
        caracteristicas_dominantes: Optional[List[str]] = None
    ) -> str:
        """Realizar crossover entre dois genomas"""
        if pai1_id not in self.genomas or pai2_id not in self.genomas:
            raise ValueError("Genomas pais não encontrados")
        
        pai1 = self.genomas[pai1_id]
        pai2 = self.genomas[pai2_id]
        
        # Nova geração
        self.geracao_atual = max(pai1.geracao, pai2.geracao) + 1
        
        # Criar novo ID
        filho_id = hashlib.md5(
            f"gen{self.geracao_atual}_{pai1_id}_{pai2_id}_{datetime.now(timezone.utc)}".encode()
        ).hexdigest()[:16]
        
        # Crossover de características
        caracteristicas_filho = {}
        todas_chaves = set(pai1.caracteristicas.keys()) | set(pai2.caracteristicas.keys())
        
        for chave in todas_chaves:
            if chave in pai1.caracteristicas and chave in pai2.caracteristicas:
                # Média ponderada pelo fitness
                fitness1 = self.calcular_fitness_medio(pai1_id)
                fitness2 = self.calcular_fitness_medio(pai2_id)
                peso_total = fitness1 + fitness2
                
                if peso_total > 0:
                    caracteristicas_filho[chave] = (
                        pai1.caracteristicas[chave] * fitness1 +
                        pai2.caracteristicas[chave] * fitness2
                    ) / peso_total
                else:
                    caracteristicas_filho[chave] = (pai1.caracteristicas[chave] + pai2.caracteristicas[chave]) / 2
            elif chave in pai1.caracteristicas:
                caracteristicas_filho[chave] = pai1.caracteristicas[chave]
            else:
                caracteristicas_filho[chave] = pai2.caracteristicas[chave]
        
        # Hiperparâmetros do pai com melhor fitness
        fitness1 = self.calcular_fitness_medio(pai1_id)
        fitness2 = self.calcular_fitness_medio(pai2_id)
        hiperparametros_filho = pai1.hiperparametros if fitness1 > fitness2 else pai2.hiperparametros
        
        # Criar genoma filho
        filho = GenomaModelo(
            id=filho_id,
            geracao=self.geracao_atual,
            caracteristicas=caracteristicas_filho,
            arquitetura=pai1.arquitetura,  # Herda arquitetura do pai1
            hiperparametros=hiperparametros_filho.copy(),
            ancestral_id=pai1_id  # Pai1 é o ancestral direto
        )
        
        self.genomas[filho_id] = filho
        
        # Atualizar linhagens
        self.linhagens[filho_id] = LinhagemModelo(
            modelo_id=filho_id,
            geracao=self.geracao_atual,
            ancestral_direto=pai1_id,
            irmaos=[pai2_id]
        )
        
        # Atualizar descendência do pai1
        if pai1_id in self.linhagens:
            self.linhagens[pai1_id].descendentes.append(filho_id)
        
        # Registrar evento
        evento = EventoEvolucao(
            id=f"evo_{len(self.eventos_evolucao)}",
            tipo=TipoEvolucao.CROSSOVER,
            geracao=self.geracao_atual,
            descricao=f"Crossover entre {pai1_id} e {pai2_id}",
            modelo_origem=pai1_id,
            modelo_destino=filho_id,
            impacto_fitness=0.0  # Será atualizado após avaliação
        )
        self.eventos_evolucao.append(evento)
        
        return filho_id
    
    def mutar(
        self,
        genoma_id: str,
        intensidade: float = 0.1,
        caracteristicas_alvo: Optional[List[str]] = None
    ) -> str:
        """Aplicar mutação em um genoma"""
        if genoma_id not in self.genomas:
            raise ValueError("Genoma não encontrado")
        
        genoma_original = self.genomas[genoma_id]
        
        # Criar novo ID
        mutante_id = hashlib.md5(
            f"mut_{genoma_id}_{datetime.now(timezone.utc)}".encode()
        ).hexdigest()[:16]
        
        # Copiar características
        caracteristicas_mutante = genoma_original.caracteristicas.copy()
        
        # Aplicar mutação
        mutacoes_aplicadas = []
        chaves_alvo = caracteristicas_alvo or list(caracteristicas_mutante.keys())
        
        for chave in chaves_alvo:
            if chave in caracteristicas_mutante:
                # Mutação gaussiana
                mutacao = np.random.normal(0, intensidade)
                caracteristicas_mutante[chave] *= (1 + mutacao)
                caracteristicas_mutante[chave] = max(0.0, min(1.0, caracteristicas_mutante[chave]))
                mutacoes_aplicadas.append(f"{chave}: {mutacao:.4f}")
        
        # Criar genoma mutante
        mutante = GenomaModelo(
            id=mutante_id,
            geracao=genoma_original.geracao,
            caracteristicas=caracteristicas_mutante,
            arquitetura=genoma_original.arquitetura,
            hiperparametros=genoma_original.hiperparametros.copy(),
            ancestral_id=genoma_id,
            mutacoes=mutacoes_aplicadas
        )
        
        self.genomas[mutante_id] = mutante
        
        # Atualizar linhagem
        self.linhagens[mutante_id] = LinhagemModelo(
            modelo_id=mutante_id,
            geracao=genoma_original.geracao,
            ancestral_direto=genoma_id
        )
        
        if genoma_id in self.linhagens:
            self.linhagens[genoma_id].descendentes.append(mutante_id)
        
        # Registrar evento
        evento = EventoEvolucao(
            id=f"evo_{len(self.eventos_evolucao)}",
            tipo=TipoEvolucao.MUTACAO,
            geracao=genoma_original.geracao,
            descricao=f"Mutação de {genoma_id}: {', '.join(mutacoes_aplicadas[:3])}",
            modelo_origem=genoma_id,
            modelo_destino=mutante_id,
            impacto_fitness=0.0
        )
        self.eventos_evolucao.append(evento)
        
        return mutante_id
    
    def adaptar_a_regime(
        self,
        novo_regime: str,
        genoma_base_id: str
    ) -> str:
        """Adaptar modelo a novo regime de mercado"""
        if genoma_base_id not in self.genomas:
            raise ValueError("Genoma base não encontrado")
        
        # Verificar se temos campeão para este regime
        if novo_regime in self.campeoes_por_regime:
            campeao_id = self.campeoes_por_regime[novo_regime]
            # Fazer crossover com o campeão
            return self.crossover(genoma_base_id, campeao_id)
        
        # Se não tem campeão, aplicar mutação direcionada
        # Mutação mais forte para adaptação rápida
        adaptado_id = self.mutar(genoma_base_id, intensidade=0.3)
        
        # Registrar adaptação
        adaptacao = {
            'tipo': TipoAdaptacao.REGIME_VOLATILIDADE if 'volatil' in novo_regime else TipoAdaptacao.REGIME_TENDENCIA,
            'regime_anterior': self.regime_atual,
            'regime_novo': novo_regime,
            'genoma_adaptado': adaptado_id,
            'timestamp': datetime.now(timezone.utc).isoformat()
        }
        self.adaptacoes_realizadas.append(adaptacao)
        
        self.regime_atual = novo_regime
        self.historico_regimes.append(novo_regime)
        
        return adaptado_id
    
    def podar_populacao(self, manter_top_n: int = 10):
        """Remover genomas de baixa performance"""
        if len(self.genomas) <= manter_top_n:
            return []
        
        # Calcular fitness de todos
        fitness_scores = [
            (gid, self.calcular_fitness_medio(gid))
            for gid in self.genomas.keys()
        ]
        
        # Ordenar por fitness
        fitness_scores.sort(key=lambda x: x[1], reverse=True)
        
        # Manter top N
        genomas_manter = [x[0] for x in fitness_scores[:manter_top_n]]
        genomas_remover = [x[0] for x in fitness_scores[manter_top_n:]]
        
        # Remover
        for gid in genomas_remover:
            del self.genomas[gid]
            if gid in self.fitness_historico:
                del self.fitness_historico[gid]
        
        return genomas_remover
    
    def evoluir_geracao(self) -> Dict[str, Any]:
        """Executar um ciclo completo de evolução"""
        resultados = {
            'geracao': self.geracao_atual + 1,
            'novos_genomas': [],
            'mutacoes': [],
            'removidos': []
        }
        
        # 1. Selecionar pais
        pais = self.selecionar_pais(n_pais=4)
        
        # 2. Criar offspring via crossover
        for i in range(0, len(pais), 2):
            if i + 1 < len(pais):
                filho_id = self.crossover(pais[i], pais[i+1])
                resultados['novos_genomas'].append(filho_id)
        
        # 3. Aplicar mutações
        for genoma_id in list(self.genomas.keys()):
            if np.random.random() < self.taxa_mutacao:
                mutante_id = self.mutar(genoma_id)
                resultados['mutacoes'].append(mutante_id)
        
        # 4. Podar
        removidos = self.podar_populacao(self.populacao_maxima)
        resultados['removidos'] = removidos
        
        self.geracao_atual += 1
        
        return resultados
    
    def get_arvore_genealogica(self, genoma_id: str) -> Dict[str, Any]:
        """Obter árvore genealógica de um genoma"""
        if genoma_id not in self.linhagens:
            return {}
        
        linhagem = self.linhagens[genoma_id]
        genoma = self.genomas.get(genoma_id)
        
        return {
            'modelo_id': genoma_id,
            'geracao': linhagem.geracao,
            'fitness_atual': self.calcular_fitness_medio(genoma_id),
            'ancestral': linhagem.ancestral_direto,
            'descendentes': linhagem.descendentes,
            'irmaos': linhagem.irmaos,
            'caracteristicas': genoma.caracteristicas if genoma else {},
            'timestamp_criacao': genoma.timestamp_criacao if genoma else None
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de evolução"""
        return {
            'geracao_atual': self.geracao_atual,
            'populacao_atual': len(self.genomas),
            'populacao_maxima': self.populacao_maxima,
            'total_eventos_evolucao': len(self.eventos_evolucao),
            'regime_atual': self.regime_atual,
            'campeoes_por_regime': self.campeoes_por_regime,
            'taxa_mutacao': self.taxa_mutacao,
            'taxa_crossover': self.taxa_crossover,
            'fitness_medio_populacao': np.mean([
                self.calcular_fitness_medio(gid)
                for gid in self.genomas.keys()
            ]) if self.genomas else 0.0,
            'melhor_fitness': max([
                self.calcular_fitness_medio(gid)
                for gid in self.genomas.keys()
            ]) if self.genomas else 0.0
        }
