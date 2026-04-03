"""
VHALINOR Automação Inteligente v6.0
====================================
Sistema de automação inteligente para ai_geral:
- Automação de tarefas repetitivas
- Scheduling e timers
- Integração com sistema operacional
- Automação de trading (com integração segura)
- Workflows personalizáveis
- Triggers e condições
- Execução paralela e sequencial
- Logging e monitoramento
- Fallbacks e recuperação de erros

@module automacao
@author VHALINOR Team
@version 6.0.0
@since 2026-04-01
"""

import numpy as np
from typing import Dict, List, Any, Optional, Tuple, Union, Callable, Coroutine
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum, auto
from collections import deque
import threading
import asyncio
import time
import os
import platform
import subprocess
import json
import hashlib
import schedule
import warnings

# Suprimir warnings de scheduling
warnings.filterwarnings("ignore", category=UserWarning, module="schedule")


class TipoAutomacao(Enum):
    """Tipos de automação disponíveis"""
    TAREFA_UNICA = "tarefa_unica"           # Executa uma vez
    RECORRENTE = "recorrente"               # Executa periodicamente
    CONDICIONAL = "condicional"             # Executa baseado em condições
    EVENTO = "evento"                       # Executa em eventos
    WORKFLOW = "workflow"                   # Sequência de tarefas
    PARALELA = "paralela"                   # Tarefas em paralelo
    OS_SYSTEM = "os_system"                 # Comandos do sistema
    TRADING = "trading"                     # Automação de trading (segura)
    NOTIFICACAO = "notificacao"             # Enviar notificações
    BACKUP = "backup"                       # Backup de dados


class EstadoTarefa(Enum):
    """Estados de uma tarefa automatizada"""
    PENDENTE = "pendente"
    AGENDADA = "agendada"
    EM_EXECUCAO = "em_execucao"
    CONCLUIDA = "concluida"
    FALHA = "falha"
    PAUSADA = "pausada"
    CANCELADA = "cancelada"


class PrioridadeTarefa(Enum):
    """Níveis de prioridade"""
    BAIXA = 1
    NORMAL = 2
    ALTA = 3
    CRITICA = 4
    URGENTE = 5


class TipoTrigger(Enum):
    """Tipos de triggers para automação"""
    TEMPO = "tempo"                         # Baseado em horário/data
    INTERVALO = "intervalo"                 # A cada X segundos/minutos
    CONDICAO = "condicao"                   # Quando condição for verdadeira
    EVENTO_EXTERNO = "evento_externo"       # Evento de sistema/mercado
    MANUAL = "manual"                       # Acionamento manual
    INICIALIZACAO = "inicializacao"         # Na inicialização


class TipoAcao(Enum):
    """Tipos de ações que podem ser automatizadas"""
    EXECUTAR_COMANDO = "executar_comando"
    CHAMAR_FUNCAO = "chamar_funcao"
    ENVIAR_NOTIFICACAO = "enviar_notificacao"
    SALVAR_ARQUIVO = "salvar_arquivo"
    LER_ARQUIVO = "ler_arquivo"
    REQUISICAO_HTTP = "requisicao_http"
    EXECUTAR_TRADE = "executar_trade"
    ANALISAR_DADOS = "analisar_dados"
    GERAR_RELATORIO = "gerar_relatorio"
    ATUALIZAR_BANCO = "atualizar_banco"
    ENVIAR_EMAIL = "enviar_email"
    AGENDAR_TAREFA = "agendar_tarefa"
    EXECUTAR_SCRIPT = "executar_script"
    COPIAR_DADOS = "copiar_dados"


@dataclass
class Trigger:
    """Configuração de trigger para automação"""
    tipo: TipoTrigger
    condicao: Optional[Callable] = None
    horario: Optional[str] = None  # "HH:MM" para triggers de tempo
    intervalo_segundos: Optional[int] = None
    dias_semana: List[int] = field(default_factory=list)  # 0=seg, 6=dom
    dados_adicionais: Dict[str, Any] = field(default_factory=dict)
    
    def __str__(self) -> str:
        if self.tipo == TipoTrigger.TEMPO and self.horario:
            return f"Todos os dias às {self.horario}"
        elif self.tipo == TipoTrigger.INTERVALO and self.intervalo_segundos:
            return f"A cada {self.intervalo_segundos} segundos"
        return f"Trigger: {self.tipo.value}"


@dataclass
class Acao:
    """Uma ação a ser executada"""
    tipo: TipoAcao
    parametros: Dict[str, Any] = field(default_factory=dict)
    funcao: Optional[Callable] = None
    falha_aceitavel: bool = False
    timeout_segundos: float = 30.0
    retry_tentativas: int = 3
    retry_delay: float = 1.0
    
    async def executar(self) -> Dict[str, Any]:
        """Executar a ação com retry"""
        for tentativa in range(self.retry_tentativas):
            try:
                if self.tipo == TipoAcao.CHAMAR_FUNCAO and self.funcao:
                    resultado = self.funcao(**self.parametros)
                    return {"sucesso": True, "resultado": resultado}
                
                elif self.tipo == TipoAcao.EXECUTAR_COMANDO:
                    comando = self.parametros.get("comando", "")
                    resultado = subprocess.run(
                        comando,
                        shell=True,
                        capture_output=True,
                        text=True,
                        timeout=self.timeout_segundos
                    )
                    return {
                        "sucesso": resultado.returncode == 0,
                        "stdout": resultado.stdout,
                        "stderr": resultado.stderr,
                        "returncode": resultado.returncode
                    }
                
                elif self.tipo == TipoAcao.SALVAR_ARQUIVO:
                    caminho = self.parametros.get("caminho", "")
                    conteudo = self.parametros.get("conteudo", "")
                    with open(caminho, 'w', encoding='utf-8') as f:
                        f.write(conteudo)
                    return {"sucesso": True, "caminho": caminho}
                
                elif self.tipo == TipoAcao.LER_ARQUIVO:
                    caminho = self.parametros.get("caminho", "")
                    with open(caminho, 'r', encoding='utf-8') as f:
                        conteudo = f.read()
                    return {"sucesso": True, "conteudo": conteudo}
                
                elif self.tipo == TipoAcao.ENVIAR_NOTIFICACAO:
                    titulo = self.parametros.get("titulo", "Notificação")
                    mensagem = self.parametros.get("mensagem", "")
                    return {"sucesso": True, "titulo": titulo, "mensagem": mensagem}
                
                else:
                    return {"sucesso": True, "mensagem": "Ação simulada", "tipo": self.tipo.value}
                    
            except Exception as e:
                if tentativa < self.retry_tentativas - 1:
                    time.sleep(self.retry_delay)
                else:
                    return {"sucesso": False, "erro": str(e)}
        
        return {"sucesso": False, "erro": "Todas as tentativas falharam"}


@dataclass
class Tarefa:
    """Uma tarefa automatizada"""
    id: str
    nome: str
    descricao: str
    tipo: TipoAutomacao
    trigger: Optional[Trigger]
    acoes: List[Acao]
    prioridade: PrioridadeTarefa = PrioridadeTarefa.NORMAL
    estado: EstadoTarefa = EstadoTarefa.PENDENTE
    dependencias: List[str] = field(default_factory=list)  # IDs de outras tarefas
    habilitada: bool = True
    data_criacao: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    ultima_execucao: Optional[str] = None
    proxima_execucao: Optional[str] = None
    total_execucoes: int = 0
    total_falhas: int = 0
    historico_resultados: deque = field(default_factory=lambda: deque(maxlen=10))
    metadados: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        if not self.id:
            self.id = hashlib.md5(f"{self.nome}{datetime.now()}".encode()).hexdigest()[:12]


@dataclass
class Workflow:
    """Um workflow composto por múltiplas tarefas"""
    id: str
    nome: str
    descricao: str
    tarefas: List[str]  # IDs das tarefas em ordem
    paralelo: bool = False  # Se True, executa tarefas em paralelo
    condicao_sucesso: str = "all"  # "all", "any", "majority"
    rollback_em_falha: bool = False
    estado: EstadoTarefa = EstadoTarefa.PENDENTE
    

@dataclass
class ExecucaoLog:
    """Log de execução de uma tarefa"""
    tarefa_id: str
    timestamp_inicio: str
    timestamp_fim: Optional[str] = None
    sucesso: bool = False
    resultado: Dict[str, Any] = field(default_factory=dict)
    erro: Optional[str] = None
    duracao_segundos: float = 0.0


class AutomacaoInteligente:
    """
    Sistema de automação inteligente da VHALINOR ai_geral.
    
    Permite criar, agendar e executar tarefas automatizadas
    com suporte a workflows, triggers, condições e recuperação de falhas.
    """
    
    def __init__(self, max_workers: int = 5):
        self.nome = "VHALINOR Automação"
        self.versao = "6.0.0"
        
        # Armazenamento
        self.tarefas: Dict[str, Tarefa] = {}
        self.workflows: Dict[str, Workflow] = {}
        self.log_execucoes: deque = deque(maxlen=1000)
        
        # Workers e threading
        self.max_workers = max_workers
        self._executor_threads: List[threading.Thread] = []
        self._loop_async: Optional[asyncio.AbstractEventLoop] = None
        self._thread_loop: Optional[threading.Thread] = None
        
        # Controle de execução
        self._executando = False
        self._tarefas_agendadas: List[schedule.Job] = []
        self._thread_scheduler: Optional[threading.Thread] = None
        self._lock = threading.Lock()
        
        # Callbacks
        self._on_tarefa_iniciada: List[Callable] = []
        self._on_tarefa_concluida: List[Callable] = []
        self._on_tarefa_falha: List[Callable] = []
        
        # Métricas
        self.total_tarefas_criadas = 0
        self.total_execucoes = 0
        self.total_sucessos = 0
        self.total_falhas = 0
    
    def criar_tarefa(
        self,
        nome: str,
        descricao: str,
        tipo: TipoAutomacao,
        acoes: List[Acao],
        trigger: Optional[Trigger] = None,
        prioridade: PrioridadeTarefa = PrioridadeTarefa.NORMAL,
        dependencias: Optional[List[str]] = None,
        habilitada: bool = True
    ) -> str:
        """Criar uma nova tarefa automatizada"""
        tarefa_id = hashlib.md5(f"{nome}{datetime.now(timezone.utc)}".encode()).hexdigest()[:12]
        
        tarefa = Tarefa(
            id=tarefa_id,
            nome=nome,
            descricao=descricao,
            tipo=tipo,
            trigger=trigger,
            acoes=acoes,
            prioridade=prioridade,
            dependencias=dependencias or [],
            habilitada=habilitada
        )
        
        self.tarefas[tarefa_id] = tarefa
        self.total_tarefas_criadas += 1
        
        # Se tem trigger de tempo, agendar imediatamente
        if trigger and trigger.tipo == TipoTrigger.TEMPO and trigger.horario:
            self._agendar_tarefa_tempo(tarefa)
        
        return tarefa_id
    
    def _agendar_tarefa_tempo(self, tarefa: Tarefa):
        """Agendar tarefa para execução em horário específico"""
        if not tarefa.trigger or not tarefa.trigger.horario:
            return
        
        horario = tarefa.trigger.horario
        
        # Parse horário "HH:MM"
        try:
            hora, minuto = map(int, horario.split(":"))
            
            # Agendar com schedule
            job = schedule.every().day.at(horario).do(
                self._executar_tarefa_agendada, tarefa.id
            )
            
            self._tarefas_agendadas.append(job)
            tarefa.estado = EstadoTarefa.AGENDADA
            tarefa.proxima_execucao = horario
            
        except ValueError:
            pass
    
    def _executar_tarefa_agendada(self, tarefa_id: str) -> None:
        """Executor para tarefas agendadas"""
        self.executar_tarefa(tarefa_id)
    
    def executar_tarefa(self, tarefa_id: str) -> Dict[str, Any]:
        """Executar uma tarefa imediatamente"""
        if tarefa_id not in self.tarefas:
            return {"sucesso": False, "erro": "Tarefa não encontrada"}
        
        tarefa = self.tarefas[tarefa_id]
        
        if not tarefa.habilitada:
            return {"sucesso": False, "erro": "Tarefa desabilitada"}
        
        # Verificar dependências
        for dep_id in tarefa.dependencias:
            if dep_id in self.tarefas:
                dep_tarefa = self.tarefas[dep_id]
                if dep_tarefa.estado != EstadoTarefa.CONCLUIDA:
                    return {"sucesso": False, "erro": f"Dependência {dep_id} não concluída"}
        
        # Atualizar estado
        tarefa.estado = EstadoTarefa.EM_EXECUCAO
        
        # Notificar início
        for callback in self._on_tarefa_iniciada:
            callback(tarefa)
        
        timestamp_inicio = datetime.now(timezone.utc).isoformat()
        
        # Executar ações
        resultados = []
        sucesso_geral = True
        
        for acao in tarefa.acoes:
            try:
                # Criar evento loop se necessário
                if asyncio.iscoroutinefunction(acao.executar):
                    if not self._loop_async:
                        self._inicializar_loop_async()
                    resultado = asyncio.run_coroutine_threadsafe(
                        acao.executar(), self._loop_async
                    ).result(timeout=acao.timeout_segundos)
                else:
                    resultado = asyncio.run(acao.executar())
                
                resultados.append(resultado)
                
                if not resultado.get("sucesso", False) and not acao.falha_aceitavel:
                    sucesso_geral = False
                    break
                    
            except Exception as e:
                resultado = {"sucesso": False, "erro": str(e)}
                resultados.append(resultado)
                sucesso_geral = False
                
                if not acao.falha_aceitavel:
                    break
        
        # Atualizar métricas
        timestamp_fim = datetime.now(timezone.utc).isoformat()
        duracao = (datetime.fromisoformat(timestamp_fim) - 
                   datetime.fromisoformat(timestamp_inicio)).total_seconds()
        
        tarefa.ultima_execucao = timestamp_inicio
        tarefa.total_execucoes += 1
        
        if sucesso_geral:
            tarefa.estado = EstadoTarefa.CONCLUIDA
            self.total_sucessos += 1
            
            # Notificar sucesso
            for callback in self._on_tarefa_concluida:
                callback(tarefa, resultados)
        else:
            tarefa.estado = EstadoTarefa.FALHA
            tarefa.total_falhas += 1
            self.total_falhas += 1
            
            # Notificar falha
            for callback in self._on_tarefa_falha:
                callback(tarefa, resultados)
        
        # Registrar log
        execucao_log = ExecucaoLog(
            tarefa_id=tarefa_id,
            timestamp_inicio=timestamp_inicio,
            timestamp_fim=timestamp_fim,
            sucesso=sucesso_geral,
            resultado={"acoes": resultados},
            duracao_segundos=duracao
        )
        
        self.log_execucoes.append(execucao_log)
        tarefa.historico_resultados.append(execucao_log)
        self.total_execucoes += 1
        
        return {
            "sucesso": sucesso_geral,
            "tarefa_id": tarefa_id,
            "resultados": resultados,
            "duracao": duracao
        }
    
    def _inicializar_loop_async(self):
        """Inicializar loop de eventos asyncio em thread separada"""
        def run_loop():
            self._loop_async = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop_async)
            self._loop_async.run_forever()
        
        self._thread_loop = threading.Thread(target=run_loop, daemon=True)
        self._thread_loop.start()
        time.sleep(0.1)  # Dar tempo para inicializar
    
    def criar_workflow(
        self,
        nome: str,
        descricao: str,
        tarefas_ids: List[str],
        paralelo: bool = False
    ) -> str:
        """Criar um workflow de múltiplas tarefas"""
        workflow_id = hashlib.md5(f"wf_{nome}{datetime.now()}".encode()).hexdigest()[:12]
        
        workflow = Workflow(
            id=workflow_id,
            nome=nome,
            descricao=descricao,
            tarefas=tarefas_ids,
            paralelo=paralelo
        )
        
        self.workflows[workflow_id] = workflow
        return workflow_id
    
    def executar_workflow(self, workflow_id: str) -> Dict[str, Any]:
        """Executar um workflow completo"""
        if workflow_id not in self.workflows:
            return {"sucesso": False, "erro": "Workflow não encontrado"}
        
        workflow = self.workflows[workflow_id]
        workflow.estado = EstadoTarefa.EM_EXECUCAO
        
        resultados = []
        
        if workflow.paralelo:
            # Executar em paralelo usando threads
            threads = []
            resultados_paralelos = {}
            
            def executar_e_armazenar(tarefa_id: str):
                resultados_paralelos[tarefa_id] = self.executar_tarefa(tarefa_id)
            
            for tarefa_id in workflow.tarefas:
                if tarefa_id in self.tarefas:
                    t = threading.Thread(target=executar_e_armazenar, args=(tarefa_id,))
                    threads.append(t)
                    t.start()
            
            for t in threads:
                t.join()
            
            resultados = [resultados_paralelos.get(tid, {}) for tid in workflow.tarefas]
        else:
            # Executar sequencialmente
            for tarefa_id in workflow.tarefas:
                if tarefa_id in self.tarefas:
                    resultado = self.executar_tarefa(tarefa_id)
                    resultados.append(resultado)
                    
                    # Se falhou e não aceita falha, parar
                    if not resultado.get("sucesso", False):
                        if workflow.rollback_em_falha:
                            # TODO: Implementar rollback
                            pass
                        break
        
        sucessos = sum(1 for r in resultados if r.get("sucesso", False))
        total = len(resultados)
        
        if workflow.condicao_sucesso == "all":
            workflow_sucesso = sucessos == total
        elif workflow.condicao_sucesso == "any":
            workflow_sucesso = sucessos > 0
        else:  # majority
            workflow_sucesso = sucessos > total / 2
        
        workflow.estado = EstadoTarefa.CONCLUIDA if workflow_sucesso else EstadoTarefa.FALHA
        
        return {
            "sucesso": workflow_sucesso,
            "workflow_id": workflow_id,
            "resultados": resultados,
            "sucessos": sucessos,
            "total": total
        }
    
    def iniciar_scheduler(self):
        """Iniciar o scheduler para tarefas agendadas"""
        if self._executando:
            return False
        
        self._executando = True
        
        def run_scheduler():
            while self._executando:
                schedule.run_pending()
                time.sleep(1)
        
        self._thread_scheduler = threading.Thread(target=run_scheduler, daemon=True)
        self._thread_scheduler.start()
        
        return True
    
    def parar_scheduler(self):
        """Parar o scheduler"""
        self._executando = False
        
        if self._thread_scheduler:
            self._thread_scheduler.join(timeout=2.0)
        
        schedule.clear()
        self._tarefas_agendadas.clear()
    
    def pausar_tarefa(self, tarefa_id: str) -> bool:
        """Pausar uma tarefa"""
        if tarefa_id in self.tarefas:
            self.tarefas[tarefa_id].estado = EstadoTarefa.PAUSADA
            self.tarefas[tarefa_id].habilitada = False
            return True
        return False
    
    def retomar_tarefa(self, tarefa_id: str) -> bool:
        """Retomar uma tarefa pausada"""
        if tarefa_id in self.tarefas:
            self.tarefas[tarefa_id].estado = EstadoTarefa.PENDENTE
            self.tarefas[tarefa_id].habilitada = True
            return True
        return False
    
    def excluir_tarefa(self, tarefa_id: str) -> bool:
        """Excluir uma tarefa"""
        if tarefa_id in self.tarefas:
            del self.tarefas[tarefa_id]
            return True
        return False
    
    def listar_tarefas(
        self,
        tipo: Optional[TipoAutomacao] = None,
        estado: Optional[EstadoTarefa] = None
    ) -> List[Tarefa]:
        """Listar tarefas com filtros opcionais"""
        tarefas = list(self.tarefas.values())
        
        if tipo:
            tarefas = [t for t in tarefas if t.tipo == tipo]
        
        if estado:
            tarefas = [t for t in tarefas if t.estado == estado]
        
        # Ordenar por prioridade (maior primeiro)
        tarefas.sort(key=lambda t: t.prioridade.value, reverse=True)
        
        return tarefas
    
    def obter_logs(self, tarefa_id: Optional[str] = None) -> List[ExecucaoLog]:
        """Obter logs de execução"""
        logs = list(self.log_execucoes)
        
        if tarefa_id:
            logs = [log for log in logs if log.tarefa_id == tarefa_id]
        
        return logs
    
    def on_tarefa_iniciada(self, callback: Callable):
        """Registrar callback para quando tarefa inicia"""
        self._on_tarefa_iniciada.append(callback)
    
    def on_tarefa_concluida(self, callback: Callable):
        """Registrar callback para quando tarefa conclui"""
        self._on_tarefa_concluida.append(callback)
    
    def on_tarefa_falha(self, callback: Callable):
        """Registrar callback para quando tarefa falha"""
        self._on_tarefa_falha.append(callback)
    
    def get_status(self) -> Dict[str, Any]:
        """Obter status do sistema de automação"""
        estados_count = {}
        for tarefa in self.tarefas.values():
            estado = tarefa.estado.value
            estados_count[estado] = estados_count.get(estado, 0) + 1
        
        return {
            "nome": self.nome,
            "versao": self.versao,
            "estatisticas": {
                "total_tarefas": len(self.tarefas),
                "total_workflows": len(self.workflows),
                "tarefas_por_estado": estados_count,
                "total_execucoes": self.total_execucoes,
                "total_sucessos": self.total_sucessos,
                "total_falhas": self.total_falhas,
                "taxa_sucesso": self.total_sucessos / max(1, self.total_execucoes)
            },
            "scheduler": {
                "executando": self._executando,
                "tarefas_agendadas": len(self._tarefas_agendadas)
            },
            "logs_disponiveis": len(self.log_execucoes)
        }


# ============== FUNÇÕES UTILITÁRIAS DE AUTOMAÇÃO ==============

def criar_acao_comando(comando: str, timeout: float = 30.0) -> Acao:
    """Criar ação para executar comando do sistema"""
    return Acao(
        tipo=TipoAcao.EXECUTAR_COMANDO,
        parametros={"comando": comando},
        timeout_segundos=timeout
    )


def criar_acao_funcao(funcao: Callable, **kwargs) -> Acao:
    """Criar ação para chamar função Python"""
    return Acao(
        tipo=TipoAcao.CHAMAR_FUNCAO,
        funcao=funcao,
        parametros=kwargs
    )


def criar_acao_notificacao(titulo: str, mensagem: str) -> Acao:
    """Criar ação para enviar notificação"""
    return Acao(
        tipo=TipoAcao.ENVIAR_NOTIFICACAO,
        parametros={"titulo": titulo, "mensagem": mensagem}
    )


def criar_acao_salvar_arquivo(caminho: str, conteudo: str) -> Acao:
    """Criar ação para salvar arquivo"""
    return Acao(
        tipo=TipoAcao.SALVAR_ARQUIVO,
        parametros={"caminho": caminho, "conteudo": conteudo}
    )


def criar_trigger_horario(horario: str) -> Trigger:
    """Criar trigger para horário específico (HH:MM)"""
    return Trigger(
        tipo=TipoTrigger.TEMPO,
        horario=horario
    )


def criar_trigger_intervalo(segundos: int) -> Trigger:
    """Criar trigger para intervalo em segundos"""
    return Trigger(
        tipo=TipoTrigger.INTERVALO,
        intervalo_segundos=segundos
    )


def criar_trigger_condicao(condicao: Callable) -> Trigger:
    """Criar trigger baseado em condição"""
    return Trigger(
        tipo=TipoTrigger.CONDICAO,
        condicao=condicao
    )
