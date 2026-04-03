#!/usr/bin/env python3
"""
VHALINOR AI Geral - Dashboard Web
=================================
Dashboard web interativo com FastAPI e Streamlit
"""

import sys
import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

try:
    import streamlit as st
    from streamlit_plotly_events import plotly_events
    import streamlit.components.v1 as components
except ImportError:
    print("Streamlit não instalado. Execute: pip install streamlit streamlit-plotly-events")
    sys.exit(1)

try:
    from consciencia_artificial import ConscienciaArtificial
    from sentiencia_artificial import SentienciaArtificial
    from raciocinio_avancado import RaciocinioAvancado
    from memoria_cognitiva import MemoriaCognitiva
    from aprendizado_profundo import AprendizadoProfundo
    from analise_mercado_financeiro import AnaliseMercadoFinanceiro
    from processamento_linguagem import ProcessamentoLinguagem
    from visao_computacional import VisaoComputacional
    from automacao import AutomacaoInteligente
    from tomada_decisao import TomadaDecisao
except ImportError as e:
    print(f"AVISO: Alguns módulos não disponíveis: {e}")


class VhalinorWebDashboard:
    """Dashboard Web do VHALINOR AI Geral"""
    
    def __init__(self):
        self.version = "6.0.0"
        self.componentes = {}
        self.inicializar_componentes()
        
        # Configuração da página
        st.set_page_config(
            page_title="VHALINOR AI Geral Dashboard",
            page_icon="🧠",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    
    def inicializar_componentes(self):
        """Inicializar componentes do sistema"""
        try:
            self.componentes['consciencia'] = ConscienciaArtificial()
            self.componentes['consciencia'].inicializar()
            
            self.componentes['sentiencia'] = SentienciaArtificial()
            self.componentes['sentiencia'].inicializar()
            
            self.componentes['raciocinio'] = RaciocinioAvancado()
            self.componentes['memoria'] = MemoriaCognitiva()
            self.componentes['aprendizado'] = AprendizadoProfundo()
            self.componentes['mercado'] = AnaliseMercadoFinanceiro()
            self.componentes['linguagem'] = ProcessamentoLinguagem()
            self.componentes['visao'] = VisaoComputacional()
            self.componentes['automacao'] = AutomacaoInteligente()
            self.componentes['decisao'] = TomadaDecisao()
            
        except Exception as e:
            st.error(f"Erro ao inicializar componentes: {e}")
    
    def render_header(self):
        """Renderizar cabeçalho"""
        st.markdown("""
        <div style='background: linear-gradient(90deg, #1a1a2e, #16213e); padding: 20px; border-radius: 10px; margin-bottom: 20px;'>
            <h1 style='color: white; text-align: center; margin: 0;'>🧠 VHALINOR AI Geral Dashboard</h1>
            <p style='color: #b0b0b0; text-align: center; margin: 5px 0 0 0;'>Inteligência Artificial Geral v6.0.0</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Renderizar barra lateral"""
        st.sidebar.markdown("## 🎛️ Controle do Sistema")
        
        # Status do sistema
        st.sidebar.markdown("### 📊 Status")
        
        status_color = "🟢" if len(self.componentes) > 5 else "🟡"
        st.sidebar.markdown(f"{status_color} **{len(self.componentes)}** componentes ativos")
        
        # Componentes ativos
        st.sidebar.markdown("### 🧩 Componentes")
        for nome in self.componentes.keys():
            st.sidebar.markdown(f"✅ {nome.capitalize()}")
        
        # Controles
        st.sidebar.markdown("### ⚙️ Configurações")
        
        auto_refresh = st.sidebar.checkbox("Atualização Automática", value=True)
        refresh_interval = st.sidebar.slider("Intervalo (segundos)", 5, 60, 10)
        
        # Ações
        st.sidebar.markdown("### 🔧 Ações")
        
        if st.sidebar.button("🔄 Atualizar Sistema"):
            st.rerun()
        
        if st.sidebar.button("🧹 Limpar Memória"):
            if 'memoria' in self.componentes:
                try:
                    self.componentes['memoria'].limpar()
                    st.sidebar.success("Memória limpa!")
                except:
                    st.sidebar.error("Erro ao limpar memória")
        
        if st.sidebar.button("📊 Gerar Relatório"):
            self.gerar_relatorio()
        
        return auto_refresh, refresh_interval
    
    def render_overview(self):
        """Renderizar visão geral"""
        st.markdown("## 📈 Visão Geral do Sistema")
        
        # Métricas principais
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Componentes Ativos",
                value=len(self.componentes),
                delta="🟢 Operacional"
            )
        
        with col2:
            mem_usage = self.get_memory_usage()
            st.metric(
                label="Uso de Memória",
                value=f"{mem_usage:.1f}%",
                delta="📊 Monitorado"
            )
        
        with col3:
            uptime = self.get_uptime()
            st.metric(
                label="Tempo Online",
                value=uptime,
                delta="⏰ Ativo"
            )
        
        with col4:
            process_count = self.get_process_count()
            st.metric(
                label="Processos",
                value=process_count,
                delta="🔄 Dinâmico"
            )
        
        # Gráficos de status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 Status dos Componentes")
            self.render_component_status_chart()
        
        with col2:
            st.markdown("### 📊 Performance do Sistema")
            self.render_performance_chart()
    
    def render_component_status_chart(self):
        """Renderizar gráfico de status dos componentes"""
        try:
            # Dados simulados de status
            componentes = list(self.componentes.keys())
            status = np.random.randint(70, 100, len(componentes))
            
            fig = go.Figure(data=[
                go.Bar(
                    x=componentes,
                    y=status,
                    marker_color='lightblue',
                    text=status,
                    textposition='auto',
                )
            ])
            
            fig.update_layout(
                title="Status dos Componentes (%)",
                xaxis_title="Componentes",
                yaxis_title="Status (%)",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao renderizar gráfico de status: {e}")
    
    def render_performance_chart(self):
        """Renderizar gráfico de performance"""
        try:
            # Dados simulados de performance
            horas = list(range(24))
            cpu_usage = np.random.normal(50, 15, 24)
            memory_usage = np.random.normal(60, 10, 24)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=horas,
                y=cpu_usage,
                mode='lines+markers',
                name='CPU (%)',
                line=dict(color='red')
            ))
            
            fig.add_trace(go.Scatter(
                x=horas,
                y=memory_usage,
                mode='lines+markers',
                name='Memória (%)',
                line=dict(color='blue')
            ))
            
            fig.update_layout(
                title="Performance do Sistema (24h)",
                xaxis_title="Horas",
                yaxis_title="Uso (%)",
                height=300,
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao renderizar gráfico de performance: {e}")
    
    def render_chat_interface(self):
        """Renderizar interface de chat"""
        st.markdown("## 💬 Chat com VHALINOR AI")
        
        # Histórico do chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Exibir histórico
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Input do usuário
        user_input = st.chat_input("Digite sua mensagem...")
        
        if user_input:
            # Adicionar mensagem do usuário
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.chat_message("user"):
                st.markdown(user_input)
            
            # Processar resposta
            with st.chat_message("assistant"):
                with st.spinner("VHALINOR está pensando..."):
                    response = self.process_chat_message(user_input)
                    st.markdown(response)
            
            # Adicionar resposta do assistente
            st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    def process_chat_message(self, message: str) -> str:
        """Processar mensagem do chat"""
        try:
            if 'raciocinio' in self.componentes:
                resposta = self.componentes['raciocinio'].processar_pergunta(message)
            else:
                # Resposta simulada
                respostas = [
                    f"Entendi sua pergunta sobre '{message}'. Estou processando...",
                    f"Interessante! Sua mensagem '{message}' me faz pensar sobre...",
                    f"Analisando '{message}', posso dizer que...",
                    f"Sobre '{message}', minha análise é..."
                ]
                resposta = np.random.choice(respostas)
            
            # Armazenar na memória
            if 'memoria' in self.componentes:
                self.componentes['memoria'].armazenar_interacao(message, resposta)
            
            return resposta
            
        except Exception as e:
            return f"Erro ao processar mensagem: {e}"
    
    def render_market_analysis(self):
        """Renderizar análise de mercado"""
        st.markdown("## 📈 Análise de Mercado")
        
        # Input de ativo
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ativo = st.text_input("Código do Ativo", value="PETR4", placeholder="Ex: PETR4, VALE3, ITUB4")
        
        with col2:
            timeframe = st.selectbox("Timeframe", ["1m", "5m", "15m", "1h", "1d", "1w"], index=4)
        
        if st.button("🔍 Analisar Ativo"):
            with st.spinner(f"Analisando {ativo}..."):
                resultado = self.analisar_ativo_mercado(ativo, timeframe)
                
                # Exibir resultados
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Preço Atual", f"R$ {resultado.get('preco', 0):.2f}")
                
                with col2:
                    tendencia = resultado.get('tendencia', 'neutra')
                    emoji = "📈" if tendencia == "alta" else "📉" if tendencia == "baixa" else "➡️"
                    st.metric("Tendência", f"{emoji} {tendencia.capitalize()}")
                
                with col3:
                    recomendacao = resultado.get('recomendacao', 'manter')
                    emoji = "🟢" if recomendacao == "comprar" else "🔴" if recomendacao == "vender" else "🟡"
                    st.metric("Recomendação", f"{emoji} {recomendacao.capitalize()}")
                
                # Gráfico de preços
                self.render_price_chart(ativo, timeframe)
                
                # Análise detalhada
                with st.expander("📊 Análise Detalhada"):
                    st.json(resultado)
    
    def analisar_ativo_mercado(self, ativo: str, timeframe: str) -> Dict[str, Any]:
        """Analisar ativo do mercado"""
        try:
            if 'mercado' in self.componentes:
                resultado = self.componentes['mercado'].analisar_ativo(ativo, timeframe)
            else:
                # Análise simulada
                resultado = {
                    "ativo": ativo,
                    "preco": np.random.uniform(20, 50),
                    "tendencia": np.random.choice(["alta", "baixa", "lateral"]),
                    "recomendacao": np.random.choice(["comprar", "vender", "manter"]),
                    "volume": np.random.uniform(1000000, 50000000),
                    "volatilidade": np.random.uniform(0.1, 0.5),
                    "rsi": np.random.uniform(20, 80),
                    "macd": np.random.uniform(-2, 2),
                    "timestamp": datetime.now().isoformat()
                }
            
            return resultado
            
        except Exception as e:
            return {"erro": f"Falha na análise: {e}"}
    
    def render_price_chart(self, ativo: str, timeframe: str):
        """Renderizar gráfico de preços"""
        try:
            # Dados simulados
            periods = {"1m": 60, "5m": 288, "15m": 96, "1h": 24, "1d": 30, "1w": 12}
            n_periods = periods.get(timeframe, 30)
            
            datas = pd.date_range(end=datetime.now(), periods=n_periods, freq='H')
            precos = np.random.uniform(20, 50, n_periods).cumsum()
            
            # Criar gráfico candlestick simulado
            fig = make_subplots(
                rows=2, cols=1,
                shared_xaxes=True,
                vertical_spacing=0.1,
                subplot_titles=(f'{ativo} - Preços', 'Volume'),
                row_heights=[0.7, 0.3]
            )
            
            # Gráfico de preços
            fig.add_trace(
                go.Scatter(
                    x=datas,
                    y=precos,
                    mode='lines',
                    name='Preço',
                    line=dict(color='blue', width=2)
                ),
                row=1, col=1
            )
            
            # Médias móveis
            ma_short = pd.Series(precos).rolling(window=5).mean()
            ma_long = pd.Series(precos).rolling(window=10).mean()
            
            fig.add_trace(
                go.Scatter(
                    x=datas,
                    y=ma_short,
                    mode='lines',
                    name='MA 5',
                    line=dict(color='orange', width=1)
                ),
                row=1, col=1
            )
            
            fig.add_trace(
                go.Scatter(
                    x=datas,
                    y=ma_long,
                    mode='lines',
                    name='MA 10',
                    line=dict(color='red', width=1)
                ),
                row=1, col=1
            )
            
            # Volume
            volume = np.random.uniform(1000000, 10000000, n_periods)
            
            fig.add_trace(
                go.Bar(
                    x=datas,
                    y=volume,
                    name='Volume',
                    marker_color='lightblue'
                ),
                row=2, col=1
            )
            
            fig.update_layout(
                title=f'Gráfico de {ativo} - {timeframe}',
                height=600,
                showlegend=True,
                xaxis_rangeslider_visible=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Erro ao renderizar gráfico: {e}")
    
    def render_nlp_interface(self):
        """Renderizar interface NLP"""
        st.markdown("## 📝 Processamento de Linguagem Natural")
        
        # Input de texto
        texto_input = st.text_area(
            "Digite o texto para análise:",
            height=150,
            placeholder="Digite ou cole o texto que deseja analisar..."
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔍 Analisar Texto"):
                if texto_input:
                    with st.spinner("Analisando texto..."):
                        resultado = self.analisar_texto_nlp(texto_input)
                        self.exibir_resultados_nlp(resultado)
                else:
                    st.warning("Digite um texto para analisar")
        
        with col2:
            if st.button("📊 Análise Avançada"):
                if texto_input:
                    with st.spinner("Análise avançada..."):
                        resultado = self.analise_avancada_nlp(texto_input)
                        self.exibir_analise_avancada(resultado)
                else:
                    st.warning("Digite um texto para analisar")
    
    def analisar_texto_nlp(self, texto: str) -> Dict[str, Any]:
        """Analisar texto com NLP"""
        try:
            if 'linguagem' in self.componentes:
                resultado = self.componentes['linguagem'].analisar_completo(texto)
            else:
                # Análise simulada
                resultado = {
                    "sentimento": np.random.choice(["positivo", "negativo", "neutro"]),
                    "confianca": np.random.uniform(0.7, 1.0),
                    "entidades": ["VHALINOR", "IA", "Mercado"],
                    "categorias": ["tecnologia", "inovação"],
                    "palavras_chave": ["inteligência", "artificial", "sistema"],
                    "idioma": "pt",
                    "comprimento": len(texto),
                    "complexidade": np.random.uniform(0.3, 0.9)
                }
            
            return resultado
            
        except Exception as e:
            return {"erro": f"Falha na análise: {e}"}
    
    def exibir_resultados_nlp(self, resultado: Dict[str, Any]):
        """Exibir resultados da análise NLP"""
        if "erro" in resultado:
            st.error(resultado["erro"])
            return
        
        # Métricas principais
        col1, col2, col3 = st.columns(3)
        
        with col1:
            sentimento = resultado.get('sentimento', 'neutro')
            emoji = "😊" if sentimento == "positivo" else "😔" if sentimento == "negativo" else "😐"
            st.metric("Sentimento", f"{emoji} {sentimento.capitalize()}")
        
        with col2:
            confianca = resultado.get('confianca', 0)
            st.metric("Confiança", f"{confianca:.1%}")
        
        with col3:
            complexidade = resultado.get('complexidade', 0)
            st.metric("Complexidade", f"{complexidade:.1%}")
        
        # Detalhes
        with st.expander("📊 Detalhes da Análise"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Entidades Detectadas:**")
                for entidade in resultado.get('entidades', []):
                    st.markdown(f"• {entidade}")
                
                st.markdown("**Categorias:**")
                for categoria in resultado.get('categorias', []):
                    st.markdown(f"• {categoria}")
            
            with col2:
                st.markdown("**Palavras-chave:**")
                for palavra in resultado.get('palavras_chave', []):
                    st.markdown(f"• {palavra}")
                
                st.markdown("**Informações:**")
                st.markdown(f"• Idioma: {resultado.get('idioma', 'N/A')}")
                st.markdown(f"• Comprimento: {resultado.get('comprimento', 0)} caracteres")
    
    def analise_avancada_nlp(self, texto: str) -> Dict[str, Any]:
        """Análise avançada de texto"""
        try:
            # Análise emocional
            emocional = {}
            if 'sentiencia' in self.componentes:
                emocional = self.componentes['sentiencia'].analisar_sentimento_texto(texto)
            else:
                emocional = {
                    "alegria": np.random.uniform(0, 1),
                    "tristeza": np.random.uniform(0, 1),
                    "raiva": np.random.uniform(0, 1),
                    "medo": np.random.uniform(0, 1),
                    "surpresa": np.random.uniform(0, 1)
                }
            
            # Resumo do texto
            palavras = len(texto.split())
            frases = texto.count('.') + texto.count('!') + texto.count('?')
            
            return {
                "analise_emocional": emocional,
                "estatisticas": {
                    "palavras": palavras,
                    "frases": frases,
                    "paragrafos": texto.count('\n\n') + 1,
                    "media_palavras_por_frase": palavras / max(frases, 1)
                },
                "legibilidade": {
                    "score": np.random.uniform(0, 100),
                    "nivel": np.random.choice(["fácil", "médio", "difícil"])
                }
            }
            
        except Exception as e:
            return {"erro": f"Falha na análise avançada: {e}"}
    
    def exibir_analise_avancada(self, resultado: Dict[str, Any]):
        """Exibir análise avançada"""
        if "erro" in resultado:
            st.error(resultado["erro"])
            return
        
        # Análise emocional
        if "analise_emocional" in resultado:
            st.markdown("### 😊 Análise Emocional")
            
            emocional = resultado["analise_emocional"]
            emocoes = list(emocional.keys())
            valores = list(emocional.values())
            
            fig = go.Figure(data=[
                go.Bar(x=emocoes, y=valores, marker_color='lightcoral')
            ])
            
            fig.update_layout(
                title="Perfil Emocional",
                xaxis_title="Emoções",
                yaxis_title="Intensidade",
                height=300
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Estatísticas
        if "estatisticas" in resultado:
            st.markdown("### 📊 Estatísticas do Texto")
            
            stats = resultado["estatisticas"]
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Palavras", stats.get("palavras", 0))
            
            with col2:
                st.metric("Frases", stats.get("frases", 0))
            
            with col3:
                st.metric("Parágrafos", stats.get("paragrafos", 0))
            
            with col4:
                media = stats.get("media_palavras_por_frase", 0)
                st.metric("Média p/ frase", f"{media:.1f}")
    
    def render_automation_interface(self):
        """Renderizar interface de automação"""
        st.markdown("## 🤖 Automação Inteligente")
        
        # Input de tarefa
        tarefa_input = st.text_input(
            "Descreva a tarefa para automatizar:",
            placeholder="Ex: analisar dados do mercado, gerar relatório, enviar email..."
        )
        
        # Configurações da automação
        col1, col2 = st.columns(2)
        
        with col1:
            prioridade = st.selectbox("Prioridade", ["baixa", "média", "alta", "urgente"])
            repeticao = st.selectbox("Repetição", ["única", "diária", "semanal", "mensal"])
        
        with col2:
            agendamento = st.time_input("Agendar para", datetime.now().time())
            notificacao = st.checkbox("Enviar notificação", value=True)
        
        if st.button("🚀 Executar Automação"):
            if tarefa_input:
                with st.spinner("Executando automação..."):
                    resultado = self.executar_automacao(tarefa_input, {
                        "prioridade": prioridade,
                        "repeticao": repeticao,
                        "agendamento": str(agendamento),
                        "notificacao": notificacao
                    })
                    
                    self.exibir_resultado_automacao(resultado)
            else:
                st.warning("Descreva a tarefa para automatizar")
        
        # Histórico de automações
        st.markdown("### 📋 Histórico de Automações")
        
        # Dados simulados de histórico
        historico = [
            {"tarefa": "Análise de PETR4", "status": "concluído", "data": "2026-04-01 14:30"},
            {"tarefa": "Geração de relatório", "status": "executando", "data": "2026-04-01 14:45"},
            {"tarefa": "Análise de sentimento", "status": "agendado", "data": "2026-04-01 15:00"},
        ]
        
        df_historico = pd.DataFrame(historico)
        st.dataframe(df_historico, use_container_width=True)
    
    def executar_automacao(self, tarefa: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Executar tarefa automatizada"""
        try:
            if 'automacao' in self.componentes:
                resultado = self.componentes['automacao'].executar_tarefa(tarefa)
            else:
                # Simulação de execução
                import time
                time.sleep(2)  # Simular tempo de processamento
                
                resultado = {
                    "status": "concluído",
                    "tarefa": tarefa,
                    "config": config,
                    "resultado": f"Tarefa '{tarefa}' executada com sucesso",
                    "tempo_execucao": f"{np.random.uniform(1, 5):.2f}s",
                    "data_conclusao": datetime.now().isoformat(),
                    "logs": [
                        "Iniciando execução...",
                        "Processando parâmetros...",
                        "Executando análise...",
                        "Gerando resultados...",
                        "Concluído com sucesso!"
                    ]
                }
            
            return resultado
            
        except Exception as e:
            return {
                "status": "erro",
                "erro": f"Falha na execução: {e}",
                "data_erro": datetime.now().isoformat()
            }
    
    def exibir_resultado_automacao(self, resultado: Dict[str, Any]):
        """Exibir resultado da automação"""
        status = resultado.get("status", "desconhecido")
        
        if status == "concluído":
            st.success("✅ Automação concluída com sucesso!")
        elif status == "executando":
            st.info("🔄 Automação em execução...")
        elif status == "erro":
            st.error("❌ Erro na automação")
        
        # Detalhes
        with st.expander("📋 Detalhes da Execução"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Informações:**")
                st.markdown(f"• Tarefa: {resultado.get('tarefa', 'N/A')}")
                st.markdown(f"• Status: {status}")
                st.markdown(f"• Tempo: {resultado.get('tempo_execucao', 'N/A')}")
            
            with col2:
                st.markdown("**Resultado:**")
                st.text_area("", value=resultado.get('resultado', 'N/A'), height=100, disabled=True)
            
            # Logs
            if "logs" in resultado:
                st.markdown("**Logs de Execução:**")
                for log in resultado["logs"]:
                    st.markdown(f"• {log}")
    
    def get_memory_usage(self) -> float:
        """Obter uso de memória simulado"""
        try:
            import psutil
            return psutil.virtual_memory().percent
        except:
            return np.random.uniform(30, 70)
    
    def get_uptime(self) -> str:
        """Obter tempo online simulado"""
        minutos = np.random.randint(60, 1440)
        horas = minutos // 60
        mins = minutos % 60
        return f"{horas}h {mins}min"
    
    def get_process_count(self) -> int:
        """Obter número de processos simulado"""
        try:
            import psutil
            return len(psutil.pids())
        except:
            return np.random.randint(50, 150)
    
    def gerar_relatorio(self):
        """Gerar relatório do sistema"""
        st.success("📊 Relatório gerado com sucesso!")
        
        relatorio = {
            "data_geracao": datetime.now().isoformat(),
            "versao": self.version,
            "componentes": len(self.componentes),
            "status": "operacional",
            "metricas": {
                "memoria": self.get_memory_usage(),
                "uptime": self.get_uptime(),
                "processos": self.get_process_count()
            }
        }
        
        st.json(relatorio)
    
    def run(self):
        """Executar dashboard"""
        # Renderizar componentes principais
        self.render_header()
        auto_refresh, refresh_interval = self.render_sidebar()
        
        # Navegação
        pagina = st.selectbox(
            "📋 Selecione uma página:",
            ["Visão Geral", "Chat IA", "Análise de Mercado", "Processamento NLP", "Automação"],
            index=0
        )
        
        # Renderizar página selecionada
        if pagina == "Visão Geral":
            self.render_overview()
        elif pagina == "Chat IA":
            self.render_chat_interface()
        elif pagina == "Análise de Mercado":
            self.render_market_analysis()
        elif pagina == "Processamento NLP":
            self.render_nlp_interface()
        elif pagina == "Automação":
            self.render_automation_interface()
        
        # Auto refresh
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()


def main():
    """Função principal"""
    try:
        dashboard = VhalinorWebDashboard()
        dashboard.run()
    except Exception as e:
        st.error(f"Erro ao iniciar dashboard: {e}")


if __name__ == "__main__":
    main()
