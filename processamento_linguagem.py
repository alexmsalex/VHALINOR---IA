"""
VHALINOR Processamento de Linguagem v6.0
===========================================
Sistema de processamento de linguagem natural com:
- Compreensão de texto
- Geração de linguagem
- Análise semântica
- Extração de entidades
- Análise de sentimento
- Resumo automático

@module processamento_linguagem
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Union, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import defaultdict
import re
import hashlib


class ModeloLinguagem(Enum):
    """Modelos de linguagem suportados"""
    GPT = "gpt"
    BERT = "bert"
    T5 = "t5"
    LLAMA = "llama"
    CUSTOM = "custom"
    REGRAS = "regras"


class TipoAnalise(Enum):
    """Tipos de análise de texto"""
    SENTIMENTO = "sentimento"
    ENTIDADES = "entidades"
    INTENCAO = "intencao"
    SUMARIZACAO = "sumarizacao"
    CLASSIFICACAO = "classificacao"
    SIMILARIDADE = "similaridade"
    TRADUCAO = "traducao"
    GERACAO = "geracao"


@dataclass
class Entidade:
    """Entidade extraída do texto"""
    texto: str
    tipo: str  # PESSOA, ORGANIZACAO, LOCAL, DATA, VALOR, etc.
    posicao_inicio: int
    posicao_fim: int
    confianca: float
    atributos: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Intencao:
    """Intenção detectada no texto"""
    tipo: str  # CONSULTA, COMANDO, PERGUNTA, AFIRMACAO, etc.
    confianca: float
    entidades_chave: List[str] = field(default_factory=list)
    acao_sugerida: Optional[str] = None


@dataclass
class ResultadoAnalise:
    """Resultado de análise de texto"""
    texto_original: str
    tipo_analise: TipoAnalise
    resultado: Any
    confianca: float
    tempo_processamento_ms: float
    modelo_usado: ModeloLinguagem
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProcessamentoLinguagem:
    """
    Sistema de processamento de linguagem natural.
    """
    
    def __init__(self, modelo_padrao: ModeloLinguagem = ModeloLinguagem.REGRAS):
        self.modelo_padrao = modelo_padrao
        self.modelos_disponiveis = [ModeloLinguagem.REGRAS]
        
        # Bases de conhecimento
        self.dicionario_sentimentos = self._carregar_dicionario_sentimentos()
        self.patterns_entidades = self._carregar_patterns_entidades()
        self.templates_respostas = self._carregar_templates()
        
        # Histórico
        self.historico_analises: List[ResultadoAnalise] = []
        self.contexto_conversa: Dict[str, Any] = {}
    
    def _carregar_dicionario_sentimentos(self) -> Dict[str, float]:
        """Carregar dicionário de palavras com sentimentos"""
        return {
            # Positivos
            'bom': 0.8, 'otimo': 1.0, 'excelente': 1.0, 'maravilhoso': 1.0,
            'positivo': 0.7, 'otimista': 0.8, 'crescimento': 0.6, 'alta': 0.5,
            'compra': 0.6, 'bullish': 0.8, 'sucesso': 0.9, 'ganho': 0.7,
            'lucro': 0.8, 'subida': 0.6, 'recuperacao': 0.6, 'forte': 0.6,
            
            # Negativos
            'ruim': -0.8, 'pessimo': -1.0, 'terrivel': -1.0, 'horrivel': -1.0,
            'negativo': -0.7, 'pessimista': -0.8, 'queda': -0.6, 'baixa': -0.5,
            'venda': -0.6, 'bearish': -0.8, 'fracasso': -0.9, 'perda': -0.7,
            'prejuizo': -0.8, 'queda': -0.6, 'crise': -0.9, 'fraco': -0.6,
            'colapso': -1.0, 'crash': -1.0, 'panico': -0.9,
            
            # Neutros/Modificadores
            'neutro': 0.0, 'estavel': 0.1, 'lateral': 0.0, 'consolidacao': 0.0,
            'muito': 1.5, 'pouco': 0.5, 'extremamente': 2.0, 'levemente': 0.3
        }
    
    def _carregar_patterns_entidades(self) -> List[Tuple[str, str]]:
        """Carregar patterns para extração de entidades"""
        return [
            (r'\b[A-Z][a-z]+ (Corporation|Corp|Inc|Ltd|LLC|Company)\b', 'ORGANIZACAO'),
            (r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', 'PESSOA'),
            (r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', 'DATA'),
            (r'\b\d{1,2} de [a-zA-Z]+ de? \d{4}\b', 'DATA'),
            (r'\$[\d,]+\.?\d*', 'VALOR_MONETARIO'),
            (r'\b\d+\.?\d*\s*(USD|EUR|BTC|ETH)\b', 'VALOR_CRIPTO'),
            (r'\b\d+\.?\d*%\b', 'PERCENTUAL'),
            (r'\b(Android|iOS|Windows|Linux|MacOS)\b', 'SISTEMA_OPERACIONAL'),
            (r'\b(Nova York|São Paulo|Londres|Tóquio|Singapura)\b', 'LOCAL'),
        ]
    
    def _carregar_templates(self) -> Dict[str, List[str]]:
        """Carregar templates de resposta"""
        return {
            'saudacao': [
                "Olá! Como posso ajudar?",
                "Bem-vindo! Estou pronto para ajudar.",
                "Oi! O que posso fazer por você hoje?"
            ],
            'despedida': [
                "Até logo! Foi um prazer ajudar.",
                "Tchau! Volte sempre.",
                "Até a próxima!"
            ],
            'nao_entendi': [
                "Desculpe, não entendi completamente. Pode reformular?",
                "Não compreendi bem. Pode explicar de outra forma?",
                "Estou com dificuldade de entender. Pode ser mais específico?"
            ],
            'confirmacao': [
                "Entendido!",
                "Compreendido!",
                "Certo!"
            ]
        }
    
    def analisar_sentimento(self, texto: str) -> ResultadoAnalise:
        """Analisar sentimento do texto"""
        inicio = datetime.now(timezone.utc)
        
        # Tokenização simples
        palavras = texto.lower().split()
        
        # Calcular sentimento
        sentimento_total = 0.0
        palavras_sentimento = []
        modificador = 1.0
        
        for palavra in palavras:
            # Limpar pontuação
            palavra_limpa = re.sub(r'[^\w]', '', palavra)
            
            if palavra_limpa in self.dicionario_sentimentos:
                valor = self.dicionario_sentimentos[palavra_limpa]
                
                # Verificar se é modificador
                if abs(valor) > 1.0:
                    modificador = valor
                else:
                    sentimento_total += valor * modificador
                    palavras_sentimento.append((palavra_limpa, valor))
                    modificador = 1.0
        
        # Normalizar
        if palavras:
            sentimento_normalizado = sentimento_total / len(palavras)
        else:
            sentimento_normalizado = 0.0
        
        # Classificar
        if sentimento_normalizado > 0.2:
            classificacao = 'positivo'
        elif sentimento_normalizado < -0.2:
            classificacao = 'negativo'
        else:
            classificacao = 'neutro'
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoAnalise(
            texto_original=texto,
            tipo_analise=TipoAnalise.SENTIMENTO,
            resultado={
                'sentimento': sentimento_normalizado,
                'classificacao': classificacao,
                'palavras_chave': palavras_sentimento
            },
            confianca=abs(sentimento_normalizado) if palavras_sentimento else 0.3,
            tempo_processamento_ms=tempo,
            modelo_usado=self.modelo_padrao
        )
    
    def extrair_entidades(self, texto: str) -> ResultadoAnalise:
        """Extrair entidades do texto"""
        inicio = datetime.now(timezone.utc)
        
        entidades = []
        
        for pattern, tipo in self.patterns_entidades:
            for match in re.finditer(pattern, texto):
                entidade = Entidade(
                    texto=match.group(),
                    tipo=tipo,
                    posicao_inicio=match.start(),
                    posicao_fim=match.end(),
                    confianca=0.8
                )
                entidades.append(entidade)
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoAnalise(
            texto_original=texto,
            tipo_analise=TipoAnalise.ENTIDADES,
            resultado=[{
                'texto': e.texto,
                'tipo': e.tipo,
                'posicao': (e.posicao_inicio, e.posicao_fim),
                'confianca': e.confianca
            } for e in entidades],
            confianca=0.8 if entidades else 0.4,
            tempo_processamento_ms=tempo,
            modelo_usado=self.modelo_padrao
        )
    
    def detectar_intencao(self, texto: str) -> ResultadoAnalise:
        """Detectar intenção do usuário"""
        inicio = datetime.now(timezone.utc)
        
        texto_lower = texto.lower()
        
        # Palavras-chave por intenção
        intencoes_keywords = {
            'consulta': ['qual', 'quanto', 'como', 'onde', 'quando', 'por que', 'explique'],
            'comando': ['execute', 'rode', 'inicie', 'pare', 'configure', 'defina', 'mude'],
            'pergunta': ['?', 'qual é', 'saber', 'informacao', 'dados'],
            'afirmacao': ['é', 'são', 'está', 'foi', 'será'],
            'negociacao': ['compre', 'venda', 'ordem', 'trade', 'posicao', 'entrada', 'saida']
        }
        
        # Detectar intenção
        melhor_intencao = 'desconhecida'
        melhor_score = 0
        
        for intencao, keywords in intencoes_keywords.items():
            score = sum(1 for kw in keywords if kw in texto_lower)
            if score > melhor_score:
                melhor_score = score
                melhor_intencao = intencao
        
        # Detectar se é pergunta
        if '?' in texto:
            melhor_intencao = 'pergunta'
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoAnalise(
            texto_original=texto,
            tipo_analise=TipoAnalise.INTENCAO,
            resultado=Intencao(
                tipo=melhor_intencao,
                confianca=0.6 + (melhor_score * 0.1),
                entidades_chave=[],
                acao_sugerida=self._sugerir_acao(melhor_intencao)
            ),
            confianca=0.6 + (melhor_score * 0.1),
            tempo_processamento_ms=tempo,
            modelo_usado=self.modelo_padrao
        )
    
    def _sugerir_acao(self, intencao: str) -> Optional[str]:
        """Sugerir ação baseada na intenção"""
        acoes = {
            'consulta': 'buscar_informacao',
            'comando': 'executar_comando',
            'pergunta': 'responder_pergunta',
            'negociacao': 'analisar_negociacao',
            'afirmacao': 'confirmar_informacao'
        }
        return acoes.get(intencao)
    
    def sumarizar(self, texto: str, max_sentencas: int = 3) -> ResultadoAnalise:
        """Sumarizar texto"""
        inicio = datetime.now(timezone.utc)
        
        # Divisão simples em sentenças
        sentencas = re.split(r'[.!?]+', texto)
        sentencas = [s.strip() for s in sentencas if s.strip()]
        
        # Selecionar primeiras sentenças (estratégia simples)
        # Em uma implementação real, usaria importância das sentenças
        resumo_sentencas = sentencas[:max_sentencas]
        
        resumo = '. '.join(resumo_sentencas)
        if not resumo.endswith('.'):
            resumo += '.'
        
        tempo = (datetime.now(timezone.utc) - inicio).total_seconds() * 1000
        
        return ResultadoAnalise(
            texto_original=texto,
            tipo_analise=TipoAnalise.SUMARIZACAO,
            resultado={
                'resumo': resumo,
                'sentencas_originais': len(sentencas),
                'sentencas_resumo': len(resumo_sentencas),
                'taxa_compressao': len(resumo) / len(texto) if texto else 0
            },
            confianca=0.7,
            tempo_processamento_ms=tempo,
            modelo_usado=self.modelo_padrao
        )
    
    def gerar_resposta(self, contexto: str, intencao: str, parametros: Optional[Dict] = None) -> str:
        """Gerar resposta baseada em templates"""
        # Selecionar template baseado na intenção
        if intencao in self.templates_respostas:
            import random
            return random.choice(self.templates_respostas[intencao])
        
        # Resposta genérica
        return "Entendido. Processando sua solicitação..."
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do processamento de linguagem"""
        return {
            'modelo_padrao': self.modelo_padrao.value,
            'modelos_disponiveis': [m.value for m in self.modelos_disponiveis],
            'tamanho_dicionario': len(self.dicionario_sentimentos),
            'patterns_entidades': len(self.patterns_entidades),
            'templates_carregados': len(self.templates_respostas),
            'analises_realizadas': len(self.historico_analises)
        }
