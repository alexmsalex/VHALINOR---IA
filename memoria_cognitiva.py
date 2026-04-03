"""
VHALINOR Memória Cognitiva v6.0
=================================
Sistema de memória cognitiva multi-camada com:
- Memória sensorial (ultra curto prazo)
- Memória de trabalho (curto prazo)
- Memória de curto prazo
- Memória de longo prazo
- Memória episódica
- Memória semântica
- Memória procedural

@module memoria_cognitiva
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from collections import deque, defaultdict
import hashlib
import json


class TipoMemoria(Enum):
    """Tipos de memória cognitiva"""
    SENSORIAL = "sensorial"           # Milissegundos a segundos
    TRABALHO = "trabalho"             # Segundos a minutos
    CURTO_PRAZO = "curto_prazo"       # Minutos a horas
    LONGO_PRAZO = "longo_prazo"       # Dias a anos
    EPISODICA = "episodica"           # Eventos específicos
    SEMANTICA = "semantica"           # Conhecimento geral
    PROCEDURAL = "procedural"         # Habilidades e procedimentos


@dataclass
class ItemMemoria:
    """Item de memória"""
    id: str
    conteudo: Any
    tipo: TipoMemoria
    timestamp: datetime
    importancia: float = 0.5  # 0.0 a 1.0
    acessos: int = 0
    ultimo_acesso: Optional[datetime] = None
    associacoes: List[str] = field(default_factory=list)
    contexto: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def idade(self) -> timedelta:
        """Calcular idade do item"""
        return datetime.now(timezone.utc) - self.timestamp
    
    @property
    def reforco(self) -> float:
        """Calcular força de reforço da memória"""
        if self.acessos == 0:
            return self.importancia * 0.5
        
        # Fórmula de reforço: importância * log(acessos + 1)
        import math
        return min(1.0, self.importancia * (1 + math.log(self.acessos + 1) * 0.1))


class MemoriaCognitiva:
    """
    Sistema completo de memória cognitiva inspirado na arquitetura
    da memória humana.
    """
    
    def __init__(self):
        # Capacidades por tipo de memória
        self.capacidades = {
            TipoMemoria.SENSORIAL: 100,      # 100 itens
            TipoMemoria.TRABALHO: 7,         # 7±2 itens (lei de Miller)
            TipoMemoria.CURTO_PRAZO: 1000,
            TipoMemoria.LONGO_PRAZO: 100000,
            TipoMemoria.EPISODICA: 10000,
            TipoMemoria.SEMANTICA: 50000,
            TipoMemoria.PROCEDURAL: 10000
        }
        
        # Decay rates (meia-vida em segundos)
        self.decay_rates = {
            TipoMemoria.SENSORIAL: 1,        # 1 segundo
            TipoMemoria.TRABALHO: 30,        # 30 segundos
            TipoMemoria.CURTO_PRAZO: 3600,   # 1 hora
            TipoMemoria.LONGO_PRAZO: 86400 * 365,  # 1 ano
            TipoMemoria.EPISODICA: 86400 * 30,     # 30 dias
            TipoMemoria.SEMANTICA: 86400 * 365 * 10,  # 10 anos
            TipoMemoria.PROCEDURAL: 86400 * 365 * 5   # 5 anos
        }
        
        # Armazenamentos
        self.memorias: Dict[TipoMemoria, Dict[str, ItemMemoria]] = {
            tipo: {} for tipo in TipoMemoria
        }
        
        # Índices
        self.indice_temporal: deque = deque(maxlen=10000)
        self.indice_conteudo: Dict[str, List[str]] = defaultdict(list)
    
    def armazenar(
        self,
        conteudo: Any,
        tipo: TipoMemoria,
        importancia: float = 0.5,
        contexto: Optional[Dict] = None,
        associacoes: Optional[List[str]] = None
    ) -> str:
        """Armazenar item na memória"""
        # Gerar ID
        id_item = hashlib.md5(
            f"{conteudo}{datetime.now(timezone.utc)}".encode()
        ).hexdigest()[:16]
        
        item = ItemMemoria(
            id=id_item,
            conteudo=conteudo,
            tipo=tipo,
            timestamp=datetime.now(timezone.utc),
            importancia=importancia,
            contexto=contexto or {},
            associacoes=associacoes or []
        )
        
        # Verificar capacidade
        if len(self.memorias[tipo]) >= self.capacidades[tipo]:
            self._evict(tipo)
        
        # Armazenar
        self.memorias[tipo][id_item] = item
        self.indice_temporal.append((tipo, id_item))
        
        # Indexar conteúdo
        self._indexar_conteudo(item)
        
        # Consolidar para memória de longo prazo se necessário
        if tipo == TipoMemoria.CURTO_PRAZO and importancia > 0.8:
            self._consolidar_para_longo_prazo(item)
        
        return id_item
    
    def recuperar(self, id_item: str, tipo: Optional[TipoMemoria] = None) -> Optional[ItemMemoria]:
        """Recuperar item da memória"""
        if tipo:
            item = self.memorias[tipo].get(id_item)
        else:
            # Buscar em todos os tipos
            item = None
            for t in TipoMemoria:
                if id_item in self.memorias[t]:
                    item = self.memorias[t][id_item]
                    break
        
        if item:
            item.acessos += 1
            item.ultimo_acesso = datetime.now(timezone.utc)
        
        return item
    
    def buscar(
        self,
        query: str,
        tipo: Optional[TipoMemoria] = None,
        limite: int = 10
    ) -> List[ItemMemoria]:
        """Buscar itens por conteúdo"""
        resultados = []
        
        tipos_busca = [tipo] if tipo else list(TipoMemoria)
        
        for t in tipos_busca:
            for item in self.memorias[t].values():
                score = self._calcular_similaridade(query, item)
                if score > 0.3:
                    resultados.append((item, score))
        
        # Ordenar por score e retornar top N
        resultados.sort(key=lambda x: x[1], reverse=True)
        
        for item, _ in resultados[:limite]:
            item.acessos += 1
            item.ultimo_acesso = datetime.now(timezone.utc)
        
        return [item for item, _ in resultados[:limite]]
    
    def recuperar_por_contexto(
        self,
        chave: str,
        valor: Any,
        limite: int = 10
    ) -> List[ItemMemoria]:
        """Recuperar itens por contexto"""
        resultados = []
        
        for tipo in TipoMemoria:
            for item in self.memorias[tipo].values():
                if item.contexto.get(chave) == valor:
                    resultados.append(item)
        
        # Ordenar por importância e recência
        resultados.sort(
            key=lambda x: (x.importancia, x.timestamp),
            reverse=True
        )
        
        return resultados[:limite]
    
    def recuperar_associados(self, id_item: str) -> List[ItemMemoria]:
        """Recuperar itens associados"""
        item = self.recuperar(id_item)
        if not item:
            return []
        
        associados = []
        for assoc_id in item.associacoes:
            assoc = self.recuperar(assoc_id)
            if assoc:
                associados.append(assoc)
        
        return associados
    
    def atualizar_importancia(self, id_item: str, nova_importancia: float) -> bool:
        """Atualizar importância de um item"""
        for tipo in TipoMemoria:
            if id_item in self.memorias[tipo]:
                self.memorias[tipo][id_item].importancia = nova_importancia
                return True
        return False
    
    def esquecer(self, id_item: str) -> bool:
        """Remover item da memória (esquecer)"""
        for tipo in TipoMemoria:
            if id_item in self.memorias[tipo]:
                del self.memorias[tipo][id_item]
                return True
        return False
    
    def consolidar(self):
        """Consolidar memórias (transferir de curto para longo prazo)"""
        itens_consolidar = []
        
        for id_item, item in list(self.memorias[TipoMemoria.CURTO_PRAZO].items()):
            # Critérios de consolidação
            if item.acessos >= 3 and item.importancia > 0.6:
                itens_consolidar.append((id_item, item))
        
        for id_item, item in itens_consolidar:
            self._consolidar_para_longo_prazo(item)
            del self.memorias[TipoMemoria.CURTO_PRAZO][id_item]
    
    def decaimento(self):
        """Aplicar decaimento natural das memórias"""
        agora = datetime.now(timezone.utc)
        
        for tipo in TipoMemoria:
            itens_remover = []
            
            for id_item, item in self.memorias[tipo].items():
                idade = (agora - item.timestamp).total_seconds()
                meia_vida = self.decay_rates[tipo]
                
                # Probabilidade de retenção baseada na curva de esquecimento de Ebbinghaus
                import math
                probabilidade_retenção = math.exp(-idade / meia_vida)
                
                # Reforço aumenta probabilidade
                probabilidade_retenção *= (0.5 + 0.5 * item.reforco)
                
                if probabilidade_retenção < 0.1 and item.acessos < 2:
                    itens_remover.append(id_item)
            
            for id_item in itens_remover:
                del self.memorias[tipo][id_item]
    
    def _evict(self, tipo: TipoMemoria):
        """Remover item menos importante para liberar espaço"""
        if not self.memorias[tipo]:
            return
        
        # Encontrar item com menor score combinado
        menor_score = float('inf')
        id_remover = None
        
        for id_item, item in self.memorias[tipo].items():
            # Score = importância * reforço / idade
            idade_horas = item.idade.total_seconds() / 3600
            if idade_horas > 0:
                score = item.importancia * item.reforco / (1 + idade_horas)
            else:
                score = item.importancia * item.reforco
            
            if score < menor_score:
                menor_score = score
                id_remover = id_item
        
        if id_remover:
            del self.memorias[tipo][id_remover]
    
    def _consolidar_para_longo_prazo(self, item: ItemMemoria):
        """Consolidar item para memória de longo prazo"""
        novo_item = ItemMemoria(
            id=item.id,
            conteudo=item.conteudo,
            tipo=TipoMemoria.LONGO_PRAZO,
            timestamp=item.timestamp,
            importancia=item.importancia,
            acessos=item.acessos,
            ultimo_acesso=item.ultimo_acesso,
            associacoes=item.associacoes.copy(),
            contexto=item.contexto.copy()
        )
        
        if len(self.memorias[TipoMemoria.LONGO_PRAZO]) >= self.capacidades[TipoMemoria.LONGO_PRAZO]:
            self._evict(TipoMemoria.LONGO_PRAZO)
        
        self.memorias[TipoMemoria.LONGO_PRAZO][item.id] = novo_item
    
    def _indexar_conteudo(self, item: ItemMemoria):
        """Indexar conteúdo para busca"""
        # Indexar palavras-chave
        if isinstance(item.conteudo, str):
            palavras = item.conteudo.lower().split()
            for palavra in palavras:
                self.indice_conteudo[palavra].append(item.id)
    
    def _calcular_similaridade(self, query: str, item: ItemMemoria) -> float:
        """Calcular similaridade entre query e item"""
        if not isinstance(item.conteudo, str):
            return 0.0
        
        query_lower = query.lower()
        conteudo_lower = item.conteudo.lower()
        
        # Similaridade simples baseada em presença de palavras
        palavras_query = set(query_lower.split())
        palavras_conteudo = set(conteudo_lower.split())
        
        if not palavras_query:
            return 0.0
        
        intersecao = palavras_query & palavras_conteudo
        return len(intersecao) / len(palavras_query)
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status da memória cognitiva"""
        return {
            'ocupacao': {
                tipo.value: {
                    'itens': len(self.memorias[tipo]),
                    'capacidade': self.capacidades[tipo],
                    'percentual': len(self.memorias[tipo]) / self.capacidades[tipo] * 100
                }
                for tipo in TipoMemoria
            },
            'total_itens': sum(len(m) for m in self.memorias.values()),
            'indice_temporal_size': len(self.indice_temporal),
            'indice_conteudo_size': len(self.indice_conteudo)
        }
