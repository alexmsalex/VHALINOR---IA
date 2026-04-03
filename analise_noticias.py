"""
VHALINOR Análise de Notícias v6.0
=====================================
Sistema de análise de notícias com:
- Scraping de fontes de notícias
- Análise de sentimento em notícias
- Detecção de eventos de mercado
- Classificação de impacto
- Análise de tendências de notícias
- Correlação notícias-mercado
- Alertas de notícias relevantes
- Sumarização automática
- Extração de entidades
- Análise temporal de notícias

@module analise_noticias
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import re
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from collections import deque, defaultdict
import hashlib


class FonteNoticia(Enum):
    """Fontes de notícias suportadas"""
    REUTERS = "reuters"
    BLOOMBERG = "bloomberg"
    CNBC = "cnbc"
    COINDESK = "coindesk"
    COINTELEGRAPH = "cointelegraph"
    TWITTER = "twitter"
    REDDIT = "reddit"
    FORBES = "forbes"
    WSJ = "wsj"
    FINANCIAL_TIMES = "financial_times"
    CUSTOM = "custom"


class CategoriaNoticia(Enum):
    """Categorias de notícias"""
    ECONOMIA = "economia"
    POLITICA = "politica"
    TECNOLOGIA = "tecnologia"
    CRIPTO = "cripto"
    FINANCAS = "financas"
    MERCADO = "mercado"
    REGULACAO = "regulacao"
    ADOCAO = "adocao"
    HACK = "hack"
    IPO = "ipo"
    FUSAO = "fusao"
    RESULTADO = "resultado"


class SentimentoNoticia(Enum):
    """Sentimento de notícia"""
    MUITO_POSITIVO = "muito_positivo"
    POSITIVO = "positivo"
    NEUTRO = "neutro"
    NEGATIVO = "negativo"
    MUITO_NEGATIVO = "muito_negativo"


class ImpactoMercado(Enum):
    """Impacto esperado no mercado"""
    EXTREMO = "extremo"      # > 10%
    ALTO = "alto"            # 5-10%
    MODERADO = "moderado"    # 2-5%
    BAIXO = "baixo"          # 1-2%
    MINIMO = "minimo"        # < 1%


@dataclass
class Noticia:
    """Representação de uma notícia"""
    id: str
    titulo: str
    conteudo: str
    fonte: FonteNoticia
    url: Optional[str] = None
    autor: Optional[str] = None
    timestamp_publicacao: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    timestamp_coleta: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    categoria: Optional[CategoriaNoticia] = None
    sentimento: Optional[SentimentoNoticia] = None
    score_sentimento: float = 0.0  # -1.0 a 1.0
    impacto: Optional[ImpactoMercado] = None
    score_impacto: float = 0.0  # 0.0 a 1.0
    entidades: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    resumo: Optional[str] = None
    relacionadas: List[str] = field(default_factory=list)
    
    @property
    def idade_horas(self) -> float:
        """Calcular idade da notícia em horas"""
        pub = datetime.fromisoformat(self.timestamp_publicacao)
        agora = datetime.now(timezone.utc)
        return (agora - pub).total_seconds() / 3600


@dataclass
class EventoMercado:
    """Evento de mercado detectado em notícia"""
    tipo: str
    descricao: str
    ativos_afetados: List[str]
    direcao_esperada: str  # "alta", "baixa", "volatilidade"
    magnitude_esperada: float
    confianca: float
    fonte_noticia: str


@dataclass
class TendenciaNoticias:
    """Tendência detectada em notícias"""
    tema: str
    frequencia_24h: int
    frequencia_7d: int
    sentimento_dominante: SentimentoNoticia
    impacto_medio: float
    noticias_relacionadas: List[str]
    evolucao_sentimento: List[Tuple[str, float]]  # (timestamp, score)


class AnaliseNoticias:
    """
    Sistema de análise de notícias para trading.
    
    Processa notícias de múltiplas fontes, analisa sentimento,
    detecta eventos de mercado e correlaciona com movimentos de preço.
    """
    
    def __init__(self, janela_analise_horas: int = 24):
        self.janela_analise = janela_analise_horas
        self.noticias: deque = deque(maxlen=10000)
        self.noticias_por_fonte: Dict[FonteNoticia, deque] = defaultdict(lambda: deque(maxlen=1000))
        self.eventos_detectados: deque = deque(maxlen=500)
        self.tendencias_ativas: Dict[str, TendenciaNoticias] = {}
        
        # Dicionários de sentimento
        self.palavras_positivas = self._carregar_palavras_sentimento('positivo')
        self.palavras_negativas = self._carregar_palavras_sentimento('negativo')
        
        # Dicionários de impacto
        self.palavras_impacto_alto = ['crash', 'colapso', 'crise', 'boom', 'explosão', 'surge']
        self.palavras_impacto_extremo = ['guerra', 'pandemia', 'recessão', 'depressão']
    
    def _carregar_palavras_sentimento(self, tipo: str) -> List[str]:
        """Carregar dicionário de palavras de sentimento"""
        positivas = [
            'bullish', 'alta', 'crescimento', 'ganhos', 'lucro', 'sucesso', 'avanço',
            'expansão', 'boom', 'rally', 'supera', 'bate recorde', 'ótimo', 'excelente',
            'promissor', 'oportunidade', 'adotado', 'parceria', 'integração', 'lançamento'
        ]
        
        negativas = [
            'bearish', 'queda', 'declínio', 'perdas', 'prejuízo', 'falha', 'retracao',
            'crise', 'crash', 'bear market', 'abaixo', 'pessimista', 'preocupante',
            'ameaça', 'hack', 'ataque', 'proibição', 'ban', 'fraud', 'scam'
        ]
        
        return positivas if tipo == 'positivo' else negativas
    
    def adicionar_noticia(
        self,
        titulo: str,
        conteudo: str,
        fonte: FonteNoticia,
        url: Optional[str] = None,
        autor: Optional[str] = None,
        timestamp: Optional[str] = None
    ) -> Noticia:
        """Adicionar e processar uma notícia"""
        # Gerar ID único
        noticia_id = hashlib.md5(f"{titulo}{fonte.value}{datetime.now(timezone.utc)}".encode()).hexdigest()[:16]
        
        # Criar notícia
        noticia = Noticia(
            id=noticia_id,
            titulo=titulo,
            conteudo=conteudo,
            fonte=fonte,
            url=url,
            autor=autor,
            timestamp_publicacao=timestamp or datetime.now(timezone.utc).isoformat()
        )
        
        # Analisar
        noticia.categoria = self._classificar_categoria(noticia)
        noticia.sentimento, noticia.score_sentimento = self._analisar_sentimento(noticia)
        noticia.impacto, noticia.score_impacto = self._avaliar_impacto(noticia)
        noticia.entidades = self._extrair_entidades(noticia)
        noticia.keywords = self._extrair_keywords(noticia)
        noticia.resumo = self._gerar_resumo(noticia)
        
        # Detectar eventos
        eventos = self._detectar_eventos(noticia)
        for evento in eventos:
            self.eventos_detectados.append(evento)
        
        # Armazenar
        self.noticias.append(noticia)
        self.noticias_por_fonte[fonte].append(noticia)
        
        # Atualizar tendências
        self._atualizar_tendencias(noticia)
        
        return noticia
    
    def _classificar_categoria(self, noticia: Noticia) -> CategoriaNoticia:
        """Classificar categoria da notícia"""
        texto = (noticia.titulo + " " + noticia.conteudo).lower()
        
        # Palavras-chave por categoria
        criterios = {
            CategoriaNoticia.CRIPTO: ['bitcoin', 'crypto', 'blockchain', 'ethereum', 'btc', 'eth'],
            CategoriaNoticia.TECNOLOGIA: ['tech', 'tecnologia', 'inovação', 'ai', 'inteligência artificial'],
            CategoriaNoticia.REGULACAO: ['regulamento', 'lei', 'sec', 'cvm', 'banco central', 'fed'],
            CategoriaNoticia.ECONOMIA: ['pib', 'inflação', 'juros', 'economia', 'dólar', 'euro'],
            CategoriaNoticia.POLITICA: ['eleição', 'governo', 'presidente', 'política', 'guerra']
        }
        
        scores = {}
        for categoria, palavras in criterios.items():
            scores[categoria] = sum(1 for p in palavras if p in texto)
        
        if scores:
            return max(scores, key=scores.get)
        
        return CategoriaNoticia.MERCADO
    
    def _analisar_sentimento(self, noticia: Noticia) -> Tuple[SentimentoNoticia, float]:
        """Analisar sentimento da notícia"""
        texto = (noticia.titulo + " " + noticia.conteudo).lower()
        
        # Contar palavras positivas e negativas
        positivas = sum(1 for p in self.palavras_positivas if p in texto)
        negativas = sum(1 for p in self.palavras_negativas if p in texto)
        
        # Calcular score (-1.0 a 1.0)
        total = positivas + negativas
        if total == 0:
            return SentimentoNoticia.NEUTRO, 0.0
        
        score = (positivas - negativas) / max(total, 5)
        score = max(-1.0, min(1.0, score))
        
        # Classificar
        if score > 0.6:
            return SentimentoNoticia.MUITO_POSITIVO, score
        elif score > 0.2:
            return SentimentoNoticia.POSITIVO, score
        elif score < -0.6:
            return SentimentoNoticia.MUITO_NEGATIVO, score
        elif score < -0.2:
            return SentimentoNoticia.NEGATIVO, score
        else:
            return SentimentoNoticia.NEUTRO, score
    
    def _avaliar_impacto(self, noticia: Noticia) -> Tuple[ImpactoMercado, float]:
        """Avaliar impacto potencial da notícia no mercado"""
        texto = (noticia.titulo + " " + noticia.conteudo).lower()
        
        score = 0.0
        
        # Palavras de alto impacto
        for palavra in self.palavras_impacto_extremo:
            if palavra in texto:
                score += 0.5
        
        for palavra in self.palavras_impacto_alto:
            if palavra in texto:
                score += 0.3
        
        # Intensificadores
        if 'urgente' in texto or 'breaking' in texto:
            score += 0.2
        
        # Fonte confiável
        if noticia.fonte in [FonteNoticia.BLOOMBERG, FonteNoticia.REUTERS, FonteNoticia.WSJ]:
            score += 0.1
        
        score = min(1.0, score)
        
        # Classificar
        if score >= 0.8:
            return ImpactoMercado.EXTREMO, score
        elif score >= 0.6:
            return ImpactoMercado.ALTO, score
        elif score >= 0.4:
            return ImpactoMercado.MODERADO, score
        elif score >= 0.2:
            return ImpactoMercado.BAIXO, score
        else:
            return ImpactoMercado.MINIMO, score
    
    def _extrair_entidades(self, noticia: Noticia) -> List[str]:
        """Extrair entidades mencionadas na notícia"""
        texto = noticia.titulo + " " + noticia.conteudo
        
        # Regex para encontrar possíveis entidades (maiúsculas)
        entidades = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', texto)
        
        # Filtrar e normalizar
        entidades_unicas = list(set([e.strip() for e in entidades if len(e) > 2]))
        
        return entidades_unicas[:20]  # Limitar a 20
    
    def _extrair_keywords(self, noticia: Noticia) -> List[str]:
        """Extrair keywords da notícia"""
        texto = (noticia.titulo + " " + noticia.conteudo).lower()
        
        # Palavras mais relevantes (frequentes e significativas)
        palavras = re.findall(r'\b[a-z]{4,}\b', texto)
        
        # Contar frequência
        freq = defaultdict(int)
        for p in palavras:
            if p not in ['como', 'onde', 'quando', 'este', 'esta', 'para', 'pelo']:
                freq[p] += 1
        
        # Top keywords
        keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return [k[0] for k in keywords]
    
    def _gerar_resumo(self, noticia: Noticia) -> str:
        """Gerar resumo automático da notícia"""
        # Extrair primeiras frases importantes
        sentencas = noticia.conteudo.split('.')
        
        # Pegar até 3 sentenças
        resumo = '. '.join([s.strip() for s in sentencas[:3] if len(s.strip()) > 20])
        
        if len(resumo) > 300:
            resumo = resumo[:297] + '...'
        
        return resumo
    
    def _detectar_eventos(self, noticia: Noticia) -> List[EventoMercado]:
        """Detectar eventos de mercado na notícia"""
        eventos = []
        texto = (noticia.titulo + " " + noticia.conteudo).lower()
        
        # Padrões de eventos
        padroes_eventos = [
            ('resultado_trimestral', r'resultado|earnings|lucro|receita', ['resultado'], 'volatilidade'),
            ('fusao_aquisicao', r'fusão|aquisição|acquisition|merge', ['fusao'], 'alta'),
            ('regulacao', r'regulamentação|regulamento|lei|proibição', ['regulacao'], 'baixa'),
            ('hack', r'hack|ataque|breach|vulnerabilidade', ['hack'], 'baixa'),
            ('parceria', r'parceria|partnership|colaboração', ['adocao'], 'alta')
        ]
        
        for tipo, padrao, ativos, direcao in padroes_eventos:
            if re.search(padrao, texto):
                evento = EventoMercado(
                    tipo=tipo,
                    descricao=f"Evento {tipo} detectado em notícia",
                    ativos_afetados=ativos,
                    direcao_esperada=direcao,
                    magnitude_esperada=noticia.score_impacto * 10,
                    confianca=noticia.score_impacto,
                    fonte_noticia=noticia.id
                )
                eventos.append(evento)
        
        return eventos
    
    def _atualizar_tendencias(self, noticia: Noticia):
        """Atualizar tendências baseado na notícia"""
        for keyword in noticia.keywords[:3]:
            if keyword not in self.tendencias_ativas:
                self.tendencias_ativas[keyword] = TendenciaNoticias(
                    tema=keyword,
                    frequencia_24h=0,
                    frequencia_7d=0,
                    sentimento_dominante=noticia.sentimento or SentimentoNoticia.NEUTRO,
                    impacto_medio=noticia.score_impacto,
                    noticias_relacionadas=[noticia.id],
                    evolucao_sentimento=[(noticia.timestamp_publicacao, noticia.score_sentimento)]
                )
            else:
                tendencia = self.tendencias_ativas[keyword]
                tendencia.frequencia_24h += 1
                tendencia.frequencia_7d += 1
                tendencia.noticias_relacionadas.append(noticia.id)
                tendencia.evolucao_sentimento.append(
                    (noticia.timestamp_publicacao, noticia.score_sentimento)
                )
    
    def buscar_noticias(
        self,
        categoria: Optional[CategoriaNoticia] = None,
        sentimento: Optional[SentimentoNoticia] = None,
        impacto_minimo: Optional[ImpactoMercado] = None,
        palavra_chave: Optional[str] = None,
        horas: int = 24
    ) -> List[Noticia]:
        """Buscar notícias com filtros"""
        resultado = []
        
        corte = datetime.now(timezone.utc) - timedelta(hours=horas)
        
        for noticia in self.noticias:
            # Verificar idade
            if datetime.fromisoformat(noticia.timestamp_coleta) < corte:
                continue
            
            # Filtros
            if categoria and noticia.categoria != categoria:
                continue
            
            if sentimento and noticia.sentimento != sentimento:
                continue
            
            if impacto_minimo and noticia.score_impacto < self._impacto_para_score(impacto_minimo):
                continue
            
            if palavra_chave and palavra_chave.lower() not in (noticia.titulo + noticia.conteudo).lower():
                continue
            
            resultado.append(noticia)
        
        # Ordenar por relevância (impacto * recência)
        resultado.sort(key=lambda n: n.score_impacto / (n.idade_horas + 1), reverse=True)
        
        return resultado
    
    def _impacto_para_score(self, impacto: ImpactoMercado) -> float:
        """Converter impacto para score numérico"""
        mapping = {
            ImpactoMercado.MINIMO: 0.0,
            ImpactoMercado.BAIXO: 0.2,
            ImpactoMercado.MODERADO: 0.4,
            ImpactoMercado.ALTO: 0.6,
            ImpactoMercado.EXTREMO: 0.8
        }
        return mapping.get(impacto, 0.0)
    
    def gerar_sentimento_mercado(self, horas: int = 24) -> Dict[str, Any]:
        """Gerar análise agregada de sentimento de mercado"""
        noticias_recentes = self.buscar_noticias(horas=horas)
        
        if not noticias_recentes:
            return {'sentimento': 'neutro', 'score': 0.0, 'confianca': 0.0}
        
        # Calcular score médio ponderado por impacto
        total_peso = sum(n.score_impacto + 0.1 for n in noticias_recentes)
        score_ponderado = sum(n.score_sentimento * (n.score_impacto + 0.1) for n in noticias_recentes) / total_peso
        
        # Classificar
        if score_ponderado > 0.5:
            sentimento = 'muito_positivo'
        elif score_ponderado > 0.2:
            sentimento = 'positivo'
        elif score_ponderado < -0.5:
            sentimento = 'muito_negativo'
        elif score_ponderado < -0.2:
            sentimento = 'negativo'
        else:
            sentimento = 'neutro'
        
        return {
            'sentimento': sentimento,
            'score': score_ponderado,
            'n_noticias': len(noticias_recentes),
            'n_positivas': len([n for n in noticias_recentes if n.score_sentimento > 0.2]),
            'n_negativas': len([n for n in noticias_recentes if n.score_sentimento < -0.2]),
            'impacto_medio': sum(n.score_impacto for n in noticias_recentes) / len(noticias_recentes),
            'confianca': min(1.0, len(noticias_recentes) / 50)  # Mais notícias = mais confiança
        }
    
    def correlacionar_com_preco(
        self,
        noticias: List[Noticia],
        variacao_preco: float
    ) -> Dict[str, Any]:
        """Correlacionar notícias com movimento de preço"""
        if not noticias:
            return {'correlacao': 0.0, 'noticias_relevantes': []}
        
        # Calcular sentimento médio
        sentimento_medio = sum(n.score_sentimento for n in noticias) / len(noticias)
        
        # Verificar se movimento está alinhado com sentimento
        alinhamento = (sentimento_medio > 0 and variacao_preco > 0) or (sentimento_medio < 0 and variacao_preco < 0)
        
        # Noticias mais relevantes
        noticias_relevantes = sorted(
            noticias,
            key=lambda n: n.score_impacto * abs(n.score_sentimento),
            reverse=True
        )[:5]
        
        return {
            'correlacao': abs(sentimento_medio) if alinhamento else -abs(sentimento_medio),
            'sentimento_previsto': sentimento_medio,
            'variacao_real': variacao_preco,
            'alinhamento': alinhamento,
            'noticias_relevantes': [n.id for n in noticias_relevantes]
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de análise de notícias"""
        return {
            'total_noticias': len(self.noticias),
            'noticias_24h': len(self.buscar_noticias(horas=24)),
            'eventos_detectados': len(self.eventos_detectados),
            'tendencias_ativas': len(self.tendencias_ativas),
            'fontes_monitoradas': len(self.noticias_por_fonte),
            'sentimento_atual': self.gerar_sentimento_mercado(horas=1),
            'categorias_dist': {c.value: len(self.buscar_noticias(categoria=c, horas=24)) for c in CategoriaNoticia}
        }
