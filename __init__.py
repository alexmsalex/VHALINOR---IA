"""
VHALINOR AI Geral v6.0
=======================
Módulo de Inteligência Artificial Geral (AGI) com sistemas cognitivos,
consciência artificial, sentiência artificial, raciocínio avançado e aprendizado contínuo.

@package ai_geral
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

__version__ = "6.0.0"
__author__ = "VHALINOR Team"
__date__ = "2026-04-01"

# Import all AI Geral components
from .consciencia_artificial import ConscienciaArtificial, EstadoConsciencia
from .sentiencia_artificial import SentienciaArtificial, NivelSentiencia, EstadoEmocional, TipoQualia
from .raciocinio_avancado import RaciocinioAvancado, TipoRaciocinio
from .memoria_cognitiva import MemoriaCognitiva, TipoMemoria
from .aprendizado_continuo import AprendizadoContinuo, EstrategiaAprendizado
from .aprendizado_profundo import (
    AprendizadoProfundo, ConfigDeepLearning, ResultadoTreinamento,
    ArquiteturaDeepLearning, TipoOtimizacao, LRScheduler
)
from .analise_profunda_padroes import (
    AnaliseProfundaPadroes, PadraoDetectado, CicloDetectado, AnomaliaPadrao,
    TipoPadrao, FormacaoGrafica, PadraoCandlestick
)
from .analise_quantica import (
    AnaliseQuantica, Qubit, CircuitoQuantico, ResultadoMedicao, MetricasQuantica,
    EstadoQubit, TipoGate, AlgoritmoQuantico
)
from .analise_noticias import (
    AnaliseNoticias, Noticia, EventoMercado, TendenciaNoticias,
    FonteNoticia, CategoriaNoticia, SentimentoNoticia, ImpactoMercado
)
from .analise_mercado_financeiro import (
    AnaliseMercadoFinanceiro, MetricaFundamentalista, DadoMacroeconomico,
    FluxoOrdem, NivelBook, AlertaRisco, AnaliseSetor,
    TipoAtivo, TimeFrame, IndicadorEconomico, SentimentoInstitucional
)
from .analise_day_trade import (
    AnaliseDayTrade, NivelVolume, SetupDayTrade, SinalVWAP,
    AnaliseLiquidez, EstatisticasIntraday,
    EstrategiaDayTrade, MomentoDia, TipoSetup
)
from .evolucao_aprendizado import (
    EvolucaoAprendizado, GenomaModelo, FitnessSnapshot, EventoEvolucao,
    LinhagemModelo, TipoEvolucao, EstagioEvolucao, TipoAdaptacao
)
from .sensorial import (
    SistemaSensorial, TipoSensor, EstadoSensor, DispositivoSensor,
    FrameCapturado, AmostraAudio, QualidadeVideo, QualidadeAudio,
    ReconhecimentoVisual, AnaliseAudio
)
from .automacao import (
    AutomacaoInteligente, Tarefa, Workflow, Acao, Trigger,
    TipoAutomacao, EstadoTarefa, PrioridadeTarefa,
    TipoTrigger, TipoAcao, ExecucaoLog
)
from .leitor_pdf import (
    LeitorPDF, DocumentoPDF, PaginaPDF, MetadadosPDF,
    AnaliseConteudoPDF, TipoPDF, StatusProcessamento,
    extrair_texto_simples, baixar_e_extrair
)
from .arquitetura_organica import (
    ArquiteturaOrganica, NeuronioOrganico, Sinapse, CamadaCortical,
    AreaCortical, SistemaLimbico, Neurotransmissor,
    TipoNeuronio, TipoSinapse, EstadoNeurotransmissor
)
from .neurogenese_comunicacao import (
    NeurogeneseComunicacao, Neuroblasto, SinalNeural, GapJunction,
    AssemblyNeural, TrofismoNeural,
    FaseNeurogenese, TipoSinalNeural, FatorCrescimento
)
from .arquitetura_sistema import (
    ArquiteturaVhalinor, Componente, Modulo, Integracao,
    CamadaArquitetura, TipoComponente,
    arquitetura_vhalinor, obter_documentacao_arquitetura
)
from .processamento_linguagem import ProcessamentoLinguagem, ModeloLinguagem
from .visao_computacional import VisaoComputacional, TipoVisao
from .tomada_decisao import TomadaDecisao, TipoDecisao
from .metacognicao import Metacognicao, NivelMetacognicao

__all__ = [
    # Consciência Artificial
    'ConscienciaArtificial',
    'EstadoConsciencia',
    
    # Sentiência Artificial
    'SentienciaArtificial',
    'NivelSentiencia',
    'EstadoEmocional',
    'TipoQualia',
    
    # Raciocínio Avançado
    'RaciocinioAvancado',
    'TipoRaciocinio',
    
    # Memória Cognitiva
    'MemoriaCognitiva',
    'TipoMemoria',
    
    # Aprendizado Contínuo
    'AprendizadoContinuo',
    'EstrategiaAprendizado',
    
    # Aprendizado Profundo
    'AprendizadoProfundo',
    'ConfigDeepLearning',
    'ResultadoTreinamento',
    'ArquiteturaDeepLearning',
    'TipoOtimizacao',
    'LRScheduler',
    
    # Análise Profunda de Padrões
    'AnaliseProfundaPadroes',
    'PadraoDetectado',
    'CicloDetectado',
    'AnomaliaPadrao',
    'TipoPadrao',
    'FormacaoGrafica',
    'PadraoCandlestick',
    
    # Análise Quântica
    'AnaliseQuantica',
    'Qubit',
    'CircuitoQuantico',
    'ResultadoMedicao',
    'MetricasQuantica',
    'EstadoQubit',
    'TipoGate',
    'AlgoritmoQuantico',
    
    # Análise de Notícias
    'AnaliseNoticias',
    'Noticia',
    'EventoMercado',
    'TendenciaNoticias',
    'FonteNoticia',
    'CategoriaNoticia',
    'SentimentoNoticia',
    'ImpactoMercado',
    
    # Análise de Mercado Financeiro
    'AnaliseMercadoFinanceiro',
    'MetricaFundamentalista',
    'DadoMacroeconomico',
    'FluxoOrdem',
    'NivelBook',
    'AlertaRisco',
    'AnaliseSetor',
    'TipoAtivo',
    'TimeFrame',
    'IndicadorEconomico',
    'SentimentoInstitucional',
    
    # Análise Day Trade
    'AnaliseDayTrade',
    'NivelVolume',
    'SetupDayTrade',
    'SinalVWAP',
    'AnaliseLiquidez',
    'EstatisticasIntraday',
    'EstrategiaDayTrade',
    'MomentoDia',
    'TipoSetup',
    
    # Evolução de Aprendizado
    'EvolucaoAprendizado',
    'GenomaModelo',
    'FitnessSnapshot',
    'EventoEvolucao',
    'LinhagemModelo',
    'TipoEvolucao',
    'EstagioEvolucao',
    'TipoAdaptacao',
    
    # Sistema Sensorial
    'SistemaSensorial',
    'TipoSensor',
    'EstadoSensor',
    'DispositivoSensor',
    'FrameCapturado',
    'AmostraAudio',
    'QualidadeVideo',
    'QualidadeAudio',
    'ReconhecimentoVisual',
    'AnaliseAudio',
    
    # Automação Inteligente
    'AutomacaoInteligente',
    'Tarefa',
    'Workflow',
    'Acao',
    'Trigger',
    'TipoAutomacao',
    'EstadoTarefa',
    'PrioridadeTarefa',
    'TipoTrigger',
    'TipoAcao',
    'ExecucaoLog',
    
    # Leitor de PDFs
    'LeitorPDF',
    'DocumentoPDF',
    'PaginaPDF',
    'MetadadosPDF',
    'AnaliseConteudoPDF',
    'TipoPDF',
    'StatusProcessamento',
    
    # Arquitetura Orgânica (Cérebro Biológico)
    'ArquiteturaOrganica',
    'NeuronioOrganico',
    'Sinapse',
    'CamadaCortical',
    'AreaCortical',
    'SistemaLimbico',
    'Neurotransmissor',
    'TipoNeuronio',
    'TipoSinapse',
    'EstadoNeurotransmissor',
    
    # Neurogênese e Comunicação Neural
    'NeurogeneseComunicacao',
    'Neuroblasto',
    'SinalNeural',
    'GapJunction',
    'AssemblyNeural',
    'TrofismoNeural',
    'FaseNeurogenese',
    'TipoSinalNeural',
    'FatorCrescimento',
    
    # Arquitetura do Sistema
    'ArquiteturaVhalinor',
    'Componente',
    'Modulo',
    'Integracao',
    'CamadaArquitetura',
    'TipoComponente',
    'arquitetura_vhalinor',
    'obter_documentacao_arquitetura',
    
    # Processamento de Linguagem
    'ProcessamentoLinguagem',
    'ModeloLinguagem',
    
    # Visão Computacional
    'VisaoComputacional',
    'TipoVisao',
    
    # Tomada de Decisão
    'TomadaDecisao',
    'TipoDecisao',
    
    # Metacognição
    'Metacognicao',
    'NivelMetacognicao',
]
