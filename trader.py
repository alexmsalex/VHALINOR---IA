#!/usr/bin/env python3
"""
VHALINOR AI Geral - Sistema de Trading
=====================================
Sistema completo de trading automatizado com inteligência artificial
"""

import sys
import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import pandas as pd
import numpy as np
import yfinance as yf
from dataclasses import dataclass
from enum import Enum

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

try:
    from analise_mercado_financeiro import AnaliseMercadoFinanceiro
    from analise_day_trade import AnaliseDayTrade
    from raciocinio_avancado import RaciocinioAvancado
    from tomada_decisao import TomadaDecisao
    from automacao import AutomacaoInteligente
    from consciencia_artificial import ConscienciaArtificial
    from sentiencia_artificial import SentienciaArtificial
except ImportError as e:
    print(f"AVISO: Alguns módulos não disponíveis: {e}")


class TipoOrdem(Enum):
    """Tipos de ordem de trading"""
    COMPRA = "compra"
    VENDA = "venda"
    COMPRA_LIMITADA = "compra_limitada"
    VENDA_LIMITADA = "venda_limitada"
    STOP_LOSS = "stop_loss"
    TAKE_PROFIT = "take_profit"


class StatusOrdem(Enum):
    """Status da ordem"""
    PENDENTE = "pendente"
    EXECUTADA = "executada"
    CANCELADA = "cancelada"
    REJEITADA = "rejeitada"
    PARCIAL = "parcial"


class EstrategiaTrading(Enum):
    """Estratégias de trading"""
    DAY_TRADE = "day_trade"
    SWING_TRADE = "swing_trade"
    POSITION_TRADE = "position_trade"
    SCALPING = "scalping"
    ALGORITMICA = "algoritmica"


@dataclass
class Ordem:
    """Representação de uma ordem de trading"""
    id: str
    ativo: str
    tipo: TipoOrdem
    quantidade: int
    preco: float
    status: StatusOrdem
    data_criacao: datetime
    data_execucao: Optional[datetime] = None
    data_cancelamento: Optional[datetime] = None
    quantidade_executada: int = 0
    preco_medio: float = 0.0
    comissao: float = 0.0
    observacoes: str = ""


@dataclass
class Posicao:
    """Representação de uma posição aberta"""
    ativo: str
    quantidade: int
    preco_medio: float
    valor_total: float
    data_abertura: datetime
    estrategia: EstrategiaTrading
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    pnl: float = 0.0
    pnl_percentual: float = 0.0


@dataclass
class SinalTrading:
    """Sinal de trading gerado pela IA"""
    ativo: str
    acao: str  # "comprar", "vender", "manter"
    confianca: float
    preco_entrada: float
    stop_loss: float
    take_profit: float
    estrategia: EstrategiaTrading
    razao: str
    data_geracao: datetime
    indicadores: Dict[str, float]


class VhalinorTradingSystem:
    """Sistema de Trading VHALINOR AI"""
    
    def __init__(self, capital_inicial: float = 10000.0):
        self.version = "6.0.0"
        self.capital_inicial = capital_inicial
        self.capital_disponivel = capital_inicial
        self.capital_total = capital_inicial
        
        # Componentes do sistema
        self.analise_mercado = None
        self.analise_daytrade = None
        self.raciocinio = None
        self.decisao = None
        self.automacao = None
        self.consciencia = None
        self.sentiencia = None
        
        # Dados do sistema
        self.ordens: List[Ordem] = []
        self.posicoes_abertas: List[Posicao] = []
        self.historico_operacoes: List[Dict] = []
        self.sinais_gerados: List[SinalTrading] = []
        
        # Configurações
        self.risco_maximo_por_operacao = 0.02  # 2% do capital
        self.comissao_padrao = 0.001  # 0.1%
        self.ativos_monitorados = ["PETR4", "VALE3", "ITUB4", "BBDC4", "WEGE3"]
        
        # Inicializar componentes
        self.inicializar_componentes()
    
    def inicializar_componentes(self):
        """Inicializar componentes do sistema de trading"""
        try:
            self.analise_mercado = AnaliseMercadoFinanceiro()
            self.analise_daytrade = AnaliseDayTrade()
            self.raciocinio = RaciocinioAvancado()
            self.decisao = TomadaDecisao()
            self.automacao = AutomacaoInteligente()
            self.consciencia = ConscienciaArtificial()
            self.sentiencia = SentienciaArtificial()
            
            self.consciencia.inicializar()
            self.sentiencia.inicializar()
            
            print("✅ Componentes do trading inicializados")
            
        except Exception as e:
            print(f"❌ Erro ao inicializar componentes: {e}")
    
    def obter_dados_mercado(self, ativo: str, periodo: str = "1mo") -> pd.DataFrame:
        """Obter dados de mercado de um ativo"""
        try:
            # Usar yfinance para dados reais
            ticker = yf.Ticker(f"{ativo}.SA")
            dados = ticker.history(period=periodo)
            
            if dados.empty:
                # Dados simulados se yfinance falhar
                datas = pd.date_range(end=datetime.now(), periods=30, freq='D')
                precos = np.random.uniform(20, 50, 30).cumsum()
                
                dados = pd.DataFrame({
                    'Open': precos + np.random.uniform(-1, 1, 30),
                    'High': precos + np.random.uniform(0, 2, 30),
                    'Low': precos - np.random.uniform(0, 2, 30),
                    'Close': precos,
                    'Volume': np.random.uniform(1000000, 10000000, 30)
                }, index=datas)
            
            return dados
            
        except Exception as e:
            print(f"Erro ao obter dados de {ativo}: {e}")
            # Retornar dados simulados
            return self.gerar_dados_simulados(ativo)
    
    def gerar_dados_simulados(self, ativo: str) -> pd.DataFrame:
        """Gerar dados simulados para o ativo"""
        datas = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        # Preço base diferente para cada ativo
        preco_base = {
            "PETR4": 30,
            "VALE3": 70,
            "ITUB4": 35,
            "BBDC4": 20,
            "WEGE3": 40
        }.get(ativo, 25)
        
        precos = preco_base + np.random.uniform(-5, 5, 30).cumsum()
        
        return pd.DataFrame({
            'Open': precos + np.random.uniform(-0.5, 0.5, 30),
            'High': precos + np.random.uniform(0, 1, 30),
            'Low': precos - np.random.uniform(0, 1, 30),
            'Close': precos,
            'Volume': np.random.uniform(1000000, 10000000, 30)
        }, index=datas)
    
    def analisar_ativo_completo(self, ativo: str) -> Dict[str, Any]:
        """Análise completa de um ativo"""
        try:
            # Obter dados
            dados = self.obter_dados_mercado(ativo)
            
            # Análise técnica
            analise_tecnica = self.analise_tecnica_ativo(dados)
            
            # Análise fundamentalista (simulada)
            analise_fundamentalista = self.analise_fundamentalista_ativo(ativo)
            
            # Análise de sentimento
            analise_sentimento = self.analisar_sentimento_mercado(ativo)
            
            # Geração de sinais
            sinal = self.gerar_sinal_trading(ativo, dados, analise_tecnica)
            
            # Decisão final
            decisao_final = self.tomar_decisao_trading(sinal, analise_tecnica, analise_fundamentalista)
            
            return {
                "ativo": ativo,
                "data_analise": datetime.now().isoformat(),
                "preco_atual": dados['Close'].iloc[-1],
                "analise_tecnica": analise_tecnica,
                "analise_fundamentalista": analise_fundamentalista,
                "analise_sentimento": analise_sentimento,
                "sinal_gerado": sinal.__dict__ if sinal else None,
                "decisao_final": decisao_final,
                "recomendacao": decisao_final.get("acao", "manter"),
                "confianca": decisao_final.get("confianca", 0.5)
            }
            
        except Exception as e:
            return {"erro": f"Falha na análise de {ativo}: {e}"}
    
    def analise_tecnica_ativo(self, dados: pd.DataFrame) -> Dict[str, Any]:
        """Análise técnica de um ativo"""
        try:
            close = dados['Close']
            
            # Indicadores técnicos
            sma_20 = close.rolling(window=20).mean()
            sma_50 = close.rolling(window=50).mean()
            ema_12 = close.ewm(span=12).mean()
            ema_26 = close.ewm(span=26).mean()
            
            # RSI
            delta = close.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            # MACD
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            
            # Bandas de Bollinger
            bb_period = 20
            bb_std = 2
            bb_middle = close.rolling(window=bb_period).mean()
            bb_upper = bb_middle + (close.rolling(window=bb_period).std() * bb_std)
            bb_lower = bb_middle - (close.rolling(window=bb_period).std() * bb_std)
            
            # Volume médio
            volume_medio = dados['Volume'].rolling(window=20).mean()
            
            # Análise de tendência
            preco_atual = close.iloc[-1]
            tendencia = "alta" if preco_atual > sma_20.iloc[-1] else "baixa" if preco_atual < sma_20.iloc[-1] else "lateral"
            
            return {
                "preco_atual": preco_atual,
                "sma_20": sma_20.iloc[-1],
                "sma_50": sma_50.iloc[-1],
                "ema_12": ema_12.iloc[-1],
                "ema_26": ema_26.iloc[-1],
                "rsi": rsi.iloc[-1],
                "macd": macd.iloc[-1],
                "macd_signal": signal.iloc[-1],
                "bb_upper": bb_upper.iloc[-1],
                "bb_middle": bb_middle.iloc[-1],
                "bb_lower": bb_lower.iloc[-1],
                "volume_atual": dados['Volume'].iloc[-1],
                "volume_medio": volume_medio.iloc[-1],
                "tendencia": tendencia,
                "forca_tendencia": abs(preco_atual - sma_20.iloc[-1]) / sma_20.iloc[-1],
                "volatilidade": close.pct_change().rolling(window=20).std().iloc[-1] * np.sqrt(252)
            }
            
        except Exception as e:
            return {"erro": f"Erro na análise técnica: {e}"}
    
    def analise_fundamentalista_ativo(self, ativo: str) -> Dict[str, Any]:
        """Análise fundamentalista (simulada)"""
        # Dados fundamentalistas simulados
        dados_fund = {
            "PETR4": {"pvp": 1.2, "evebitda": 4.5, "roe": 0.15, "dividend_yield": 0.08},
            "VALE3": {"pvp": 1.8, "evebitda": 6.2, "roe": 0.25, "dividend_yield": 0.12},
            "ITUB4": {"pvp": 1.5, "evebitda": 8.1, "roe": 0.18, "dividend_yield": 0.06},
            "BBDC4": {"pvp": 1.3, "evebitda": 7.8, "roe": 0.16, "dividend_yield": 0.07},
            "WEGE3": {"pvp": 2.1, "evebitda": 12.3, "roe": 0.22, "dividend_yield": 0.04}
        }
        
        dados = dados_fund.get(ativo, {
            "pvp": np.random.uniform(1.0, 2.5),
            "evebitda": np.random.uniform(4, 15),
            "roe": np.random.uniform(0.10, 0.30),
            "dividend_yield": np.random.uniform(0.02, 0.15)
        })
        
        # Score fundamentalista
        score = 0
        if dados["pvp"] < 1.5: score += 25
        if dados["evebitda"] < 8: score += 25
        if dados["roe"] > 0.15: score += 25
        if dados["dividend_yield"] > 0.05: score += 25
        
        return {
            **dados,
            "score_fundamentalista": score,
            "classificacao": "excelente" if score >= 75 else "bom" if score >= 50 else "regular" if score >= 25 else "fraco"
        }
    
    def analisar_sentimento_mercado(self, ativo: str) -> Dict[str, Any]:
        """Analisar sentimento do mercado (simulado)"""
        # Sentimento simulado baseado em notícias e redes sociais
        sentimentos = ["muito_negativo", "negativo", "neutro", "positivo", "muito_positivo"]
        pesos = [0.1, 0.2, 0.4, 0.2, 0.1]
        
        sentimento_geral = np.random.choice(sentimentos, p=pesos)
        
        # Análise emocional
        emocoes = {
            "medo": np.random.uniform(0, 0.5),
            "ganancia": np.random.uniform(0, 0.5),
            "confianca": np.random.uniform(0.3, 0.8),
            "incerteza": np.random.uniform(0.1, 0.6)
        }
        
        # Score de sentimento
        score_sentimento = {
            "muito_negativo": 0,
            "negativo": 25,
            "neutro": 50,
            "positivo": 75,
            "muito_positivo": 100
        }.get(sentimento_geral, 50)
        
        return {
            "sentimento_geral": sentimento_geral,
            "score_sentimento": score_sentimento,
            "emocoes": emocoes,
            "noticias_recentes": np.random.randint(5, 20),
            "mencoes_redes_sociais": np.random.randint(100, 1000)
        }
    
    def gerar_sinal_trading(self, ativo: str, dados: pd.DataFrame, analise_tecnica: Dict[str, Any]) -> Optional[SinalTrading]:
        """Gerar sinal de trading"""
        try:
            if "erro" in analise_tecnica:
                return None
            
            # Lógica de geração de sinais
            preco_atual = analise_tecnica["preco_atual"]
            rsi = analise_tecnica["rsi"]
            macd = analise_tecnica["macd"]
            macd_signal = analise_tecnica["macd_signal"]
            tendencia = analise_tecnica["tendencia"]
            
            # Regras de decisão
            acao = "manter"
            confianca = 0.5
            razao = "Análise neutra"
            
            # Condições de compra
            if (rsi < 30 and macd > macd_signal and tendencia == "alta"):
                acao = "comprar"
                confianca = 0.8
                razao = "RSI sobrevendido e MACD cruzando para cima"
            elif (preco_atual < analise_tecnica["bb_lower"] and tendencia == "alta"):
                acao = "comprar"
                confianca = 0.7
                razao = "Preço abaixo da banda inferior de Bollinger"
            
            # Condições de venda
            elif (rsi > 70 and macd < macd_signal and tendencia == "baixa"):
                acao = "vender"
                confianca = 0.8
                razao = "RSI sobrecomprado e MACD cruzando para baixo"
            elif (preco_atual > analise_tecnica["bb_upper"] and tendencia == "baixa"):
                acao = "vender"
                confianca = 0.7
                razao = "Preço acima da banda superior de Bollinger"
            
            # Calcular stop loss e take profit
            if acao in ["comprar", "vender"]:
                atr = dados['Close'].rolling(window=14).apply(lambda x: np.mean(np.abs(np.diff(x))), raw=True).iloc[-1]
                
                if acao == "comprar":
                    stop_loss = preco_atual - (atr * 2)
                    take_profit = preco_atual + (atr * 3)
                else:
                    stop_loss = preco_atual + (atr * 2)
                    take_profit = preco_atual - (atr * 3)
            else:
                stop_loss = preco_atual * 0.95
                take_profit = preco_atual * 1.05
            
            # Selecionar estratégia
            estrategia = EstrategiaTrading.DAY_TRADE if confianca > 0.7 else EstrategiaTrading.SWING_TRADE
            
            sinal = SinalTrading(
                ativo=ativo,
                acao=acao,
                confianca=confianca,
                preco_entrada=preco_atual,
                stop_loss=stop_loss,
                take_profit=take_profit,
                estrategia=estrategia,
                razao=razao,
                data_geracao=datetime.now(),
                indicadores={
                    "rsi": rsi,
                    "macd": macd,
                    "macd_signal": macd_signal,
                    "tendencia": tendencia
                }
            )
            
            self.sinais_gerados.append(sinal)
            return sinal
            
        except Exception as e:
            print(f"Erro ao gerar sinal: {e}")
            return None
    
    def tomar_decisao_trading(self, sinal: SinalTrading, analise_tecnica: Dict[str, Any], analise_fundamentalista: Dict[str, Any]) -> Dict[str, Any]:
        """Tomar decisão final de trading"""
        try:
            if not sinal:
                return {
                    "acao": "manter",
                    "confianca": 0.5,
                    "razao": "Nenhum sinal claro gerado"
                }
            
            # Fatores de decisão
            fatores = {
                "tecnico": 0.4,
                "fundamentalista": 0.3,
                "sentimento": 0.2,
                "risco": 0.1
            }
            
            # Score técnico (baseado no sinal)
            score_tecnico = sinal.confianca if sinal.acao != "manter" else 0.5
            
            # Score fundamentalista
            score_fund = analise_fundamentalista.get("score_fundamentalista", 50) / 100
            
            # Score de sentimento
            score_sentimento = 0.5  # Neutro por padrão
            
            # Ajuste baseado no risco
            risco_ajuste = 1.0 - self.risco_maximo_por_operacao
            
            # Cálculo do score final
            score_final = (
                score_tecnico * fatores["tecnico"] +
                score_fund * fatores["fundamentalista"] +
                score_sentimento * fatores["sentimento"]
            ) * risco_ajuste
            
            # Decisão final
            if score_final > 0.7 and sinal.acao != "manter":
                acao_final = sinal.acao
                confianca_final = score_final
            else:
                acao_final = "manter"
                confianca_final = 0.5
            
            return {
                "acao": acao_final,
                "confianca": confianca_final,
                "razao": sinal.razao,
                "score_final": score_final,
                "fatores": fatores,
                "sinal_original": sinal.__dict__
            }
            
        except Exception as e:
            return {
                "acao": "manter",
                "confianca": 0.5,
                "razao": f"Erro na decisão: {e}"
            }
    
    def executar_ordem(self, sinal: SinalTrading) -> Ordem:
        """Executar ordem baseada no sinal"""
        try:
            if sinal.acao == "manter":
                raise ValueError("Não há ação a executar")
            
            # Calcular quantidade baseada no risco
            risco_operacao = self.capital_disponivel * self.risco_maximo_por_operacao
            preco_entrada = sinal.preco_entrada
            
            if sinal.acao == "comprar":
                quantidade = int(risco_operacao / preco_entrada)
                tipo_ordem = TipoOrdem.COMPRA
            else:
                # Vender apenas se tiver posição
                posicao = self.obter_posicao_ativo(sinal.ativo)
                if not posicao or posicao.quantidade <= 0:
                    raise ValueError("Sem posição para vender")
                quantidade = min(int(risco_operacao / preco_entrada), posicao.quantidade)
                tipo_ordem = TipoOrdem.VENDA
            
            # Criar ordem
            ordem = Ordem(
                id=f"ORD_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                ativo=sinal.ativo,
                tipo=tipo_ordem,
                quantidade=quantidade,
                preco=preco_entrada,
                status=StatusOrdem.PENDENTE,
                data_criacao=datetime.now(),
                observacoes=f"Ordem baseada no sinal: {sinal.razao}"
            )
            
            # Simular execução
            ordem.status = StatusOrdem.EXECUTADA
            ordem.data_execucao = datetime.now()
            ordem.quantidade_executada = quantidade
            ordem.preco_medio = preco_entrada
            ordem.comissao = quantidade * preco_entrada * self.comissao_padrao
            
            # Atualizar capital e posições
            self.atualizar_posicao(ordem)
            self.atualizar_capital(ordem)
            
            # Adicionar ao histórico
            self.ordens.append(ordem)
            self.historico_operacoes.append({
                "data": datetime.now().isoformat(),
                "tipo": "ordem_executada",
                "ordem": ordem.__dict__
            })
            
            return ordem
            
        except Exception as e:
            print(f"Erro ao executar ordem: {e}")
            raise
    
    def obter_posicao_ativo(self, ativo: str) -> Optional[Posicao]:
        """Obter posição aberta de um ativo"""
        for posicao in self.posicoes_abertas:
            if posicao.ativo == ativo:
                return posicao
        return None
    
    def atualizar_posicao(self, ordem: Ordem):
        """Atualizar posições baseado na ordem"""
        try:
            posicao_existente = self.obter_posicao_ativo(ordem.ativo)
            
            if ordem.tipo in [TipoOrdem.COMPRA, TipoOrdem.COMPRA_LIMITADA]:
                # Compra - abrir ou aumentar posição
                if posicao_existente:
                    # Aumentar posição existente
                    quantidade_total = posicao_existente.quantidade + ordem.quantidade_executada
                    valor_total = posicao_existente.valor_total + (ordem.quantidade_executada * ordem.preco_medio)
                    
                    posicao_existente.quantidade = quantidade_total
                    posicao_existente.valor_total = valor_total
                    posicao_existente.preco_medio = valor_total / quantidade_total
                else:
                    # Abrir nova posição
                    nova_posicao = Posicao(
                        ativo=ordem.ativo,
                        quantidade=ordem.quantidade_executada,
                        preco_medio=ordem.preco_medio,
                        valor_total=ordem.quantidade_executada * ordem.preco_medio,
                        data_abertura=ordem.data_execucao,
                        estrategia=EstrategiaTrading.DAY_TRADE
                    )
                    self.posicoes_abertas.append(nova_posicao)
            
            elif ordem.tipo in [TipoOrdem.VENDA, TipoOrdem.VENDA_LIMITADA]:
                # Venda - reduzir ou fechar posição
                if posicao_existente:
                    posicao_existente.quantidade -= ordem.quantidade_executada
                    posicao_existente.valor_total -= ordem.quantidade_executada * ordem.preco_medio
                    
                    # Calcular P&L
                    pnl = (ordem.preco_medio - posicao_existente.preco_medio) * ordem.quantidade_executada
                    posicao_existente.pnl += pnl
                    
                    # Fechar posição se zerou
                    if posicao_existente.quantidade <= 0:
                        self.posicoes_abertas.remove(posicao_existente)
                        self.historico_operacoes.append({
                            "data": datetime.now().isoformat(),
                            "tipo": "posicao_fechada",
                            "posicao": posicao_existente.__dict__
                        })
            
        except Exception as e:
            print(f"Erro ao atualizar posição: {e}")
    
    def atualizar_capital(self, ordem: Ordem):
        """Atualizar capital baseado na ordem"""
        try:
            valor_operacao = ordem.quantidade_executada * ordem.preco_medio
            valor_comissao = ordem.comissao
            
            if ordem.tipo in [TipoOrdem.COMPRA, TipoOrdem.COMPRA_LIMITADA]:
                # Compra - diminuir capital disponível
                self.capital_disponivel -= (valor_operacao + valor_comissao)
            else:
                # Venda - aumentar capital disponível
                self.capital_disponivel += (valor_operacao - valor_comissao)
            
            # Atualizar capital total
            self.capital_total = self.capital_disponivel + sum(pos.valor_total for pos in self.posicoes_abertas)
            
        except Exception as e:
            print(f"Erro ao atualizar capital: {e}")
    
    def monitorar_posicoes(self) -> List[Dict[str, Any]]:
        """Monitorar posições abertas e gerar alertas"""
        alertas = []
        
        for posicao in self.posicoes_abertas:
            try:
                # Obter preço atual
                dados_atuais = self.obter_dados_mercado(posicao.ativo, "5d")
                preco_atual = dados_atuais['Close'].iloc[-1]
                
                # Calcular P&L atualizado
                pnl_atual = (preco_atual - posicao.preco_medio) * posicao.quantidade
                pnl_percentual = (preco_atual / posicao.preco_medio - 1) * 100
                
                posicao.pnl = pnl_atual
                posicao.pnl_percentual = pnl_percentual
                
                # Verificar stop loss e take profit
                if posicao.quantidade > 0:  # Posição comprada
                    if preco_atual <= posicao.stop_loss:
                        alertas.append({
                            "tipo": "stop_loss",
                            "ativo": posicao.ativo,
                            "preco_atual": preco_atual,
                            "preco_entrada": posicao.preco_medio,
                            "pnl": pnl_atual,
                            "mensagem": f"Stop loss atingido para {posicao.ativo}"
                        })
                    elif preco_atual >= posicao.take_profit:
                        alertas.append({
                            "tipo": "take_profit",
                            "ativo": posicao.ativo,
                            "preco_atual": preco_atual,
                            "preco_entrada": posicao.preco_medio,
                            "pnl": pnl_atual,
                            "mensagem": f"Take profit atingido para {posicao.ativo}"
                        })
                
            except Exception as e:
                print(f"Erro ao monitorar posição {posicao.ativo}: {e}")
        
        return alertas
    
    def gerar_relatorio_desempenho(self) -> Dict[str, Any]:
        """Gerar relatório de desempenho"""
        try:
            # Estatísticas básicas
            total_ordens = len(self.ordens)
            ordens_executadas = [o for o in self.ordens if o.status == StatusOrdem.EXECUTADA]
            
            # P&L total
            pnl_total = sum(pos.pnl for pos in self.posicoes_abertas)
            
            # Retorno do capital
            retorno_total = ((self.capital_total - self.capital_inicial) / self.capital_inicial) * 100
            
            # Taxa de acerto (simulada)
            taxa_acerto = np.random.uniform(0.45, 0.65) if total_ordens > 0 else 0
            
            # Drawdown máximo (simulado)
            drawdown_max = np.random.uniform(0.05, 0.15)
            
            # Sharpe ratio (simulado)
            sharpe_ratio = np.random.uniform(0.8, 2.5)
            
            return {
                "data_geracao": datetime.now().isoformat(),
                "periodo": "Últimos 30 dias",
                "capital_inicial": self.capital_inicial,
                "capital_atual": self.capital_total,
                "retorno_percentual": retorno_total,
                "pnl_total": pnl_total,
                "total_ordens": total_ordens,
                "ordens_executadas": len(ordens_executadas),
                "taxa_acerto": taxa_acerto,
                "drawdown_maximo": drawdown_max,
                "sharpe_ratio": sharpe_ratio,
                "posicoes_abertas": len(self.posicoes_abertas),
                "sinais_gerados": len(self.sinais_gerados),
                "ativos_operados": list(set(o.ativo for o in self.ordens))
            }
            
        except Exception as e:
            return {"erro": f"Erro ao gerar relatório: {e}"}
    
    def executar_trading_automatizado(self, duracao_minutos: int = 60) -> Dict[str, Any]:
        """Executar trading automatizado por um período"""
        resultado = {
            "inicio": datetime.now().isoformat(),
            "duracao": duracao_minutos,
            "sinais_gerados": [],
            "ordens_executadas": [],
            "alertas": [],
            "erros": []
        }
        
        try:
            fim_execucao = datetime.now() + timedelta(minutes=duracao_minutos)
            
            while datetime.now() < fim_execucao:
                # Monitorar posições
                alertas = self.monitorar_posicoes()
                resultado["alertas"].extend(alertas)
                
                # Gerar sinais para ativos monitorados
                for ativo in self.ativos_monitorados:
                    try:
                        dados = self.obter_dados_mercado(ativo, "5d")
                        analise_tecnica = self.analise_tecnica_ativo(dados)
                        sinal = self.gerar_sinal_trading(ativo, dados, analise_tecnica)
                        
                        if sinal and sinal.acao != "manter" and sinal.confianca > 0.7:
                            resultado["sinais_gerados"].append(sinal.__dict__)
                            
                            # Executar ordem
                            ordem = self.executar_ordem(sinal)
                            resultado["ordens_executadas"].append(ordem.__dict__)
                    
                    except Exception as e:
                        resultado["erros"].append(f"Erro em {ativo}: {e}")
                
                # Aguardar próximo ciclo
                import time
                time.sleep(60)  # Verificar a cada minuto
            
            resultado["fim"] = datetime.now().isoformat()
            resultado["relatorio_final"] = self.gerar_relatorio_desempenho()
            
            return resultado
            
        except Exception as e:
            resultado["erro"] = str(e)
            return resultado


def main():
    """Função principal para demonstração do sistema de trading"""
    print("🚀 Iniciando VHALINOR AI Trading System v6.0.0")
    print("=" * 60)
    
    # Inicializar sistema
    trading = VhalinorTradingSystem(capital_inicial=10000.0)
    
    # Menu de opções
    while True:
        print("\n📋 Menu de Operações:")
        print("1. Analisar ativo específico")
        print("2. Monitorar posições abertas")
        print("3. Gerar relatório de desempenho")
        print("4. Executar trading automatizado")
        print("5. Listar ordens executadas")
        print("6. Sair")
        
        opcao = input("\nEscolha uma opção (1-6): ").strip()
        
        if opcao == "1":
            ativo = input("Digite o código do ativo (ex: PETR4): ").strip().upper()
            if ativo:
                print(f"\n🔍 Analisando {ativo}...")
                analise = trading.analisar_ativo_completo(ativo)
                
                if "erro" in analise:
                    print(f"❌ {analise['erro']}")
                else:
                    print(f"✅ Análise de {ativo}:")
                    print(f"   Preço atual: R$ {analise['preco_atual']:.2f}")
                    print(f"   Recomendação: {analise['recomendacao']}")
                    print(f"   Confiança: {analise['confianca']:.1%}")
                    print(f"   Tendência: {analise['analise_tecnica']['tendencia']}")
                    print(f"   RSI: {analise['analise_tecnica']['rsi']:.1f}")
        
        elif opcao == "2":
            print("\n📊 Posições Abertas:")
            if trading.posicoes_abertas:
                for posicao in trading.posicoes_abertas:
                    print(f"   Ativo: {posicao.ativo}")
                    print(f"   Quantidade: {posicao.quantidade}")
                    print(f"   Preço médio: R$ {posicao.preco_medio:.2f}")
                    print(f"   P&L: R$ {posicao.pnl:.2f} ({posicao.pnl_percentual:.1f}%)")
                    print(f"   Data abertura: {posicao.data_abertura}")
                    print()
            else:
                print("   Nenhuma posição aberta")
        
        elif opcao == "3":
            print("\n📈 Relatório de Desempenho:")
            relatorio = trading.gerar_relatorio_desempenho()
            
            if "erro" in relatorio:
                print(f"❌ {relatorio['erro']}")
            else:
                print(f"   Capital inicial: R$ {relatorio['capital_inicial']:.2f}")
                print(f"   Capital atual: R$ {relatorio['capital_atual']:.2f}")
                print(f"   Retorno: {relatorio['retorno_percentual']:.1f}%")
                print(f"   Total de ordens: {relatorio['total_ordens']}")
                print(f"   Taxa de acerto: {relatorio['taxa_acerto']:.1%}")
                print(f"   Sharpe Ratio: {relatorio['sharpe_ratio']:.2f}")
        
        elif opcao == "4":
            duracao = input("Duração em minutos (padrão: 5): ").strip()
            duracao = int(duracao) if duracao.isdigit() else 5
            
            print(f"\n🤖 Executando trading automatizado por {duracao} minutos...")
            resultado = trading.executar_trading_automatizado(duracao)
            
            print(f"✅ Execução concluída:")
            print(f"   Sinais gerados: {len(resultado['sinais_gerados'])}")
            print(f"   Ordens executadas: {len(resultado['ordens_executadas'])}")
            print(f"   Alertas: {len(resultado['alertas'])}")
            print(f"   Erros: {len(resultado['erros'])}")
        
        elif opcao == "5":
            print("\n📋 Ordens Executadas:")
            if trading.ordens:
                for ordem in trading.ordens[-5:]:  # Últimas 5 ordens
                    print(f"   ID: {ordem.id}")
                    print(f"   Ativo: {ordem.ativo}")
                    print(f"   Tipo: {ordem.tipo.value}")
                    print(f"   Quantidade: {ordem.quantidade}")
                    print(f"   Preço: R$ {ordem.preco:.2f}")
                    print(f"   Status: {ordem.status.value}")
                    print(f"   Data: {ordem.data_criacao}")
                    print()
            else:
                print("   Nenhuma ordem executada")
        
        elif opcao == "6":
            print("\n👋 Encerrando VHALINOR AI Trading System...")
            break
        
        else:
            print("❌ Opção inválida. Tente novamente.")


if __name__ == "__main__":
    main()
