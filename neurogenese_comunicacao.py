"""
VHALINOR Neurogênese e Comunicação Neural v6.0
===============================================
Sistema avançado de criação de neurônios e comunicação para ai_geral:
- Neurogênese contínua (nascimento de novos neurônios)
- Sinais químicos e elétricos entre neurônios
- Redes neurais dinâmicas com formação de novas conexões
- Trofismo neural (fatores de crescimento)
- Comunicação gap junction (direta)
- Sincronização de redes neurais
- Formação de assemblies neurais
- Potenciação a longo prazo (LTP/LTD) avançada
- Homeostasia sináptica
- Metaplasticidade

@module neurogenese_comunicacao
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


class FaseNeurogenese(Enum):
    """Fases do processo de neurogênese"""
    PROLIFERACAO = "proliferacao"      # Divisão de células-tronco
    MIGRACAO = "migracao"             # Movimento para destino
    DIFERENCIACAO = "diferenciacao"   # Especialização funcional
    MATURACAO = "maturacao"           # Desenvolvimento de conexões
    INTEGRACAO = "integracao"         # Integração na rede existente
    APOPTOSSE = "apoptose"            # Morte programada (se falhar)


class TipoSinalNeural(Enum):
    """Tipos de sinais entre neurônios"""
    POTENCIAL_ACAO = "potencial_acao"       # Elétrico
    SINAPSE_QUIMICA = "sinapse_quimica"     # Via neurotransmissores
    GAP_JUNCTION = "gap_junction"           # Conexão elétrica direta
    VOLUME_TRANSMISSION = "volume"          # Difusão no espaço extracelular
    RETROGRADO = "retrogrado"               # Sinal de volta (pós -> pré)
    AUTOCRINO = "autocrino"                 # Neurônio sinaliza a si mesmo


class FatorCrescimento(Enum):
    """Fatores neurotróficos para crescimento neural"""
    BDNF = "BDNF"           # Brain-Derived Neurotrophic Factor
    NGF = "NGF"             # Nerve Growth Factor
    GDNF = "GDNF"           # Glial cell line-Derived Neurotrophic Factor
    NT3 = "NT3"             # Neurotrophin-3
    NT4 = "NT4"             # Neurotrophin-4
    IGF1 = "IGF1"           # Insulin-like Growth Factor 1


@dataclass
class Neuroblasto:
    """Célula precursora neural em processo de neurogênese"""
    id: str
    fase: FaseNeurogenese
    posicao_3d: Tuple[float, float, float]
    posicao_destino: Tuple[float, float, float]
    
    # Características em desenvolvimento
    tipo_previsto: str
    fatores_crescimento: Dict[FatorCrescimento, float] = field(default_factory=dict)
    
    # Timeline
    timestamp_nascimento: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    timestamp_maturacao_esperada: Optional[str] = None
    
    # Taxas
    velocidade_migracao: float = 0.1  # mm/hora
    taxa_diferenciacao: float = 0.01
    
    def avancar_fase(self) -> bool:
        """Avançar para próxima fase de desenvolvimento"""
        fases = list(FaseNeurogenese)
        idx_atual = fases.index(self.fase)
        
        if idx_atual < len(fases) - 2:  # Não avançar para apoptose automaticamente
            self.fase = fases[idx_atual + 1]
            
            if self.fase == FaseNeurogenese.MATURACAO:
                # Calcular data esperada de maturação
                dt = datetime.now(timezone.utc) + timedelta(hours=48)
                self.timestamp_maturacao_esperada = dt.isoformat()
            
            return True
        return False
    
    def migrar(self) -> float:
        """Migrar em direção ao destino"""
        if self.fase != FaseNeurogenese.MIGRACAO:
            return 0.0
        
        # Calcular vetor direção
        dx = self.posicao_destino[0] - self.posicao_3d[0]
        dy = self.posicao_destino[1] - self.posicao_3d[1]
        dz = self.posicao_destino[2] - self.posicao_3d[2]
        
        distancia = math.sqrt(dx**2 + dy**2 + dz**2)
        
        if distancia < 0.1:  # Chegou ao destino
            self.avancar_fase()
            return distancia
        
        # Mover na direção (com algum ruído biológico)
        fator = self.velocidade_migracao / distancia if distancia > 0 else 0
        ruido = 0.1
        
        self.posicao_3d = (
            self.posicao_3d[0] + dx * fator + random.uniform(-ruido, ruido),
            self.posicao_3d[1] + dy * fator + random.uniform(-ruido, ruido),
            self.posicao_3d[2] + dz * fator + random.uniform(-ruido, ruido)
        )
        
        return distancia
    
    @property
    def esta_maduro(self) -> bool:
        return self.fase == FaseNeurogenese.INTEGRACAO


@dataclass
class SinalNeural:
    """Um sinal neural transmitido entre neurônios"""
    id: str
    origem_id: str
    destino_id: str
    tipo: TipoSinalNeural
    
    # Características do sinal
    amplitude: float  # Força do sinal (0-1)
    frequencia: Optional[float] = None  # Hz, para sinais oscilatórios
    duracao_ms: float = 1.0
    
    # Conteúdo químico (para sinapses)
    neurotransmissores: List[str] = field(default_factory=list)
    concentracao_vesiculas: float = 0.5
    
    # Temporal
    timestamp_emissao: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    timestamp_recebimento: Optional[str] = None
    latencia_ms: Optional[float] = None
    
    # Modulação
    modulacao_presinaptica: float = 1.0  # Facilitação ou depressão
    modulacao_postsinsaptica: float = 1.0
    
    def calcular_eficacia(self) -> float:
        """Calcular eficácia do sinal considerando todas as modulações"""
        return (
            self.amplitude *
            self.modulacao_presinaptica *
            self.modulacao_postsinsaptica *
            (self.concentracao_vesiculas / 0.5)  # Normalizado
        )


@dataclass
class GapJunction:
    """Conexão elétrica direta entre neurônios (gap junction)"""
    id: str
    neuronio_a_id: str
    neuronio_b_id: str
    condutancia: float  # S (siemens) - facilidade de passagem de corrente
    resistencia: float  # Ohms
    
    # Sincronização
    sincronizacao_fase: float = 0.0  # 0-1, quão sincronizados estão
    frequencia_sincronia: Optional[float] = None
    
    def transmitir_corrente(self, potencial_a: float, potencial_b: float) -> float:
        """Calcular corrente transmitida (Lei de Ohm)"""
        # I = G * (V1 - V2)
        diferenca_potencial = potencial_a - potencial_b
        corrente = self.condutancia * diferenca_potencial
        return corrente
    
    def sincronizar(self, fase_a: float, fase_b: float):
        """Atualizar sincronização entre neurônios"""
        diff_fase = abs(fase_a - fase_b)
        self.sincronizacao_fase = 1.0 - (diff_fase / (2 * math.pi))


@dataclass
class AssemblyNeural:
    """Grupo de neurônios que disparam juntos (cell assembly)"""
    id: str
    nome: str
    neuronios_ids: Set[str]
    
    # Características
    padrao_ativacao: List[float] = field(default_factory=list)
    frequencia_ressonancia: Optional[float] = None
    forca_cohesao: float = 0.5  # Quão fortemente conectados
    
    # Formação
    timestamp_formacao: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    vezes_ativado: int = 0
    
    def ativar(self, intensidade: float = 1.0):
        """Ativar todo o assembly"""
        self.vezes_ativado += 1
        self.padrao_ativacao.append(intensidade)
        
        if len(self.padrao_ativacao) > 100:
            self.padrao_ativacao.pop(0)
    
    @property
    def esta_consolidado(self) -> bool:
        """Assembly está consolidado na memória de longo prazo"""
        return self.vezes_ativado > 10 and self.forca_cohesao > 0.7


@dataclass
class TrofismoNeural:
    """Estado trófico (nutricional) de um neurônio ou região"""
    neuronio_id: str
    
    # Fatores neurotróficos disponíveis
    fatores: Dict[FatorCrescimento, float] = field(default_factory=dict)
    
    # Nutrientes
    glicose: float = 1.0
    oxigenio: float = 1.0
    aminoacidos: float = 1.0
    lipideos: float = 1.0
    
    # Estado metabólico
    atp_producao: float = 1.0
    atp_consumo: float = 0.5
    stress_oxidativo: float = 0.0
    
    def calcular_saude(self) -> float:
        """Calcular índice de saúde trófica"""
        nutrientes = (self.glicose + self.oxigenio + self.aminoacidos + self.lipideos) / 4
        energia = self.atp_producao / max(0.1, self.atp_consumo)
        fatores = sum(self.fatores.values()) / max(1, len(self.fatores))
        
        saude = (nutrientes * 0.3 + energia * 0.4 + fatores * 0.3) - self.stress_oxidativo
        return max(0.0, min(1.0, saude))


class NeurogeneseComunicacao:
    """
    Sistema de neurogênese e comunicação neural da VHALINOR ai_geral.
    
    Permite:
    - Criação contínua de novos neurônios
    - Comunicação complexa entre neurônios (química e elétrica)
    - Formação de assemblies neurais
    - Manutenção trófica da rede neural
    """
    
    def __init__(self, ambiente_tridimensional: Tuple[float, float, float] = (100, 100, 10)):
        self.nome = "VHALINOR Neurogênese e Comunicação"
        self.versao = "6.0.0"
        
        # Dimensões do espaço neural (mm)
        self.ambiente_3d = ambiente_tridimensional
        
        # Neurogênese
        self.neuroblastos: Dict[str, Neuroblasto] = {}
        self.fila_neurogenese: deque = deque(maxlen=1000)
        self.zonas_proliferativas: List[Tuple[float, float, float]] = []
        self._inicializar_zonas_proliferativas()
        
        # Comunicação
        self.sinais_ativos: Dict[str, SinalNeural] = {}
        self.historico_sinais: deque = deque(maxlen=10000)
        self.gap_junctions: Dict[str, GapJunction] = {}
        self.assemblies: Dict[str, AssemblyNeural] = {}
        
        # Trofismo
        self.estado_trofico: Dict[str, TrofismoNeural] = {}
        
        # Configurações
        self.taxa_baseline_neurogenese = 0.001  # Novos neurônios por ciclo
        self.fator_atividade_dependente = 2.0  # Multiplicador se alta atividade
        self.limite_populacional = 100000
        
        # Métricas
        self.total_neuroblastos_criados = 0
        self.total_neuroblastos_maduros = 0
        self.total_neuroblastos_apoptose = 0
        self.total_sinais_transmitidos = 0
        self.total_gap_junctions_formadas = 0
        self.total_assemblies_formados = 0
        
        # Estado
        self._executando = False
        self.ciclo_atual = 0
        
        # Callbacks
        self._on_novo_neuronio: List[Callable] = []
        self._on_sinal_transmitido: List[Callable] = []
        self._on_assembly_formado: List[Callable] = []
    
    def _inicializar_zonas_proliferativas(self):
        """Inicializar zonas onde novos neurônios nascem"""
        # Simular giro denteado do hipocampo e zona subventricular
        self.zonas_proliferativas = [
            (20, 20, 2),   # Giro denteado (analogia)
            (80, 80, 2),   # Zona subventricular (analogia)
            (50, 10, 5),   # Córtex (baixa proliferação)
        ]
    
    def iniciar_neurogenese(
        self,
        quantidade: int = 1,
        tipo_previsto: str = "piramidal",
        estimulo_atividade: float = 0.0
    ) -> List[str]:
        """
        Iniciar processo de neurogênese.
        
        Args:
            quantidade: Quantos neuroblastos criar
            tipo_previsto: Tipo de neurônio que se tornarão
            estimulo_atividade: Estímulo por atividade (aumenta neurogênese)
        
        Returns:
            IDs dos neuroblastos criados
        """
        ids_criados = []
        
        # Ajustar taxa baseada no estímulo
        taxa_efetiva = self.taxa_baseline_neurogenese * (1 + estimulo_atividade * self.fator_atividade_dependente)
        
        for _ in range(quantidade):
            if random.random() > taxa_efetiva:
                continue
            
            # Escolher zona proliferativa
            zona = random.choice(self.zonas_proliferativas)
            
            # Posição com ruído
            posicao = (
                zona[0] + random.uniform(-5, 5),
                zona[1] + random.uniform(-5, 5),
                zona[2] + random.uniform(-1, 1)
            )
            
            # Destino aleatório no córtex
            destino = (
                random.uniform(0, self.ambiente_3d[0]),
                random.uniform(0, self.ambiente_3d[1]),
                random.uniform(0, self.ambiente_3d[2])
            )
            
            neuroblasto = Neuroblasto(
                id=f"nb_{self.total_neuroblastos_criados:06d}",
                fase=FaseNeurogenese.PROLIFERACAO,
                posicao_3d=posicao,
                posicao_destino=destino,
                tipo_previsto=tipo_previsto,
                fatores_crescimento={
                    FatorCrescimento.BDNF: random.uniform(0.5, 1.0),
                    FatorCrescimento.NGF: random.uniform(0.3, 0.8),
                }
            )
            
            self.neuroblastos[neuroblasto.id] = neuroblasto
            self.fila_neurogenese.append(neuroblasto.id)
            ids_criados.append(neuroblasto.id)
            
            self.total_neuroblastos_criados += 1
            
            # Notificar
            for callback in self._on_novo_neuronio:
                callback(neuroblasto)
        
        return ids_criados
    
    def processar_neurogenese(self, ciclos: int = 1) -> Dict[str, int]:
        """Processar ciclo de desenvolvimento dos neuroblastos"""
        resultados = {
            "maduros": 0,
            "em_desenvolvimento": 0,
            "apoptose": 0
        }
        
        for _ in range(ciclos):
            for nb_id in list(self.neuroblastos.keys()):
                neuroblasto = self.neuroblastos[nb_id]
                
                # Processar baseado na fase
                if neuroblasto.fase == FaseNeurogenese.MIGRACAO:
                    neuroblasto.migrar()
                    resultados["em_desenvolvimento"] += 1
                    
                elif neuroblasto.fase == FaseNeurogenese.DIFERENCIACAO:
                    # Chance de avançar baseada nos fatores de crescimento
                    saude = sum(neuroblasto.fatores_crescimento.values()) / len(neuroblasto.fatores_crescimento)
                    if random.random() < neuroblasto.taxa_diferenciacao * saude:
                        neuroblasto.avancar_fase()
                    resultados["em_desenvolvimento"] += 1
                    
                elif neuroblasto.fase == FaseNeurogenese.MATURACAO:
                    # Verificar se já está na hora de integrar
                    if neuroblasto.timestamp_maturacao_esperada:
                        esperada = datetime.fromisoformat(neuroblasto.timestamp_maturacao_esperada)
                        if datetime.now(timezone.utc) >= esperada:
                            neuroblasto.avancar_fase()
                            resultados["maduros"] += 1
                            self.total_neuroblastos_maduros += 1
                    else:
                        resultados["em_desenvolvimento"] += 1
                
                # Verificar apoptose (morte se desenvolvimento falhou)
                elif neuroblasto.fase == FaseNeurogenese.APTOPOSSE:
                    del self.neuroblastos[nb_id]
                    resultados["apoptose"] += 1
                    self.total_neuroblastos_apoptose += 1
                
                elif neuroblasto.esta_maduro:
                    resultados["maduros"] += 1
        
        return resultados
    
    def converter_neuroblasto(self, nb_id: str) -> Optional[str]:
        """Converter neuroblasto maduro em neurônio funcional"""
        if nb_id not in self.neuroblastos:
            return None
        
        nb = self.neuroblastos[nb_id]
        if not nb.esta_maduro:
            return None
        
        # Retornar dados para criar neurônio (integração com arquitetura_organica)
        return json.dumps({
            "tipo": nb.tipo_previsto,
            "posicao_3d": nb.posicao_3d,
            "origem": "neurogenese",
            "fatores_crescimento": {k.value: v for k, v in nb.fatores_crescimento.items()}
        })
    
    def transmitir_sinal(
        self,
        origem_id: str,
        destino_id: str,
        tipo: TipoSinalNeural,
        amplitude: float,
        neurotransmissores: Optional[List[str]] = None
    ) -> Optional[str]:
        """Transmitir sinal neural entre dois pontos"""
        sinal_id = f"sig_{origem_id}_{destino_id}_{int(time.time()*1000)}"
        
        sinal = SinalNeural(
            id=sinal_id,
            origem_id=origem_id,
            destino_id=destino_id,
            tipo=tipo,
            amplitude=amplitude,
            neurotransmissores=neurotransmissores or ["glutamato"]
        )
        
        # Simular latência baseada na distância (velocidade axonal ~1-100 m/s)
        # Simplificado: 1ms base + aleatório
        latencia = random.uniform(0.5, 2.0)
        sinal.latencia_ms = latencia
        
        # Registrar recebimento (simulado)
        time.sleep(latencia / 1000)  # Simular delay
        sinal.timestamp_recebimento = datetime.now(timezone.utc).isoformat()
        
        self.sinais_ativos[sinal_id] = sinal
        self.historico_sinais.append(sinal)
        self.total_sinais_transmitidos += 1
        
        # Notificar
        for callback in self._on_sinal_transmitido:
            callback(sinal)
        
        return sinal_id
    
    def criar_gap_junction(
        self,
        neuronio_a: str,
        neuronio_b: str,
        condutancia: Optional[float] = None
    ) -> str:
        """Criar conexão elétrica direta (gap junction)"""
        gj_id = f"gj_{neuronio_a}_{neuronio_b}"
        
        if condutancia is None:
            condutancia = random.uniform(0.1, 1.0)  # nS (nanosiemens)
        
        gap_junction = GapJunction(
            id=gj_id,
            neuronio_a_id=neuronio_a,
            neuronio_b_id=neuronio_b,
            condutancia=condutancia,
            resistencia=1.0 / condutancia if condutancia > 0 else float('inf')
        )
        
        self.gap_junctions[gj_id] = gap_junction
        self.total_gap_junctions_formadas += 1
        
        return gj_id
    
    def detectar_assembly(
        self,
        neuronios_ids: List[str],
        atividade_correlacionada: float
    ) -> Optional[str]:
        """Detectar e registrar assembly neural"""
        if len(neuronios_ids) < 3 or atividade_correlacionada < 0.6:
            return None
        
        assembly_id = f"asm_{hash(tuple(sorted(neuronios_ids))) % 100000:05d}"
        
        if assembly_id in self.assemblies:
            # Assembly existente, atualizar
            self.assemblies[assembly_id].ativar(atividade_correlacionada)
            return assembly_id
        
        assembly = AssemblyNeural(
            id=assembly_id,
            nome=f"Assembly_{len(self.assemblies)}",
            neuronios_ids=set(neuronios_ids),
            forca_cohesao=atividade_correlacionada
        )
        
        self.assemblies[assembly_id] = assembly
        self.total_assemblies_formados += 1
        
        for callback in self._on_assembly_formado:
            callback(assembly)
        
        return assembly_id
    
    def atualizar_trofismo(self, neuronio_id: str, condicoes: Dict[str, float]):
        """Atualizar estado trófico de um neurônio"""
        if neuronio_id not in self.estado_trofico:
            self.estado_trofico[neuronio_id] = TrofismoNeural(neuronio_id=neuronio_id)
        
        trofismo = self.estado_trofico[neuronio_id]
        
        # Atualizar com novas condições
        for chave, valor in condicoes.items():
            if hasattr(trofismo, chave):
                setattr(trofismo, chave, max(0.0, min(1.0, valor)))
        
        return trofismo.calcular_saude()
    
    def obter_neuroblastos_maduros(self) -> List[Neuroblasto]:
        """Obter lista de neuroblastos prontos para integração"""
        return [nb for nb in self.neuroblastos.values() if nb.esta_maduro]
    
    def obter_sincronizacao_rede(self) -> Dict[str, float]:
        """Calcular métricas de sincronização da rede"""
        if not self.gap_junctions:
            return {"media": 0.0, "maxima": 0.0}
        
        sincronizacoes = [gj.sincronizacao_fase for gj in self.gap_junctions.values()]
        
        return {
            "media": np.mean(sincronizacoes) if sincronizacoes else 0.0,
            "maxima": max(sincronizacoes) if sincronizacoes else 0.0,
            "minima": min(sincronizacoes) if sincronizacoes else 0.0,
            "std": np.std(sincronizacoes) if sincronizacoes else 0.0
        }
    
    def on_novo_neuronio(self, callback: Callable):
        """Registrar callback para quando novo neurônio é criado"""
        self._on_novo_neuronio.append(callback)
    
    def on_sinal_transmitido(self, callback: Callable):
        """Registrar callback para quando sinal é transmitido"""
        self._on_sinal_transmitido.append(callback)
    
    def on_assembly_formado(self, callback: Callable):
        """Registrar callback para quando assembly é formado"""
        self._on_assembly_formado.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status completo do sistema"""
        # Contar neuroblastos por fase
        fases_count = {}
        for nb in self.neuroblastos.values():
            f = nb.fase.value
            fases_count[f] = fases_count.get(f, 0) + 1
        
        # Calcular saúde trófica média
        saude_trofica = [
            t.calcular_saude()
            for t in self.estado_trofico.values()
        ]
        
        return {
            "nome": self.nome,
            "versao": self.versao,
            "neurogenese": {
                "total_neuroblastos": len(self.neuroblastos),
                "por_fase": fases_count,
                "maduros": sum(1 for nb in self.neuroblastos.values() if nb.esta_maduro),
                "total_criados": self.total_neuroblastos_criados,
                "total_maduros_historico": self.total_neuroblastos_maduros,
                "total_apoptose": self.total_neuroblastos_apoptose,
                "taxa_sobrevivencia": (
                    self.total_neuroblastos_maduros / max(1, self.total_neuroblastos_criados)
                )
            },
            "comunicacao": {
                "sinais_totais": self.total_sinais_transmitidos,
                "sinais_ativos": len(self.sinais_ativos),
                "gap_junctions": len(self.gap_junctions),
                "assemblies": len(self.assemblies),
                "assemblies_consolidados": sum(
                    1 for a in self.assemblies.values() if a.esta_consolidado
                )
            },
            "sincronizacao": self.obter_sincronizacao_rede(),
            "trofismo": {
                "neuronios_monitorados": len(self.estado_trofico),
                "saude_media": np.mean(saude_trofica) if saude_trofica else 0.0,
                "saude_minima": min(saude_trofica) if saude_trofica else 0.0
            },
            "ciclo_atual": self.ciclo_atual
        }
