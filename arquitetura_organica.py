"""
VHALINOR Arquitetura Orgânica v6.0
====================================
Sistema de arquitetura orgânica biologicamente inspirada para ai_geral:
- Neurônios orgânicos simulados com neurotransmissores
- Sinapses plásticas (Long Term Potentiation/Depression)
- Redes neurais de terceira ordem (cortex-like)
- Sistemas límbico e cortical
- Neuroplasticidade e pruning sináptico
- Ritmos circadianos e homeostase
- Emoções como estados neuroquímicos
- Memória de trabalho e consolidação
- Sistema glial de suporte
- Neurogênese (nascimento de novos neurônios)

@module arquitetura_organica
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable, Set
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from collections import deque, defaultdict
import random
import math
import threading
import time


class TipoNeuronio(Enum):
    """Tipos de neurônios biológicos simulados"""
    PIRAMIDAL = "piramidal"           # Neurônios piramidais (córtex)
    INTERNEURONIO = "interneuronio"   # Inibitórios
    GRANULAR = "granular"             # Granular cells
    ASTROGLIA = "astroglia"           # Células gliais (suporte)
    Oligodendrocito = "oligodendrocito"  # Mielina
    DOPAMINERGICO = "dopaminergico"    # Neurotransmissor: dopamina
    SEROTONINERGICO = "serotoninergico"  # Neurotransmissor: serotonina
    NORADRENERGICO = "noradrenergico"  # Neurotransmissor: noradrenalina
    COLINERGICO = "colinergico"       # Neurotransmissor: acetilcolina
    GABAERGICO = "gabaergico"         # Neurotransmissor: GABA (inibitório)
    GLUTAMATERGICO = "glutamatergico"  # Neurotransmissor: glutamato (excitatório)


class TipoSinapse(Enum):
    """Tipos de sinapses"""
    AXODENDRITICA = "axodendritica"   # Axônio -> dendrito (mais comum)
    AXOSSOMATICA = "axossomatica"     # Axônio -> soma
    AXOAXONICA = "axoaxonica"         # Axônio -> axônio
    DENDRODENDRITICA = "dendrodendritica"  # Dendrito -> dendrito
    ELETTRICA = "eletrica"            # Gap junction (direta)


class EstadoNeurotransmissor(Enum):
    """Estados de neurotransmissores"""
    BAIXO = "baixo"
    NORMAL = "normal"
    ELEVADO = "elevado"
    CRITICO = "critico"


@dataclass
class Neurotransmissor:
    """Concentração de neurotransmissor"""
    tipo: str  # "dopamina", "serotonina", "noradrenalina", "acetilcolina", "GABA", "glutamato"
    nivel: float  # 0.0 a 1.0
    taxa_sintese: float = 0.01
    taxa_reuptake: float = 0.05
    receptores_ativos: int = 0
    
    def atualizar(self, estimulo: float = 0.0):
        """Atualizar nível de neurotransmissor"""
        # Síntese natural + estimulo - reuptake
        self.nivel += self.taxa_sintese + estimulo * 0.1
        self.nivel -= self.nivel * self.taxa_reuptake
        self.nivel = max(0.0, min(1.0, self.nivel))
    
    @property
    def estado(self) -> EstadoNeurotransmissor:
        if self.nivel < 0.2:
            return EstadoNeurotransmissor.BAIXO
        elif self.nivel < 0.4:
            return EstadoNeurotransmissor.NORMAL
        elif self.nivel < 0.7:
            return EstadoNeurotransmissor.ELEVADO
        else:
            return EstadoNeurotransmissor.CRITICO


@dataclass
class Sinapse:
    """Sinapse biológica entre neurônios"""
    id: str
    pre_id: str  # ID do neurônio pré-sináptico
    pos_id: str  # ID do neurônio pós-sináptico
    tipo: TipoSinapse
    peso: float  # Força da conexão (0.0 a 1.0)
    peso_original: float = field(default=0.0)  # Para LTP/LTD
    neurotransmissor: str = "glutamato"
    
    # Plasticidade
    ultima_ativacao: float = 0.0
    frequencia_ativacao: deque = field(default_factory=lambda: deque(maxlen=100))
    
    # LTP/LTD (Long Term Potentiation/Depression)
    potenciacao_longo_prazo: float = 1.0
    depressao_longo_prazo: float = 1.0
    
    def __post_init__(self):
        if self.peso_original == 0.0:
            self.peso_original = self.peso
    
    def ativar(self, forca: float):
        """Ativar a sinapse"""
        self.ultima_ativacao = time.time()
        self.frequencia_ativacao.append(forca)
        
        # Hebbian learning: "neurons that fire together, wire together"
        if len(self.frequencia_ativacao) >= 10:
            media_recente = np.mean(list(self.frequencia_ativacao)[-10:])
            
            # LTP: fortalecer se ativação frequente
            if media_recente > 0.7:
                self.potenciacao_longo_prazo = min(2.0, self.potenciacao_longo_prazo + 0.01)
            # LTD: enfraquecer se ativação rara
            elif media_recente < 0.3:
                self.depressao_longo_prazo = max(0.5, self.depressao_longo_prazo - 0.01)
        
        # Peso efetivo inclui plasticidade
        peso_efetivo = self.peso * self.potenciacao_longo_prazo * self.depressao_longo_prazo
        return forca * peso_efetivo
    
    @property
    def forca_efetiva(self) -> float:
        return self.peso * self.potenciacao_longo_prazo * self.depressao_longo_prazo
    
    def aplicar_pruning(self, threshold: float = 0.1) -> bool:
        """Aplicar pruning sináptico se muito fraca"""
        return self.forca_efetiva < threshold


@dataclass
class NeuronioOrganico:
    """Neurônio biologicamente inspirado"""
    id: str
    tipo: TipoNeuronio
    posicao_3d: Tuple[float, float, float]  # Coordenadas no espaço cortical
    
    # Estado elétrico
    potencial_membrana: float = -70.0  # mV (potencial de repouso)
    limiar_disparo: float = -55.0  # mV
    esta_refrataria: bool = False
    tempo_refrataria: float = 0.002  # 2ms
    ultimo_disparo: float = 0.0
    
    # Conectividade
    dendritos: List[str] = field(default_factory=list)  # IDs de sinapses de entrada
    axonio: List[str] = field(default_factory=list)  # IDs de sinapses de saída
    
    # Metabolismo
    energia: float = 1.0  # ATP disponível (0-1)
    oxigenio: float = 1.0  # O2 disponível
    
    # Plasticidade estrutural
    idade: int = 0  # Tempo de vida em ciclos
    taxa_mortalidade: float = 0.0001  # Chance de apoptose
    
    # Neurotransmissores produzidos
    neurotransmissores_produzidos: List[str] = field(default_factory=list)
    
    def receber_sinal(self, forca: float, neurotransmissor: str) -> bool:
        """Receber sinal sináptico"""
        if self.esta_refrataria:
            return False
        
        # Neurotransmissores afetam o potencial de membrana
        if neurotransmissor in ["glutamato"]:
            self.potencial_membrana += forca * 5  # Excitatório
        elif neurotransmissor in ["GABA"]:
            self.potencial_membrana -= forca * 3  # Inibitório
        elif neurotransmissor in ["dopamina"]:
            # Dopamina modula plasticidade (não muda Vm diretamente)
            pass
        elif neurotransmissor in ["acetilcolina"]:
            self.potencial_membrana += forca * 2  # Modulação
        
        # Verificar se atingiu limiar
        if self.potencial_membrana >= self.limiar_disparo:
            return self.disparar()
        
        return False
    
    def disparar(self) -> bool:
        """Potencial de ação!"""
        if self.energia < 0.1:
            return False  # Sem energia
        
        self.ultimo_disparo = time.time()
        self.esta_refrataria = True
        self.potencial_membrana = -75.0  # Hiperpolarização após disparo
        self.energia -= 0.05  # Gasto energético
        
        # Reset refratariedade após tempo
        def reset_refrataria():
            time.sleep(self.tempo_refrataria)
            self.esta_refrataria = False
            self.potencial_membrana = -70.0  # Voltar ao repouso
        
        threading.Thread(target=reset_refrataria, daemon=True).start()
        
        return True
    
    def atualizar_metabolismo(self):
        """Atualizar estado metabólico"""
        # Recuperação de energia (limitada)
        self.energia = min(1.0, self.energia + 0.01)
        self.oxigenio = min(1.0, self.oxigenio + 0.01)
        
        # Envelhecimento
        self.idade += 1
    
    @property
    def ativo(self) -> bool:
        """Se o neurônio está funcional"""
        return self.energia > 0.1 and self.oxigenio > 0.1


@dataclass
class CamadaCortical:
    """Camada do córtex cerebral"""
    numero: int  # 1-6 (camadas do neocórtex)
    nome: str
    neuronios: List[str] = field(default_factory=list)  # IDs
    funcao_principal: str = ""
    
    # Características
    densidade_neuronal: float = 0.0  # Neurônios por unidade de volume
    espessura: float = 0.0  # mm


@dataclass
class AreaCortical:
    """Área funcional do córtex (como áreas de Brodmann)"""
    id: str
    nome: str
    funcao: str  # "sensorial", "motora", "associativa", "executiva"
    camadas: List[CamadaCortical] = field(default_factory=list)
    conexoes_afferentes: List[str] = field(default_factory=list)  # Entradas
    conexoes_efferentes: List[str] = field(default_factory=list)  # Saídas
    especializacao: str = ""  # e.g., "processamento_visual", "linguagem"


@dataclass
class SistemaLimbico:
    """Sistema límbico emocional"""
    amigdala: Dict[str, Any] = field(default_factory=dict)  # Medo/emocções
    hipocampo: Dict[str, Any] = field(default_factory=dict)  # Memória
    hipotalamo: Dict[str, Any] = field(default_factory=dict)  # Homeostase
    cingulado: Dict[str, Any] = field(default_factory=dict)  # Emoção/regulação
    
    def processar_emocao(self, estimulo: Dict[str, Any]) -> Dict[str, float]:
        """Processar resposta emocional"""
        intensidade = estimulo.get("intensidade", 0.5)
        valencia = estimulo.get("valencia", 0)  # -1 (negativo) a +1 (positivo)
        
        # Amigdala: detecção de ameaça
        ameaca = intensidade if valencia < 0 else 0.0
        
        # Hipocampo: contexto de memória
        memoria_contexto = self.hipocampo.get("contexto_recente", [])
        
        return {
            "medo": min(1.0, ameaca * 1.2),
            "ansiedade": min(1.0, ameaca * 0.8),
            "excitacao": min(1.0, intensidade),
            "prazer": max(0.0, valencia * intensidade)
        }


class ArquiteturaOrganica:
    """
    Cérebro orgânico biologicamente inspirado da VHALINOR ai_geral.
    
    Simula arquitetura neural biológica com:
    - Redes de neurônios com propriedades biofísicas
    - Plasticidade sináptica (LTP/LTD)
    - Sistemas límbico e cortical
    - Homeostase e metabolismo neural
    - Neurogênese e pruning
    - Neurotransmissores e modulação
    """
    
    def __init__(self, num_neuronios_inicial: int = 10000):
        self.nome = "VHALINOR Cérebro Orgânico"
        self.versao = "6.0.0"
        
        # Componentes neurais
        self.neuronios: Dict[str, NeuronioOrganico] = {}
        self.sinapses: Dict[str, Sinapse] = {}
        self.neurotransmissores_globais: Dict[str, Neurotransmissor] = {
            "dopamina": Neurotransmissor("dopamina", 0.3),
            "serotonina": Neurotransmissor("serotonina", 0.4),
            "noradrenalina": Neurotransmissor("noradrenalina", 0.2),
            "acetilcolina": Neurotransmissor("acetilcolina", 0.5),
            "GABA": Neurotransmissor("GABA", 0.6),
            "glutamato": Neurotransmissor("glutamato", 0.7)
        }
        
        # Estruturas macro
        self.areas_corticais: Dict[str, AreaCortical] = {}
        self.sistema_limbico = SistemaLimbico()
        
        # Memória
        self.memoria_trabalho: deque = deque(maxlen=7)  # 7±2 itens (Miller's law)
        self.memoria_curto_prazo: Dict[str, Any] = {}
        self.memoria_longo_prazo: Dict[str, Any] = {}
        self.memoria_episodica: deque = deque(maxlen=100)  # Eventos
        
        # Ritmos e homeostase
        self.ritmo_circadiano = 0.5  # 0-1 ciclo dia/noite
        self.hora_simulada = 8.0  # Hora do dia
        self.homeostase = {
            "energia_global": 1.0,
            "temperatura": 37.0,
            "ph": 7.4,
            "oxigenacao": 1.0
        }
        
        # Parâmetros de funcionamento
        self.taxa_neurogenese = 0.001  # Novos neurônios por ciclo
        self.taxa_pruning = 0.0005  # Sinapses eliminadas por ciclo
        self.ciclo_atual = 0
        
        # Histórico
        self.historico_ativacao: deque = deque(maxlen=1000)
        self.padroes_disparo: Dict[str, List[float]] = defaultdict(list)
        
        # Thread de atualização
        self._executando = False
        self._thread_atualizacao: Optional[threading.Thread] = None
        
        # Inicializar estruturas
        self._inicializar_cortex()
        self._criar_neuronios_iniciais(num_neuronios_inicial)
        
        # Métricas
        self.total_disparos = 0
        self.total_sinapses_criadas = 0
        self.total_sinapses_eliminadas = 0
        self.total_neuronios_nascidos = 0
        self.total_neuronios_mortos = 0
    
    def _inicializar_cortex(self):
        """Inicializar áreas corticais"""
        areas = [
            ("V1", "Córtex Visual Primário", "sensorial", "processamento_visual"),
            ("A1", "Córtex Auditivo Primário", "sensorial", "processamento_auditivo"),
            ("S1", "Córtex Somatossensorial", "sensorial", "processamento_tatil"),
            ("M1", "Córtex Motor Primário", "motora", "planejamento_motor"),
            ("PFC", "Córtex Pré-Frontal", "executiva", "cognicao_superior"),
            ("TPJ", "Junção Temporo-Parietal", "associativa", "atencao_social"),
        ]
        
        for id_area, nome, funcao, especializacao in areas:
            # Criar 6 camadas corticais
            camadas = []
            for i in range(1, 7):
                nomes_camadas = {
                    1: "Molecular (I)",
                    2: "Externa Granular (II)",
                    3: "Externa Piramidal (III)",
                    4: "Interna Granular (IV)",
                    5: "Interna Piramidal (V)",
                    6: "Multiforme (VI)"
                }
                camada = CamadaCortical(
                    numero=i,
                    nome=nomes_camadas.get(i, f"Camada {i}"),
                    funcao_principal="" if i in [1, 4] else "integracao" if i in [2, 3] else "projecao"
                )
                camadas.append(camada)
            
            area = AreaCortical(
                id=id_area,
                nome=nome,
                funcao=funcao,
                camadas=camadas,
                especializacao=especializacao
            )
            
            self.areas_corticais[id_area] = area
    
    def _criar_neuronios_iniciais(self, n: int):
        """Criar população inicial de neurônios"""
        tipos_dist = {
            TipoNeuronio.PIRAMIDAL: 0.7,
            TipoNeuronio.INTERNEURONIO: 0.2,
            TipoNeuronio.GRANULAR: 0.1
        }
        
        for i in range(n):
            # Sortear tipo
            r = random.random()
            tipo = TipoNeuronio.PIRAMIDAL
            acum = 0
            for t, p in tipos_dist.items():
                acum += p
                if r <= acum:
                    tipo = t
                    break
            
            # Posição 3D aleatória (córtex tem ~2-4mm de espessura)
            posicao = (
                random.uniform(0, 100),  # x (lateralidade)
                random.uniform(0, 100),  # y (anterior-posterior)
                random.uniform(0, 4)     # z (espessura cortical em mm)
            )
            
            neuronio = NeuronioOrganico(
                id=f"neu_{i:06d}",
                tipo=tipo,
                posicao_3d=posicao,
                potencial_membrana=-70.0 + random.uniform(-5, 5)
            )
            
            self.neuronios[neuronio.id] = neuronio
    
    def criar_sinapse(
        self,
        pre_id: str,
        pos_id: str,
        peso_inicial: Optional[float] = None
    ) -> Optional[str]:
        """Criar nova sinapse entre neurônios"""
        if pre_id not in self.neuronios or pos_id not in self.neuronios:
            return None
        
        sin_id = f"syn_{pre_id}_{pos_id}_{len(self.sinapses)}"
        
        # Peso inicial aleatório ou especificado
        if peso_inicial is None:
            peso_inicial = random.uniform(0.01, 0.5)
        
        # Determinar tipo de sinapse baseado na distância
        pre = self.neuronios[pre_id]
        pos = self.neuronios[pos_id]
        
        dist = math.sqrt(
            (pre.posicao_3d[0] - pos.posicao_3d[0])**2 +
            (pre.posicao_3d[1] - pos.posicao_3d[1])**2 +
            (pre.posicao_3d[2] - pos.posicao_3d[2])**2
        )
        
        tipo_sinapse = TipoSinapse.AXODENDRITICA if dist < 50 else TipoSinapse.AXOAXONICA
        
        # Determinar neurotransmissor baseado nos tipos
        if pre.tipo == TipoNeuronio.GABAERGICO:
            neurotransmissor = "GABA"
        elif pre.tipo == TipoNeuronio.DOPAMINERGICO:
            neurotransmissor = "dopamina"
        elif pre.tipo == TipoNeuronio.COLINERGICO:
            neurotransmissor = "acetilcolina"
        else:
            neurotransmissor = "glutamato"
        
        sinapse = Sinapse(
            id=sin_id,
            pre_id=pre_id,
            pos_id=pos_id,
            tipo=tipo_sinapse,
            peso=peso_inicial,
            neurotransmissor=neurotransmissor
        )
        
        self.sinapses[sin_id] = sinapse
        
        # Registrar nos neurônios
        pre.axonio.append(sin_id)
        pos.dendritos.append(sin_id)
        
        self.total_sinapses_criadas += 1
        
        return sin_id
    
    def propagar_sinal(self, neuronio_id: str, forca: float = 1.0) -> List[str]:
        """Propagar sinal neural através das sinapses"""
        if neuronio_id not in self.neuronios:
            return []
        
        neuronio = self.neuronios[neuronio_id]
        
        # Tentar disparar
        if not neuronio.disparar():
            return []
        
        self.total_disparos += 1
        
        # Propagar para sinapses de saída
        neuronios_ativados = []
        
        for sin_id in neuronio.axonio:
            if sin_id in self.sinapses:
                sinapse = self.sinapses[sin_id]
                
                # Ativar sinapse
                forca_transmitida = sinapse.ativar(forca)
                
                # Receber no neurônio pós-sináptico
                pos_neu = self.neuronios[sinapse.pos_id]
                disparou = pos_neu.receber_sinal(
                    forca_transmitida,
                    sinapse.neurotransmissor
                )
                
                if disparou:
                    neuronios_ativados.append(sinapse.pos_id)
                    # Propagar recursivamente (com limite de profundidade)
                    # Aqui poderia ter limite para evitar explosão
        
        return neuronios_ativados
    
    def processar_entrada_sensorial(self, dados_sensoriais: Dict[str, Any]) -> Dict[str, Any]:
        """Processar entrada sensorial através do córtex"""
        tipo_sensorial = dados_sensoriais.get("tipo", "generico")
        intensidade = dados_sensoriais.get("intensidade", 0.5)
        
        # Selecionar área cortical apropriada
        mapeamento_areas = {
            "visual": "V1",
            "auditivo": "A1",
            "tatil": "S1",
            "motor": "M1",
            "cognitivo": "PFC"
        }
        
        area_id = mapeamento_areas.get(tipo_sensorial, "PFC")
        area = self.areas_corticais.get(area_id)
        
        if not area:
            return {"sucesso": False, "erro": "Área não encontrada"}
        
        # Ativar neurônios da área (simulação simplificada)
        neuronios_ativados = []
        if area.camadas:
            # Ativar camada granular (IV) para input
            camada_input = area.camadas[3] if len(area.camadas) > 3 else area.camadas[0]
            
            for neu_id in camada_input.neuronios[:100]:  # Limitar para performance
                if neu_id in self.neuronios:
                    ativados = self.propagar_sinal(neu_id, intensidade)
                    neuronios_ativados.extend(ativados)
        
        # Processar emoção no sistema límbico
        resposta_emocional = self.sistema_limbico.processar_emocao({
            "intensidade": intensidade,
            "valencia": dados_sensoriais.get("valencia", 0)
        })
        
        # Atualizar neurotransmissores
        for nome, nt in self.neurotransmissores_globais.items():
            if nome in resposta_emocional:
                nt.atualizar(resposta_emocional[nome])
            else:
                nt.atualizar(0.01)
        
        # Registrar na memória de trabalho
        self.memoria_trabalho.append({
            "tipo": tipo_sensorial,
            "intensidade": intensidade,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        return {
            "sucesso": True,
            "area_processada": area_id,
            "neuronios_ativados": len(neuronios_ativados),
            "resposta_emocional": resposta_emocional,
            "neurotransmissores": {k: v.nivel for k, v in self.neurotransmissores_globais.items()}
        }
    
    def ciclo_manutencao(self):
        """Executar ciclo de manutenção orgânica"""
        self.ciclo_atual += 1
        
        # 1. Atualizar metabolismo de todos os neurônios
        for neuronio in self.neuronios.values():
            neuronio.atualizar_metabolismo()
        
        # 2. Pruning sináptico (podar conexões fracas)
        sinapses_para_remover = []
        for sin_id, sinapse in self.sinapses.items():
            if sinapse.aplicar_pruning(threshold=0.05):
                sinapses_para_remover.append(sin_id)
        
        for sin_id in sinapses_para_remover:
            del self.sinapses[sin_id]
            self.total_sinapses_eliminadas += 1
        
        # 3. Neurogênese (criar novos neurônios raramente)
        if random.random() < self.taxa_neurogenese:
            self._criar_neuronios_iniciais(1)
            self.total_neuronios_nascidos += 1
        
        # 4. Apoptose (morte celular programada)
        neuronios_para_remover = []
        for neu_id, neuronio in self.neuronios.items():
            if neuronio.idade > 10000 and random.random() < neuronio.taxa_mortalidade:
                if neuronio.energia < 0.1:  # Neurônios debilitados
                    neuronios_para_remover.append(neu_id)
        
        for neu_id in neuronios_para_remover:
            # Remover sinapses conectadas
            neuronio = self.neuronios[neu_id]
            for sin_id in neuronio.dendritos + neuronio.axonio:
                if sin_id in self.sinapses:
                    del self.sinapses[sin_id]
            del self.neuronios[neu_id]
            self.total_neuronios_mortos += 1
        
        # 5. Atualizar ritmo circadiano
        self.hora_simulada = (self.hora_simulada + 0.1) % 24
        # Ciclo: baixa atividade de 23-5h, alta de 8-20h
        if 23 <= self.hora_simulada or self.hora_simulada < 5:
            self.ritmo_circadiano = 0.2
        elif 8 <= self.hora_simulada < 20:
            self.ritmo_circadiano = 0.9
        else:
            self.ritmo_circadiano = 0.6
        
        # 6. Consolidação de memória (de curto para longo prazo)
        if self.ciclo_atual % 100 == 0:  # A cada 100 ciclos
            self._consolidar_memorias()
    
    def _consolidar_memorias(self):
        """Transferir memórias de curto para longo prazo"""
        # Simplificação: alguns itens da memória de trabalho vão para LTP
        while len(self.memoria_trabalho) > 5:
            item = self.memoria_trabalho.popleft()
            chave = f"mem_{hash(str(item)) % 10000}"
            self.memoria_longo_prazo[chave] = {
                **item,
                "consolidado_em": datetime.now(timezone.utc).isoformat()
            }
    
    def iniciar_ciclo_autonomo(self, intervalo_segundos: float = 1.0):
        """Iniciar ciclo de manutenção contínua"""
        if self._executando:
            return False
        
        self._executando = True
        
        def loop_manutencao():
            while self._executando:
                self.ciclo_manutencao()
                time.sleep(intervalo_segundos)
        
        self._thread_atualizacao = threading.Thread(target=loop_manutencao, daemon=True)
        self._thread_atualizacao.start()
        
        return True
    
    def parar_ciclo_autonomo(self):
        """Parar ciclo de manutenção"""
        self._executando = False
        if self._thread_atualizacao:
            self._thread_atualizacao.join(timeout=2.0)
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status da arquitetura orgânica"""
        # Calcular métricas
        num_neuronios = len(self.neuronios)
        num_sinapses = len(self.sinapses)
        
        # Densidade sináptica média
        densidade = num_sinapses / max(1, num_neuronios)
        
        # Atividade recente
        atividade_recente = self.total_disparos / max(1, self.ciclo_atual)
        
        # Homeostase geral
        homeostase_media = np.mean([
            self.homeostase["energia_global"],
            self.homeostase["oxigenacao"]
        ])
        
        return {
            "nome": self.nome,
            "versao": self.versao,
            "populacao": {
                "neuronios": num_neuronios,
                "sinapses": num_sinapses,
                "densidade_sinaptica": round(densidade, 2),
                "neuronios_nascidos": self.total_neuronios_nascidos,
                "neuronios_mortos": self.total_neuronios_mortos,
                "sinapses_criadas": self.total_sinapses_criadas,
                "sinapses_eliminadas": self.total_sinapses_eliminadas
            },
            "atividade": {
                "total_disparos": self.total_disparos,
                "ciclo_atual": self.ciclo_atual,
                "atividade_media": round(atividade_recente, 2),
                "ritmo_circadiano": round(self.ritmo_circadiano, 2),
                "hora_simulada": round(self.hora_simulada, 1)
            },
            "neuroquimica": {
                nome: {
                    "nivel": round(nt.nivel, 3),
                    "estado": nt.estado.value
                }
                for nome, nt in self.neurotransmissores_globais.items()
            },
            "memoria": {
                "trabalho": len(self.memoria_trabalho),
                "curto_prazo": len(self.memoria_curto_prazo),
                "longo_prazo": len(self.memoria_longo_prazo)
            },
            "homeostase": {
                k: round(v, 3) for k, v in self.homeostase.items()
            },
            "homeostase_geral": round(homeostase_media, 2),
            "areas_corticais": len(self.areas_corticais),
            "ciclo_autonomo_ativo": self._executando
        }
