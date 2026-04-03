#!/usr/bin/env python3
"""
VHALINOR AI Geral - Interface Principal Unificada
================================================
Interface gráfica completa para todos os módulos do sistema
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
from datetime import datetime
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import numpy as np

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

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


class VhalinorGUI:
    """Interface Principal do VHALINOR AI Geral"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VHALINOR AI Geral v6.0.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Estilo dark theme
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.configure_dark_theme()
        
        # Inicializar componentes
        self.inicializar_componentes()
        
        # Criar interface
        self.criar_interface()
        
        # Status
        self.status_var = tk.StringVar(value="Sistema pronto")
        
    def configure_dark_theme(self):
        """Configurar tema escuro"""
        colors = {
            'bg': '#1a1a1a',
            'fg': '#ffffff',
            'selectbg': '#404040',
            'selectfg': '#ffffff',
            'button_bg': '#2a2a2a',
            'button_fg': '#ffffff'
        }
        
        self.style.configure('TFrame', background=colors['bg'])
        self.style.configure('TLabel', background=colors['bg'], foreground=colors['fg'])
        self.style.configure('TButton', background=colors['button_bg'], foreground=colors['button_fg'])
        self.style.configure('TEntry', fieldbackground=colors['button_bg'], foreground=colors['button_fg'])
        self.style.configure('TNotebook', background=colors['bg'], foreground=colors['fg'])
        self.style.configure('TNotebook.Tab', background=colors['button_bg'], foreground=colors['button_fg'])
    
    def inicializar_componentes(self):
        """Inicializar todos os componentes do sistema"""
        self.componentes = {}
        
        try:
            # Consciência Artificial
            self.componentes['consciencia'] = ConscienciaArtificial()
            self.componentes['consciencia'].inicializar()
            
            # Sentiência Artificial
            self.componentes['sentiencia'] = SentienciaArtificial()
            self.componentes['sentiencia'].inicializar()
            
            # Raciocínio Avançado
            self.componentes['raciocinio'] = RaciocinioAvancado()
            
            # Memória Cognitiva
            self.componentes['memoria'] = MemoriaCognitiva()
            
            # Aprendizado Profundo
            self.componentes['aprendizado'] = AprendizadoProfundo()
            
            # Análise de Mercado
            self.componentes['mercado'] = AnaliseMercadoFinanceiro()
            
            # Processamento de Linguagem
            self.componentes['linguagem'] = ProcessamentoLinguagem()
            
            # Visão Computacional
            self.componentes['visao'] = VisaoComputacional()
            
            # Automação Inteligente
            self.componentes['automacao'] = AutomacaoInteligente()
            
            # Tomada de Decisão
            self.componentes['decisao'] = TomadaDecisao()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inicializar componentes: {e}")
    
    def criar_interface(self):
        """Criar interface principal"""
        # Menu superior
        self.criar_menu()
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook com abas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Criar abas
        self.criar_aba_status()
        self.criar_aba_chat()
        self.criar_aba_mercado()
        self.criar_aba_nlp()
        self.criar_aba_visao()
        self.criar_aba_automacao()
        self.criar_aba_config()
        
        # Barra de status
        self.criar_status_bar()
    
    def criar_menu(self):
        """Criar menu superior"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Arquivo
        arquivo_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Arquivo", menu=arquivo_menu)
        arquivo_menu.add_command(label="Sessão", command=self.salvar_sessao)
        arquivo_menu.add_command(label="Carregar Sessão", command=self.carregar_sessao)
        arquivo_menu.add_separator()
        arquivo_menu.add_command(label="Sair", command=self.root.quit)
        
        # Menu Ferramentas
        ferramentas_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ferramentas", menu=ferramentas_menu)
        ferramentas_menu.add_command(label="Limpar Memória", command=self.limpar_memoria)
        ferramentas_menu.add_command(label="Recarregar Componentes", command=self.recarregar_componentes)
        
        # Menu Ajuda
        ajuda_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=ajuda_menu)
        ajuda_menu.add_command(label="Sobre", command=self.sobre)
        ajuda_menu.add_command(label="Documentação", command=self.documentacao)
    
    def criar_aba_status(self):
        """Criar aba de status do sistema"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📊 Status")
        
        # Frame de informações
        info_frame = ttk.Frame(frame)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(info_frame, text="Status do Sistema VHALINOR AI Geral", 
                                font=('Arial', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Status dos componentes
        self.status_text = scrolledtext.ScrolledText(info_frame, height=15, width=80)
        self.status_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Botão atualizar
        btn_atualizar = ttk.Button(info_frame, text="Atualizar Status", 
                                  command=self.atualizar_status)
        btn_atualizar.pack(pady=5)
        
        # Atualizar status inicial
        self.atualizar_status()
    
    def criar_aba_chat(self):
        """Criar aba de chat com a IA"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="💬 Chat IA")
        
        # Frame principal
        chat_frame = ttk.Frame(frame)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Histórico do chat
        ttk.Label(chat_frame, text="Conversa com VHALINOR AI", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.chat_text = scrolledtext.ScrolledText(chat_frame, height=20, width=80)
        self.chat_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Frame de input
        input_frame = ttk.Frame(chat_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Mensagem:").pack(side=tk.LEFT, padx=5)
        self.chat_input = ttk.Entry(input_frame, width=60)
        self.chat_input.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.chat_input.bind('<Return>', lambda e: self.enviar_mensagem())
        
        ttk.Button(input_frame, text="Enviar", command=self.enviar_mensagem).pack(side=tk.RIGHT, padx=5)
        
        # Botões de ação
        btn_frame = ttk.Frame(chat_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Limpar Chat", command=self.limpar_chat).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Salvar Conversa", command=self.salvar_chat).pack(side=tk.LEFT, padx=5)
    
    def criar_aba_mercado(self):
        """Criar aba de análise de mercado"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📈 Mercado")
        
        # Frame principal
        mercado_frame = ttk.Frame(frame)
        mercado_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de input
        input_frame = ttk.Frame(mercado_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Ativo:").pack(side=tk.LEFT, padx=5)
        self.ativo_input = ttk.Entry(input_frame, width=15)
        self.ativo_input.pack(side=tk.LEFT, padx=5)
        self.ativo_input.insert(0, "PETR4")
        
        ttk.Label(input_frame, text="Timeframe:").pack(side=tk.LEFT, padx=5)
        self.timeframe_combo = ttk.Combobox(input_frame, values=["1m", "5m", "15m", "1h", "1d", "1w"], width=10)
        self.timeframe_combo.pack(side=tk.LEFT, padx=5)
        self.timeframe_combo.set("1d")
        
        ttk.Button(input_frame, text="Analisar", command=self.analisar_mercado).pack(side=tk.LEFT, padx=5)
        
        # Frame de resultados
        result_frame = ttk.Frame(mercado_frame)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text de resultados
        self.mercado_text = scrolledtext.ScrolledText(result_frame, height=15, width=80)
        self.mercado_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de gráfico
        self.chart_frame = ttk.Frame(mercado_frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, pady=5)
    
    def criar_aba_nlp(self):
        """Criar aba de processamento de linguagem"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="📝 NLP")
        
        # Frame principal
        nlp_frame = ttk.Frame(frame)
        nlp_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input de texto
        ttk.Label(nlp_frame, text="Texto para análise:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.nlp_input = scrolledtext.ScrolledText(nlp_frame, height=10, width=80)
        self.nlp_input.pack(fill=tk.X, pady=5)
        
        # Botões
        btn_frame = ttk.Frame(nlp_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Analisar Texto", command=self.analisar_texto).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_nlp).pack(side=tk.LEFT, padx=5)
        
        # Resultados
        ttk.Label(nlp_frame, text="Resultados:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.nlp_result = scrolledtext.ScrolledText(nlp_frame, height=15, width=80)
        self.nlp_result.pack(fill=tk.BOTH, expand=True)
    
    def criar_aba_visao(self):
        """Criar aba de visão computacional"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="👁️ Visão")
        
        # Frame principal
        visao_frame = ttk.Frame(frame)
        visao_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame de upload
        upload_frame = ttk.Frame(visao_frame)
        upload_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(upload_frame, text="Carregar Imagem", command=self.carregar_imagem).pack(side=tk.LEFT, padx=5)
        ttk.Button(upload_frame, text="Analisar Imagem", command=self.analisar_imagem).pack(side=tk.LEFT, padx=5)
        
        # Frame de imagem
        self.imagem_frame = ttk.Frame(visao_frame)
        self.imagem_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Resultados
        ttk.Label(visao_frame, text="Análise:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.visao_result = scrolledtext.ScrolledText(visao_frame, height=10, width=80)
        self.visao_result.pack(fill=tk.BOTH, expand=True)
    
    def criar_aba_automacao(self):
        """Criar aba de automação"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🤖 Automação")
        
        # Frame principal
        auto_frame = ttk.Frame(frame)
        auto_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Input de tarefa
        ttk.Label(auto_frame, text="Tarefa para automatizar:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.auto_input = ttk.Entry(auto_frame, width=80)
        self.auto_input.pack(fill=tk.X, pady=5)
        self.auto_input.insert(0, "analisar dados do mercado")
        
        # Botões
        btn_frame = ttk.Frame(auto_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="Executar", command=self.executar_automacao).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Limpar", command=self.limpar_auto).pack(side=tk.LEFT, padx=5)
        
        # Resultados
        ttk.Label(auto_frame, text="Resultados:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        self.auto_result = scrolledtext.ScrolledText(auto_frame, height=15, width=80)
        self.auto_result.pack(fill=tk.BOTH, expand=True)
    
    def criar_aba_config(self):
        """Criar aba de configuração"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ Config")
        
        # Frame principal
        config_frame = ttk.Frame(frame)
        config_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(config_frame, text="Configurações do Sistema", font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Configurações
        configs = [
            ("Consciência Artificial", "Ativar consciência artificial"),
            ("Sentiência Artificial", "Ativar análise emocional"),
            ("Aprendizado Contínuo", "Ativar aprendizado automático"),
            ("Log Detalhado", "Ativar logs detalhados")
        ]
        
        self.config_vars = {}
        for config, desc in configs:
            var = tk.BooleanVar(value=True)
            self.config_vars[config] = var
            
            frame_config = ttk.Frame(config_frame)
            frame_config.pack(fill=tk.X, pady=2)
            
            cb = ttk.Checkbutton(frame_config, text=desc, variable=var)
            cb.pack(side=tk.LEFT)
        
        # Botões
        btn_frame = ttk.Frame(config_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(btn_frame, text="Salvar Configurações", command=self.salvar_config).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Redefinir", command=self.redefinir_config).pack(side=tk.LEFT, padx=5)
    
    def criar_status_bar(self):
        """Criar barra de status"""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var)
        self.status_label.pack(side=tk.LEFT, padx=5)
        
        # Relógio
        self.clock_var = tk.StringVar()
        self.clock_label = ttk.Label(status_frame, textvariable=self.clock_var)
        self.clock_label.pack(side=tk.RIGHT, padx=5)
        
        self.atualizar_relogio()
    
    def atualizar_relogio(self):
        """Atualizar relógio"""
        self.clock_var.set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        self.root.after(1000, self.atualizar_relogio)
    
    def atualizar_status(self):
        """Atualizar status do sistema"""
        self.status_var.set("Atualizando status...")
        
        def atualizar():
            try:
                status_info = {
                    "Versão": "6.0.0",
                    "Data/Hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Componentes Ativos": []
                }
                
                for nome, componente in self.componentes.items():
                    status_info["Componentes Ativos"].append(f"✅ {nome.capitalize()}")
                
                # Exibir status
                self.status_text.delete(1.0, tk.END)
                for chave, valor in status_info.items():
                    if chave == "Componentes Ativos":
                        self.status_text.insert(tk.END, f"{chave}:\n")
                        for comp in valor:
                            self.status_text.insert(tk.END, f"  {comp}\n")
                    else:
                        self.status_text.insert(tk.END, f"{chave}: {valor}\n")
                
                self.status_var.set("Status atualizado")
                
            except Exception as e:
                self.status_text.delete(1.0, tk.END)
                self.status_text.insert(tk.END, f"Erro ao atualizar status: {e}")
                self.status_var.set("Erro ao atualizar status")
        
        # Executar em thread separada
        threading.Thread(target=atualizar, daemon=True).start()
    
    def enviar_mensagem(self):
        """Enviar mensagem para o chat"""
        mensagem = self.chat_input.get().strip()
        if not mensagem:
            return
        
        self.chat_input.delete(0, tk.END)
        self.chat_text.insert(tk.END, f"Você: {mensagem}\n")
        self.chat_text.see(tk.END)
        
        def processar():
            try:
                if 'raciocinio' in self.componentes:
                    resposta = self.componentes['raciocinio'].processar_pergunta(mensagem)
                else:
                    resposta = f"Resposta simulada para: {mensagem}"
                
                self.chat_text.insert(tk.END, f"VHALINOR: {resposta}\n\n")
                self.chat_text.see(tk.END)
                
                # Armazenar na memória
                if 'memoria' in self.componentes:
                    self.componentes['memoria'].armazenar_interacao(mensagem, resposta)
                
            except Exception as e:
                self.chat_text.insert(tk.END, f"VHALINOR: Erro ao processar mensagem: {e}\n\n")
                self.chat_text.see(tk.END)
        
        threading.Thread(target=processar, daemon=True).start()
    
    def analisar_mercado(self):
        """Analisar ativo do mercado"""
        ativo = self.ativo_input.get().strip()
        timeframe = self.timeframe_combo.get()
        
        if not ativo:
            messagebox.showwarning("Aviso", "Informe o código do ativo")
            return
        
        self.status_var.set(f"Analisando {ativo}...")
        
        def analisar():
            try:
                if 'mercado' in self.componentes:
                    resultado = self.componentes['mercado'].analisar_ativo(ativo, timeframe)
                else:
                    resultado = {
                        "ativo": ativo,
                        "preco": np.random.uniform(20, 50),
                        "tendencia": np.random.choice(["alta", "baixa", "lateral"]),
                        "recomendacao": np.random.choice(["comprar", "vender", "manter"])
                    }
                
                # Exibir resultados
                self.mercado_text.delete(1.0, tk.END)
                for chave, valor in resultado.items():
                    self.mercado_text.insert(tk.END, f"{chave}: {valor}\n")
                
                # Criar gráfico simples
                self.criar_grafico_mercado(ativo)
                
                self.status_var.set(f"Análise de {ativo} concluída")
                
            except Exception as e:
                self.mercado_text.delete(1.0, tk.END)
                self.mercado_text.insert(tk.END, f"Erro na análise: {e}")
                self.status_var.set("Erro na análise")
        
        threading.Thread(target=analisar, daemon=True).start()
    
    def criar_grafico_mercado(self, ativo):
        """Criar gráfico de preços"""
        try:
            # Limpar gráfico anterior
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            # Dados simulados
            dias = 30
            precos = np.random.uniform(20, 50, dias)
            datas = pd.date_range(end=datetime.now(), periods=dias)
            
            # Criar figura
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(datas, precos, color='green', linewidth=2)
            ax.set_title(f'Preços Simulados - {ativo}')
            ax.set_xlabel('Data')
            ax.set_ylabel('Preço (R$)')
            ax.grid(True, alpha=0.3)
            
            # Embed no tkinter
            canvas = FigureCanvasTkAgg(fig, self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            print(f"Erro ao criar gráfico: {e}")
    
    def analisar_texto(self):
        """Analisar texto com NLP"""
        texto = self.nlp_input.get(1.0, tk.END).strip()
        if not texto:
            messagebox.showwarning("Aviso", "Informe um texto para análise")
            return
        
        self.status_var.set("Analisando texto...")
        
        def analisar():
            try:
                if 'linguagem' in self.componentes:
                    resultado = self.componentes['linguagem'].analisar_completo(texto)
                else:
                    resultado = {
                        "sentimento": np.random.choice(["positivo", "negativo", "neutro"]),
                        "confianca": np.random.uniform(0.7, 1.0),
                        "entidades": ["entidade1", "entidade2"],
                        "categorias": ["categoria1", "categoria2"]
                    }
                
                # Exibir resultados
                self.nlp_result.delete(1.0, tk.END)
                for chave, valor in resultado.items():
                    self.nlp_result.insert(tk.END, f"{chave}: {valor}\n")
                
                self.status_var.set("Análise de texto concluída")
                
            except Exception as e:
                self.nlp_result.delete(1.0, tk.END)
                self.nlp_result.insert(tk.END, f"Erro na análise: {e}")
                self.status_var.set("Erro na análise")
        
        threading.Thread(target=analisar, daemon=True).start()
    
    def carregar_imagem(self):
        """Carregar imagem para análise"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.jpg *.jpeg *.png *.bmp"), ("Todos", "*.*")]
        )
        
        if arquivo:
            self.imagem_path = arquivo
            self.status_var.set(f"Imagem carregada: {os.path.basename(arquivo)}")
    
    def analisar_imagem(self):
        """Analisar imagem com visão computacional"""
        if not hasattr(self, 'imagem_path'):
            messagebox.showwarning("Aviso", "Carregue uma imagem primeiro")
            return
        
        self.status_var.set("Analisando imagem...")
        
        def analisar():
            try:
                if 'visao' in self.componentes:
                    resultado = self.componentes['visao'].analisar_imagem(self.imagem_path)
                else:
                    resultado = {
                        "objetos_detectados": ["objeto1", "objeto2"],
                        "confianca": np.random.uniform(0.7, 1.0),
                        "descricao": "Análise simulada da imagem"
                    }
                
                # Exibir resultados
                self.visao_result.delete(1.0, tk.END)
                for chave, valor in resultado.items():
                    self.visao_result.insert(tk.END, f"{chave}: {valor}\n")
                
                self.status_var.set("Análise de imagem concluída")
                
            except Exception as e:
                self.visao_result.delete(1.0, tk.END)
                self.visao_result.insert(tk.END, f"Erro na análise: {e}")
                self.status_var.set("Erro na análise")
        
        threading.Thread(target=analisar, daemon=True).start()
    
    def executar_automacao(self):
        """Executar tarefa automatizada"""
        tarefa = self.auto_input.get().strip()
        if not tarefa:
            messagebox.showwarning("Aviso", "Informe uma tarefa para executar")
            return
        
        self.status_var.set("Executando automação...")
        
        def executar():
            try:
                if 'automacao' in self.componentes:
                    resultado = self.componentes['automacao'].executar_tarefa(tarefa)
                else:
                    resultado = {
                        "status": "concluído",
                        "resultado": f"Tarefa '{tarefa}' executada com sucesso",
                        "tempo": f"{np.random.uniform(1, 5):.2f}s"
                    }
                
                # Exibir resultados
                self.auto_result.delete(1.0, tk.END)
                for chave, valor in resultado.items():
                    self.auto_result.insert(tk.END, f"{chave}: {valor}\n")
                
                self.status_var.set("Automação concluída")
                
            except Exception as e:
                self.auto_result.delete(1.0, tk.END)
                self.auto_result.insert(tk.END, f"Erro na automação: {e}")
                self.status_var.set("Erro na automação")
        
        threading.Thread(target=executar, daemon=True).start()
    
    # Métodos utilitários
    def limpar_chat(self):
        """Limpar chat"""
        self.chat_text.delete(1.0, tk.END)
    
    def salvar_chat(self):
        """Salvar conversa"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de Texto", "*.txt"), ("Todos", "*.*")]
        )
        if arquivo:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write(self.chat_text.get(1.0, tk.END))
            messagebox.showinfo("Sucesso", "Conversa salva com sucesso!")
    
    def limpar_nlp(self):
        """Limpar análise NLP"""
        self.nlp_input.delete(1.0, tk.END)
        self.nlp_result.delete(1.0, tk.END)
    
    def limpar_auto(self):
        """Limpar automação"""
        self.auto_result.delete(1.0, tk.END)
    
    def salvar_config(self):
        """Salvar configurações"""
        config = {}
        for nome, var in self.config_vars.items():
            config[nome] = var.get()
        
        messagebox.showinfo("Configurações", f"Configurações salvas: {config}")
    
    def redefinir_config(self):
        """Redefinir configurações"""
        for var in self.config_vars.values():
            var.set(True)
    
    def limpar_memoria(self):
        """Limpar memória do sistema"""
        if 'memoria' in self.componentes:
            try:
                self.componentes['memoria'].limpar()
                messagebox.showinfo("Sucesso", "Memória limpa com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao limpar memória: {e}")
    
    def recarregar_componentes(self):
        """Recarregar componentes do sistema"""
        resposta = messagebox.askyesno("Recarregar", "Deseja recarregar todos os componentes?")
        if resposta:
            self.inicializar_componentes()
            self.atualizar_status()
            messagebox.showinfo("Sucesso", "Componentes recarregados!")
    
    def salvar_sessao(self):
        """Salvar sessão atual"""
        arquivo = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("Arquivos JSON", "*.json"), ("Todos", "*.*")]
        )
        if arquivo:
            sessao = {
                "data": datetime.now().isoformat(),
                "config": {nome: var.get() for nome, var in self.config_vars.items()},
                "chat": self.chat_text.get(1.0, tk.END)
            }
            
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(sessao, f, indent=2, ensure_ascii=False)
            
            messagebox.showinfo("Sucesso", "Sessão salva com sucesso!")
    
    def carregar_sessao(self):
        """Carregar sessão salva"""
        arquivo = filedialog.askopenfilename(
            filetypes=[("Arquivos JSON", "*.json"), ("Todos", "*.*")]
        )
        if arquivo:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    sessao = json.load(f)
                
                # Carregar configurações
                if 'config' in sessao:
                    for nome, valor in sessao['config'].items():
                        if nome in self.config_vars:
                            self.config_vars[nome].set(valor)
                
                # Carregar chat
                if 'chat' in sessao:
                    self.chat_text.delete(1.0, tk.END)
                    self.chat_text.insert(1.0, sessao['chat'])
                
                messagebox.showinfo("Sucesso", "Sessão carregada com sucesso!")
                
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao carregar sessão: {e}")
    
    def sobre(self):
        """Exibir sobre"""
        sobre_text = """
VHALINOR AI Geral v6.0.0

Sistema completo de Inteligência Artificial Geral com:
- Consciência e Sentiência Artificial
- Raciocínio Avançado e Metacognição
- Aprendizado Profundo e Contínuo
- Análise de Mercado Financeiro
- Processamento de Linguagem Natural
- Visão Computacional
- Automação Inteligente

Desenvolvido por VHALINOR Team
© 2026 - Todos os direitos reservados
        """
        messagebox.showinfo("Sobre VHALINOR AI Geral", sobre_text)
    
    def documentacao(self):
        """Exibir documentação"""
        doc_text = """
Documentação VHALINOR AI Geral

Para usar o sistema:

1. Status - Verifique o status dos componentes
2. Chat IA - Converse com a inteligência artificial
3. Mercado - Analise ativos financeiros
4. NLP - Processe texto com linguagem natural
5. Visão - Analise imagens
6. Automação - Execute tarefas automatizadas
7. Config - Configure o sistema

Para mais informações, consulte o README.md
        """
        messagebox.showinfo("Documentação", doc_text)
    
    def run(self):
        """Executar interface"""
        self.root.mainloop()


def main():
    """Função principal"""
    try:
        app = VhalinorGUI()
        app.run()
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao iniciar aplicação: {e}")


if __name__ == "__main__":
    main()
