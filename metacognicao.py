"""
VHALINOR Metacognição v6.0
============================
Sistema de metacognição com:
- Consciência dos próprios processos cognitivos
- Monitoramento do aprendizado
- Regulação estratégica
- Auto-avaliação
- Adaptação de estratégias

@module metacognicao
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from collections import deque


class NivelMetacognicao(Enum):
    """Níveis de metacognição"""
    INCONSCIENTE = "inconsciente"      # Sem consciência dos processos
    CONSCIENTE = "consciente"          # Consciência básica
    MONITORADO = "monitorado"          # Monitoramento ativo
    REGULADO = "regulado"              # Regulação ativa
    REFLEXIVO = "reflexivo"            # Reflexão profunda
    META_REFLEXIVO = "meta_reflexivo"  # Reflexão sobre a reflexão


@dataclass
class MonitorCognitivo:
    """Monitoramento de processo cognitivo"""
    processo: str
    inicio: str
    fim: Optional[str] = None
    sucesso: Optional[bool] = None
    dificuldades: List[str] = field(default_factory=list)
    estrategias_usadas: List[str] = field(default_factory=list)
    ajustes_realizados: List[Dict] = field(default_factory=list)


@dataclass
class Reflexao:
    """Registro de reflexão metacognitiva"""
    id: str
    tipo: str  # 'auto_avaliacao', 'planejamento', 'monitoramento', 'avaliacao'
    conteudo: str
    insights: List[str]
    acoes_sugeridas: List[str]
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Metacognicao:
    """
    Sistema de metacognição para auto-consciência e regulação.
    """
    
    def __init__(self, nivel_inicial: NivelMetacognicao = NivelMetacognicao.CONSCIENTE):
        self.nivel_atual = nivel_inicial
        self.processos_monitorados: Dict[str, MonitorCognitivo] = {}
        self.historico_reflexoes: deque = deque(maxlen=500)
        self.estrategias_efetivas: Dict[str, float] = {}
        self.padroes_aprendizado: Dict[str, Any] = {}
        
        # Auto-conhecimento
        self.pontos_fortes: List[str] = []
        self.pontos_fracos: List[str] = []
        self.preferencias_estrategicas: Dict[str, Any] = {}
        
        # Métricas
        self.taxa_acerto_estimada = 0.7
        self.confiança_calibrada = 0.5
        self.bias_conhecidos: List[str] = []
    
    def iniciar_monitoramento(self, processo_id: str, descricao: str) -> str:
        """Iniciar monitoramento de processo cognitivo"""
        monitor = MonitorCognitivo(
            processo=descricao,
            inicio=datetime.now(timezone.utc).isoformat()
        )
        
        self.processos_monitorados[processo_id] = monitor
        
        # Registrar reflexão
        self._registrar_reflexao(
            'monitoramento',
            f"Iniciando monitoramento: {descricao}",
            [f"Processo {processo_id} sob observação"]
        )
        
        return processo_id
    
    def finalizar_monitoramento(
        self,
        processo_id: str,
        sucesso: bool,
        dificuldades: Optional[List[str]] = None
    ):
        """Finalizar monitoramento e avaliar"""
        if processo_id not in self.processos_monitorados:
            return
        
        monitor = self.processos_monitorados[processo_id]
        monitor.fim = datetime.now(timezone.utc).isoformat()
        monitor.sucesso = sucesso
        monitor.dificuldades = dificuldades or []
        
        # Auto-avaliação
        self._avaliar_processo(monitor)
        
        # Atualizar conhecimento sobre estratégias
        for estrategia in monitor.estrategias_usadas:
            if estrategia not in self.estrategias_efetivas:
                self.estrategias_efetivas[estrategia] = 0.5
            
            # Atualizar efetividade
            delta = 0.1 if sucesso else -0.1
            self.estrategias_efetivas[estrategia] += delta
            self.estrategias_efetivas[estrategia] = max(0.0, min(1.0, self.estrategias_efetivas[estrategia]))
    
    def _avaliar_processo(self, monitor: MonitorCognitivo):
        """Realizar auto-avaliação do processo"""
        insights = []
        acoes = []
        
        if monitor.sucesso:
            insights.append("Processo concluído com sucesso")
            
            # Identificar estratégias efetivas
            if monitor.estrategias_usadas:
                melhor_estrategia = max(
                    monitor.estrategias_usadas,
                    key=lambda e: self.estrategias_efetivas.get(e, 0.5)
                )
                insights.append(f"Estratégia '{melhor_estrategia}' foi efetiva")
        else:
            insights.append("Processo enfrentou dificuldades")
            
            # Analisar dificuldades
            if monitor.dificuldades:
                insights.append(f"Dificuldades identificadas: {', '.join(monitor.dificuldades)}")
                acoes.append("Revisar estratégias para próxima tentativa")
        
        # Identificar padrões
        if 'tempo_excessivo' in monitor.dificuldades:
            self.pontos_fracos.append('gestao_tempo')
            acoes.append("Melhorar estimativa de tempo")
        
        self._registrar_reflexao('avaliacao', "Auto-avaliação do processo", insights, acoes)
    
    def _registrar_reflexao(
        self,
        tipo: str,
        conteudo: str,
        insights: List[str],
        acoes: Optional[List[str]] = None
    ):
        """Registrar reflexão metacognitiva"""
        reflexao = Reflexao(
            id=f"ref_{len(self.historico_reflexoes)}",
            tipo=tipo,
            conteudo=conteudo,
            insights=insights,
            acoes_sugeridas=acoes or []
        )
        
        self.historico_reflexoes.append(reflexao)
    
    def planejar_abordagem(
        self,
        objetivo: str,
        contexto: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Planejar abordagem baseada em metacognição"""
        insights = []
        estrategias_sugeridas = []
        
        # Analisar contexto
        complexidade = contexto.get('complexidade', 'media')
        prazo = contexto.get('prazo', 'normal')
        
        # Selecionar estratégias baseado em histórico
        estrategias_ordenadas = sorted(
            self.estrategias_efetivas.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        for estrategia, efetividade in estrategias_ordenadas[:3]:
            estrategias_sugeridas.append({
                'nome': estrategia,
                'efetividade_historica': efetividade,
                'racional': f"Efetividade histórica de {efetividade:.1%}"
            })
        
        # Considerar pontos fracos
        if 'gestao_tempo' in self.pontos_fracos and prazo == 'curto':
            insights.append("Alerta: Prazo curto com histórico de dificuldade com tempo")
            estrategias_sugeridas.append({
                'nome': 'dividir_conquistas',
                'efetividade_historica': 0.7,
                'racional': 'Mitigar risco de tempo'
            })
        
        # Calibrar confiança
        if self.nivel_atual.value in ['reflexivo', 'meta_reflexivo']:
            confianca_planejamento = min(0.9, self.confiança_calibrada + 0.1)
        else:
            confianca_planejamento = self.confiança_calibrada
        
        plano = {
            'objetivo': objetivo,
            'estrategias': estrategias_sugeridas,
            'riscos_identificados': [],
            'pontos_atencao': insights,
            'monitoramento_sugerido': True,
            'checkpoints': [
                '25% - Verificação inicial',
                '50% - Avaliação de progresso',
                '75% - Preparação para finalização',
                '100% - Auto-avaliação'
            ],
            'confianca': confianca_planejamento
        }
        
        self._registrar_reflexao(
            'planejamento',
            f"Planejamento para: {objetivo}",
            insights,
            [e['nome'] for e in estrategias_sugeridas]
        )
        
        return plano
    
    def calibrar_confiança(
        self,
        predicao_feita: Any,
        resultado_real: Any,
        confianca_declarada: float
    ) -> Dict[str, float]:
        """Calibrar estimativa de confiança"""
        # Verificar se predição foi correta
        correto = (predicao_feita == resultado_real)
        
        # Análise de calibração
        if correto and confianca_declarada < 0.7:
            # Subconfiança
            ajuste = 0.05
            insight = "Possível subconfiança detectada"
        elif not correto and confianca_declarada > 0.8:
            # Superconfiança
            ajuste = -0.1
            insight = "Superconfiança detectada - ajustar estimativas"
        else:
            ajuste = 0.0
            insight = "Calibração adequada"
        
        # Aplicar ajuste suavizado
        self.confiança_calibrada += ajuste * 0.3
        self.confiança_calibrada = max(0.3, min(0.95, self.confiança_calibrada))
        
        # Atualizar taxa de acerto estimada
        alpha = 0.1
        self.taxa_acerto_estimada += alpha * (1.0 if correto else 0.0 - self.taxa_acerto_estimada)
        
        self._registrar_reflexao(
            'calibracao',
            f"Calibração de confiança: predição {'correta' if correto else 'incorreta'}",
            [insight, f"Confiança ajustada para {self.confiança_calibrada:.1%}"]
        )
        
        return {
            'confianca_calibrada': self.confiança_calibrada,
            'taxa_acerto_estimada': self.taxa_acerto_estimada,
            'direcao_ajuste': ajuste,
            'bem_calibrado': abs(self.taxa_acerto_estimada - confianca_declarada) < 0.15
        }
    
    def identificar_bias(self, contexto: Dict[str, Any]) -> List[str]:
        """Identificar potenciais vieses cognitivos"""
        vieses_detectados = []
        
        # Analisar padrões de decisão
        if contexto.get('recent_successes', 0) > 5:
            vieses_detectados.append('viés_otimismo')
        
        if contexto.get('recent_failures', 0) > 3:
            vieses_detectados.append('viés_pessimismo')
        
        if contexto.get('primeira_impressao'):
            vieses_detectados.append('efeito_ancoragem')
        
        if contexto.get('informacao_recente'):
            vieses_detectados.append('viés_recencia')
        
        # Registrar
        if vieses_detectados:
            self.bias_conhecidos.extend(vieses_detectados)
            self._registrar_reflexao(
                'identificacao_vies',
                f"Vieses detectados: {', '.join(vieses_detectados)}",
                ["Consciência de vieses é o primeiro passo para mitigá-los"],
                ["Aplicar técnicas de de-biasing"]
            )
        
        return vieses_detectados
    
    def sugerir_melhoria(self, area: Optional[str] = None) -> Dict[str, Any]:
        """Sugerir melhorias baseadas em metacognição"""
        sugestoes = []
        
        if not area or area == 'estrategias':
            # Identificar estratégias pouco efetivas
            estrategias_fracas = [
                e for e, ef in self.estrategias_efetivas.items()
                if ef < 0.5
            ]
            if estrategias_fracas:
                sugestoes.append({
                    'area': 'estrategias',
                    'problema': f"Estratégias com baixa efetividade: {', '.join(estrategias_fracas)}",
                    'sugestao': "Considerar substituir ou adaptar essas estratégias"
                })
        
        if not area or area == 'conhecimento':
            # Identificar lacunas
            if len(self.pontos_fracos) > len(self.pontos_fortes):
                sugestoes.append({
                    'area': 'conhecimento',
                    'problema': "Mais pontos fracos que fortes identificados",
                    'sugestao': "Focar em desenvolver competências nas áreas de dificuldade"
                })
        
        if not area or area == 'calibracao':
            if abs(self.taxa_acerto_estimada - self.confiança_calibrada) > 0.2:
                sugestoes.append({
                    'area': 'calibracao',
                    'problema': f"Descalibracao detectada: acerto={self.taxa_acerto_estimada:.1%}, confiança={self.confiança_calibrada:.1%}",
                    'sugestao': "Praticar mais exercícios de calibragem de confiança"
                })
        
        return {
            'sugestoes': sugestoes,
            'total': len(sugestoes),
            'prioridade': 'alta' if sugestoes else 'normal'
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status da metacognição"""
        return {
            'nivel_atual': self.nivel_atual.value,
            'processos_monitorados': len(self.processos_monitorados),
            'reflexoes_registradas': len(self.historico_reflexoes),
            'estrategias_mapeadas': len(self.estrategias_efetivas),
            'confianca_calibrada': self.confiança_calibrada,
            'taxa_acerto_estimada': self.taxa_acerto_estimada,
            'pontos_fortes': len(self.pontos_fortes),
            'pontos_fracos': len(self.pontos_fracos),
            'bias_conhecidos': len(self.bias_conhecidos)
        }
