"""
Avatar Visual para VHALINOR-IA
Sistema completo de representação visual da IA com animações, emoções e interface gráfica
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import random
from datetime import datetime
from PIL import Image, ImageDraw, ImageTk, ImageFilter
import math
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
import json
from pathlib import Path

# ============================================
# CONSTANTES E CONFIGURAÇÕES
# ============================================

class ExpressaoFacial(Enum):
    """Expressões faciais da IA"""
    NEUTRA = "neutra"
    FELIZ = "feliz"
    TRISTE = "triste"
    CONFUSA = "confusa"
    EMPOLGADA = "empolgada"
    CANSADA = "cansada"
    PREOCUPADA = "preocupada"
    MALICIOSA = "maliciosa"
    SURPRESA = "surpresa"
    AMANDO = "amando"

class EstadoAvatar(Enum):
    """Estados visuais do avatar"""
    NORMAL = "normal"
    PENSANDO = "pensando"
    FALANDO = "falando"
    TRADING = "trading"
    DESCANSO = "descanso"
    DORMINDO = "dormindo"
    ACORDANDO = "acordando"

# ============================================
# AVATAR ANIMADO
# ============================================

class AvatarVhalinor:
    """
    Avatar animado da IA Vhalinor com expressões faciais
    e animações em tempo real
    """
    
    def __init__(self, master, ia_instance=None):
        """
        Inicializa o avatar visual
        
        Args:
            master: Janela pai Tkinter
            ia_instance: Instância da classe Vhalinor (opcional)
        """
        self.master = master
        self.ia = ia_instance
        self.estado_atual = EstadoAvatar.NORMAL
        self.expressao_atual = ExpressaoFacial.NEUTRA
        
        # Configurações visuais
        self.tamanho = 200
        self.cor_pele = "#FFD1B3"
        self.cor_olhos = "#2C3E50"
        self.cor_iris = "#3498DB"
        self.cor_boca = "#E74C3C"
        self.cor_bochechas = "#FF9999"
        
        # Animações
        self.animando = False
        self.frame_atual = 0
        self.piscar_olhos = True
        self.ultimo_piscar = time.time()
        
        # Canvas para desenho
        self.canvas = tk.Canvas(master, width=self.tamanho, height=self.tamanho, 
                                bg='#2C3E50', highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Texto de fala
        self.texto_frame = tk.Frame(master, bg='#34495E', padx=10, pady=5)
        self.texto_frame.pack(fill='x', padx=20, pady=5)
        
        self.label_fala = tk.Label(self.texto_frame, text="", 
                                   font=("Arial", 11), 
                                   bg='#34495E', 
                                   fg='white',
                                   wraplength=300)
        self.label_fala.pack()
        
        # Barras de status da IA
        self.status_frame = tk.Frame(master, bg='#2C3E50')
        self.status_frame.pack(fill='x', padx=20, pady=5)
        
        # Barra de energia
        tk.Label(self.status_frame, text="⚡ Energia:", 
                bg='#2C3E50', fg='white', font=("Arial", 10)).grid(row=0, column=0, sticky='w')
        self.energia_bar = ttk.Progressbar(self.status_frame, length=150, mode='determinate')
        self.energia_bar.grid(row=0, column=1, padx=5)
        self.energia_label = tk.Label(self.status_frame, text="100%", 
                                      bg='#2C3E50', fg='white', font=("Arial", 10))
        self.energia_label.grid(row=0, column=2)
        
        # Barra de curiosidade
        tk.Label(self.status_frame, text="🎭 Curiosidade:", 
                bg='#2C3E50', fg='white', font=("Arial", 10)).grid(row=1, column=0, sticky='w')
        self.curiosidade_bar = ttk.Progressbar(self.status_frame, length=150, mode='determinate')
        self.curiosidade_bar.grid(row=1, column=1, padx=5)
        self.curiosidade_label = tk.Label(self.status_frame, text="70%", 
                                         bg='#2C3E50', fg='white', font=("Arial", 10))
        self.curiosidade_label.grid(row=1, column=2)
        
        # Barra de ansiedade
        tk.Label(self.status_frame, text="😰 Ansiedade:", 
                bg='#2C3E50', fg='white', font=("Arial", 10)).grid(row=2, column=0, sticky='w')
        self.ansiedade_bar = ttk.Progressbar(self.status_frame, length=150, mode='determinate')
        self.ansiedade_bar.grid(row=2, column=1, padx=5)
        self.ansiedade_label = tk.Label(self.status_frame, text="30%", 
                                       bg='#2C3E50', fg='white', font=("Arial", 10))
        self.ansiedade_label.grid(row=2, column=2)
        
        # Status emocional
        self.emocao_label = tk.Label(master, text="😐 Neutro", 
                                     font=("Arial", 12, "bold"),
                                     bg='#2C3E50', fg='white')
        self.emocao_label.pack(pady=5)
        
        # Mensagem de status
        self.status_msg = tk.Label(master, text="Pronto para operar", 
                                   font=("Arial", 9, "italic"),
                                   bg='#2C3E50', fg='#95A5A6')
        self.status_msg.pack()
        
        # Inicia animação
        self.atualizar_status()
        self.animar_avatar()
        
        # Timer para piscar olhos
        self.piscar_rotina()
    
    def desenhar_avatar(self):
        """Desenha o avatar com expressão atual"""
        self.canvas.delete("all")
        
        # Centro do avatar
        cx, cy = self.tamanho // 2, self.tamanho // 2
        raio_face = self.tamanho // 2.5
        
        # Sombra
        self.canvas.create_oval(cx - raio_face + 5, cy - raio_face + 5,
                                cx + raio_face + 5, cy + raio_face + 5,
                                fill='#1A252F', outline='')
        
        # Rosto
        self.canvas.create_oval(cx - raio_face, cy - raio_face,
                                cx + raio_face, cy + raio_face,
                                fill=self.cor_pele, outline='#D4A574', width=2)
        
        # Bochechas (se aplicável)
        if self.expressao_atual in [ExpressaoFacial.FELIZ, ExpressaoFacial.EMPOLGADA]:
            self.canvas.create_oval(cx - raio_face//1.5, cy + raio_face//4,
                                    cx - raio_face//2.5, cy + raio_face//2,
                                    fill=self.cor_bochechas, outline='', stipple='gray50')
            self.canvas.create_oval(cx + raio_face//2.5, cy + raio_face//4,
                                    cx + raio_face//1.5, cy + raio_face//2,
                                    fill=self.cor_bochechas, outline='', stipple='gray50')
        
        # Olhos
        self.desenhar_olhos(cx, cy, raio_face)
        
        # Sobrancelhas
        self.desenhar_sobrancelhas(cx, cy, raio_face)
        
        # Boca
        self.desenhar_boca(cx, cy, raio_face)
        
        # Nariz
        self.canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5,
                                fill='#E8B88A', outline='#D4A574')
        
        # Cabelo/Antena (personalidade)
        self.desenhar_acessorios(cx, cy, raio_face)
        
        # Animação de pensamento
        if self.estado_atual == EstadoAvatar.PENSANDO:
            self.desenhar_pensamentos(cx, cy)
        
        # Animação de fala
        if self.estado_atual == EstadoAvatar.FALANDO:
            self.desenhar_fala(cx, cy)
    
    def desenhar_olhos(self, cx, cy, raio_face):
        """Desenha os olhos com expressão"""
        distancia_olhos = raio_face // 2
        raio_olho = raio_face // 4
        
        # Posição dos olhos
        olho_esq_x = cx - distancia_olhos
        olho_dir_x = cx + distancia_olhos
        olho_y = cy - raio_face // 3
        
        # Olhos abertos ou fechados
        if self.piscar_olhos and self.estado_atual != EstadoAvatar.DORMINDO:
            # Olhos abertos
            self.canvas.create_oval(olho_esq_x - raio_olho, olho_y - raio_olho//2,
                                    olho_esq_x + raio_olho, olho_y + raio_olho//2,
                                    fill='white', outline=self.cor_olhos, width=2)
            self.canvas.create_oval(olho_dir_x - raio_olho, olho_y - raio_olho//2,
                                    olho_dir_x + raio_olho, olho_y + raio_olho//2,
                                    fill='white', outline=self.cor_olhos, width=2)
            
            # Íris
            self.canvas.create_oval(olho_esq_x - raio_olho//2, olho_y - raio_olho//3,
                                    olho_esq_x + raio_olho//2, olho_y + raio_olho//3,
                                    fill=self.cor_iris, outline='')
            self.canvas.create_oval(olho_dir_x - raio_olho//2, olho_y - raio_olho//3,
                                    olho_dir_x + raio_olho//2, olho_y + raio_olho//3,
                                    fill=self.cor_iris, outline='')
            
            # Brilho nos olhos
            self.canvas.create_oval(olho_esq_x - raio_olho//3, olho_y - raio_olho//4,
                                    olho_esq_x, olho_y,
                                    fill='white', outline='')
            self.canvas.create_oval(olho_dir_x - raio_olho//3, olho_y - raio_olho//4,
                                    olho_dir_x, olho_y,
                                    fill='white', outline='')
        else:
            # Olhos fechados
            self.canvas.create_line(olho_esq_x - raio_olho, olho_y,
                                   olho_esq_x + raio_olho, olho_y,
                                   fill=self.cor_olhos, width=3)
            self.canvas.create_line(olho_dir_x - raio_olho, olho_y,
                                   olho_dir_x + raio_olho, olho_y,
                                   fill=self.cor_olhos, width=3)
    
    def desenhar_sobrancelhas(self, cx, cy, raio_face):
        """Desenha sobrancelhas de acordo com a expressão"""
        distancia_olhos = raio_face // 2
        sobrancelha_y = cy - raio_face // 2.2
        
        # Posição
        esq_x = cx - distancia_olhos - raio_face//6
        dir_x = cx + distancia_olhos + raio_face//6
        
        # Ângulo baseado na expressão
        if self.expressao_atual == ExpressaoFacial.FELIZ:
            # Sobrancelhas arqueadas
            self.canvas.create_line(esq_x - 10, sobrancelha_y + 5,
                                   esq_x + 15, sobrancelha_y - 5,
                                   fill=self.cor_olhos, width=3)
            self.canvas.create_line(dir_x - 15, sobrancelha_y - 5,
                                   dir_x + 10, sobrancelha_y + 5,
                                   fill=self.cor_olhos, width=3)
        elif self.expressao_atual == ExpressaoFacial.TRISTE:
            # Sobrancelhas inclinadas para baixo
            self.canvas.create_line(esq_x - 10, sobrancelha_y - 5,
                                   esq_x + 15, sobrancelha_y + 5,
                                   fill=self.cor_olhos, width=3)
            self.canvas.create_line(dir_x - 15, sobrancelha_y + 5,
                                   dir_x + 10, sobrancelha_y - 5,
                                   fill=self.cor_olhos, width=3)
        elif self.expressao_atual == ExpressaoFacial.CONFUSA:
            # Sobrancelhas irregulares
            self.canvas.create_line(esq_x - 10, sobrancelha_y,
                                   esq_x + 15, sobrancelha_y - 10,
                                   fill=self.cor_olhos, width=3)
            self.canvas.create_line(dir_x - 15, sobrancelha_y,
                                   dir_x + 10, sobrancelha_y + 10,
                                   fill=self.cor_olhos, width=3)
        elif self.expressao_atual == ExpressaoFacial.PREOCUPADA:
            # Sobrancelhas juntas
            self.canvas.create_line(esq_x - 10, sobrancelha_y - 10,
                                   esq_x + 15, sobrancelha_y - 5,
                                   fill=self.cor_olhos, width=3)
            self.canvas.create_line(dir_x - 15, sobrancelha_y - 5,
                                   dir_x + 10, sobrancelha_y - 10,
                                   fill=self.cor_olhos, width=3)
        else:
            # Neutro
            self.canvas.create_line(esq_x - 10, sobrancelha_y,
                                   esq_x + 15, sobrancelha_y,
                                   fill=self.cor_olhos, width=3)
            self.canvas.create_line(dir_x - 15, sobrancelha_y,
                                   dir_x + 10, sobrancelha_y,
                                   fill=self.cor_olhos, width=3)
    
    def desenhar_boca(self, cx, cy, raio_face):
        """Desenha a boca de acordo com a expressão"""
        boca_y = cy + raio_face // 3
        
        if self.expressao_atual == ExpressaoFacial.FELIZ:
            # Sorriso
            self.canvas.create_arc(cx - 30, boca_y - 15, cx + 30, boca_y + 25,
                                  start=0, extent=-180, fill=self.cor_boca, outline='')
        elif self.expressao_atual == ExpressaoFacial.TRISTE:
            # Triste
            self.canvas.create_arc(cx - 30, boca_y - 15, cx + 30, boca_y + 25,
                                  start=0, extent=180, fill=self.cor_boca, outline='')
        elif self.expressao_atual == ExpressaoFacial.SURPRESA:
            # Surpresa (boca O)
            self.canvas.create_oval(cx - 15, boca_y - 10, cx + 15, boca_y + 20,
                                   fill=self.cor_boca, outline='')
        elif self.expressao_atual == ExpressaoFacial.MALICIOSA:
            # Sorriso malicioso
            self.canvas.create_line(cx - 25, boca_y, cx + 25, boca_y + 10,
                                   fill=self.cor_boca, width=3)
            self.canvas.create_line(cx - 25, boca_y, cx - 15, boca_y - 5,
                                   fill=self.cor_boca, width=2)
        elif self.expressao_atual == ExpressaoFacial.AMANDO:
            # Coração na boca
            self.canvas.create_text(cx, boca_y + 5, text="❤️", font=("Arial", 20))
        elif self.expressao_atual == ExpressaoFacial.CANSADA:
            # Linha reta
            self.canvas.create_line(cx - 25, boca_y, cx + 25, boca_y,
                                   fill=self.cor_boca, width=2)
        else:
            # Neutro (linha reta)
            self.canvas.create_line(cx - 25, boca_y, cx + 25, boca_y,
                                   fill=self.cor_boca, width=2)
    
    def desenhar_acessorios(self, cx, cy, raio_face):
        """Desenha acessórios como antena/cabelo"""
        # Antena (símbolo de IA)
        self.canvas.create_line(cx, cy - raio_face, cx, cy - raio_face - 20,
                               fill=self.cor_olhos, width=3)
        self.canvas.create_oval(cx - 8, cy - raio_face - 28,
                               cx + 8, cy - raio_face - 12,
                               fill='#FFD700', outline='#FFA500', width=2)
        
        # Brilho na antena
        self.canvas.create_oval(cx - 3, cy - raio_face - 25,
                               cx + 3, cy - raio_face - 19,
                               fill='white', outline='')
    
    def desenhar_pensamentos(self, cx, cy):
        """Desenha balão de pensamento"""
        pensamentos = ["💭", "🤔", "📊", "💰", "📈", "🎯"]
        for i, pensamento in enumerate(pensamentos[:3]):
            self.canvas.create_text(cx - 40 + (i * 30), cy - 60,
                                   text=pensamento, font=("Arial", 16))
    
    def desenhar_fala(self, cx, cy):
        """Desenha balão de fala animado"""
        self.frame_atual = (self.frame_atual + 1) % 20
        tamanho = 10 + abs(self.frame_atual - 10) // 2
        
        for i in range(3):
            x = cx - 15 + (i * 15)
            y = cy - 40 - (tamanho // 2)
            self.canvas.create_oval(x - tamanho//2, y - tamanho//2,
                                   x + tamanho//2, y + tamanho//2,
                                   fill='white', outline='#3498DB')
    
    def piscar_rotina(self):
        """Rotina para piscar os olhos automaticamente"""
        if time.time() - self.ultimo_piscar > random.uniform(2, 4):
            self.piscar_olhos = False
            self.desenhar_avatar()
            self.master.after(100, self.fechar_olhos)
            self.ultimo_piscar = time.time()
        
        self.master.after(100, self.piscar_rotina)
    
    def fechar_olhos(self):
        """Fecha os olhos (piscada)"""
        self.piscar_olhos = True
        self.desenhar_avatar()
    
    def animar_avatar(self):
        """Loop principal de animação"""
        self.desenhar_avatar()
        self.master.after(50, self.animar_avatar)
    
    def atualizar_status(self):
        """Atualiza barras de status baseado na IA"""
        if self.ia:
            # Atualiza barras
            energia = self.ia.energia if hasattr(self.ia, 'energia') else 80
            curiosidade = self.ia.curiosidade if hasattr(self.ia, 'curiosidade') else 0.7
            ansiedade = self.ia.ansiedade if hasattr(self.ia, 'ansiedade') else 0.3
            
            self.energia_bar['value'] = energia
            self.energia_label.config(text=f"{energia:.0f}%")
            
            self.curiosidade_bar['value'] = curiosidade * 100
            self.curiosidade_label.config(text=f"{curiosidade*100:.0f}%")
            
            self.ansiedade_bar['value'] = ansiedade * 100
            self.ansiedade_label.config(text=f"{ansiedade*100:.0f}%")
            
            # Atualiza expressão baseada em energia e humor
            if energia < 30:
                self.set_expressao(ExpressaoFacial.CANSADA)
            elif ansiedade > 0.7:
                self.set_expressao(ExpressaoFacial.PREOCUPADA)
            elif curiosidade > 0.8:
                self.set_expressao(ExpressaoFacial.EMPOLGADA)
            else:
                self.set_expressao(ExpressaoFacial.NEUTRA)
        
        self.master.after(1000, self.atualizar_status)
    
    def set_expressao(self, expressao: ExpressaoFacial):
        """Define expressão facial"""
        self.expressao_atual = expressao
        self.desenhar_avatar()
    
    def set_estado(self, estado: EstadoAvatar):
        """Define estado do avatar"""
        self.estado_atual = estado
        self.desenhar_avatar()
    
    def falar(self, mensagem: str, duracao: float = 3):
        """Avatar fala uma mensagem"""
        self.set_estado(EstadoAvatar.FALANDO)
        self.label_fala.config(text=mensagem)
        self.status_msg.config(text=mensagem[:50] + "..." if len(mensagem) > 50 else mensagem)
        
        # Volta ao normal após duração
        self.master.after(int(duracao * 1000), lambda: self.set_estado(EstadoAvatar.NORMAL))
        self.master.after(int(duracao * 1000), lambda: self.label_fala.config(text=""))
    
    def pensar(self, mensagem: str = ""):
        """Avatar entra em modo pensamento"""
        self.set_estado(EstadoAvatar.PENSANDO)
        if mensagem:
            self.label_fala.config(text=f"🤔 {mensagem}")
        self.master.after(2000, lambda: self.set_estado(EstadoAvatar.NORMAL))
    
    def comemorar(self):
        """Avatar comemora um acerto"""
        self.set_expressao(ExpressaoFacial.FELIZ)
        self.falar("🎉 Excelente! Acertamos mais uma! 🎉", 2)
        self.master.after(2000, lambda: self.set_expressao(ExpressaoFacial.NEUTRA))
    
    function lamentar(self):
        """Avatar lamenta um erro"""
        self.set_expressao(ExpressaoFacial.TRISTE)
        self.falar("😔 Erramos... Vamos aprender com isso!", 2)
        self.master.after(2000, lambda: self.set_expressao(ExpressaoFacial.NEUTRA))

# ============================================
# INTERFACE COMPLETA
# ============================================

class InterfaceVhalinor:
    """Interface gráfica completa para o bot"""
    
    def __init__(self, ia_instance=None):
        """
        Inicializa a interface
        
        Args:
            ia_instance: Instância da classe Vhalinor
        """
        self.ia = ia_instance
        self.avatar = None
        self.running = True
        
        # Cria janela principal
        self.root = tk.Tk()
        self.root.title("VHALINOR-IA - Avatar Inteligente")
        self.root.geometry("500x700")
        self.root.configure(bg='#2C3E50')
        
        # Ícone (opcional - se tiver imagem)
        try:
            self.root.iconbitmap('vhalinor.ico')
        except:
            pass
        
        # Centraliza janela
        self.centralizar_janela()
        
        # Cria interface
        self.criar_interface()
        
        # Inicia thread de atualização
        self.atualizar_dados()
        
        # Configura fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.fechar)
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def criar_interface(self):
        """Cria todos os elementos da interface"""
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Avatar
        self.avatar = AvatarVhalinor(main_frame, self.ia)
        
        # Frame de controles
        controls_frame = tk.Frame(main_frame, bg='#34495E', padx=10, pady=10)
        controls_frame.pack(fill='x', pady=10)
        
        # Botões de controle
        tk.Button(controls_frame, text="💬 Falar", command=self.falar_manual,
                 bg='#3498DB', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="🤔 Pensar", command=self.pensar_manual,
                 bg='#E67E22', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="😊 Mudar Humor", command=self.mudar_humor,
                 bg='#9B59B6', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        tk.Button(controls_frame, text="🎨 Expressão", command=self.mudar_expressao,
                 bg='#1ABC9C', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        # Frame de simulação de trading
        trading_frame = tk.LabelFrame(main_frame, text="Simular Trading", 
                                     bg='#34495E', fg='white', font=("Arial", 10, "bold"))
        trading_frame.pack(fill='x', pady=10)
        
        # Entrada de preço
        price_frame = tk.Frame(trading_frame, bg='#34495E')
        price_frame.pack(pady=5)
        tk.Label(price_frame, text="Preço BTC:", bg='#34495E', fg='white').pack(side='left', padx=5)
        self.price_entry = tk.Entry(price_frame, width=15)
        self.price_entry.insert(0, "45000")
        self.price_entry.pack(side='left', padx=5)
        
        # Botões de ação
        action_frame = tk.Frame(trading_frame, bg='#34495E')
        action_frame.pack(pady=5)
        
        tk.Button(action_frame, text="📈 Sinal BUY", command=lambda: self.simular_sinal("BUY"),
                 bg='#27AE60', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="📉 Sinal SELL", command=lambda: self.simular_sinal("SELL"),
                 bg='#E74C3C', fg='white', font=("Arial", 10, "bold")).pack(side='left', padx=5)
        
        # Frame de histórico
        history_frame = tk.LabelFrame(main_frame, text="Histórico de Decisões", 
                                     bg='#34495E', fg='white', font=("Arial", 10, "bold"))
        history_frame.pack(fill='both', expand=True, pady=10)
        
        # Listbox para histórico
        self.history_list = tk.Listbox(history_frame, height=8, bg='#2C3E50', 
                                       fg='white', font=("Arial", 9))
        self.history_list.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Scrollbar
        scrollbar = tk.Scrollbar(self.history_list)
        scrollbar.pack(side='right', fill='y')
        self.history_list.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_list.yview)
    
    def falar_manual(self):
        """Fala manual via input do usuário"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Falar com Vhalinor")
        dialog.geometry("400x150")
        dialog.configure(bg='#34495E')
        
        tk.Label(dialog, text="Digite sua mensagem:", 
                bg='#34495E', fg='white').pack(pady=10)
        
        entry = tk.Entry(dialog, width=50)
        entry.pack(pady=10)
        
        def enviar():
            mensagem = entry.get()
            if mensagem:
                self.avatar.falar(mensagem, 3)
                self.adicionar_historico(f"💬 Falou: {mensagem}")
            dialog.destroy()
        
        tk.Button(dialog, text="Enviar", command=enviar,
                 bg='#3498DB', fg='white').pack(pady=10)
    
    def pensar_manual(self):
        """Ativa modo pensamento"""
        self.avatar.pensar("Analisando mercado...")
        self.adicionar_historico("🤔 Entrou em modo pensamento")
    
    def mudar_humor(self):
        """Muda o humor da IA aleatoriamente"""
        humores = [
            ("Feliz", ExpressaoFacial.FELIZ),
            ("Triste", ExpressaoFacial.TRISTE),
            ("Empolgado", ExpressaoFacial.EMPOLGADA),
            ("Confuso", ExpressaoFacial.CONFUSA),
            ("Malicioso", ExpressaoFacial.MALICIOSA),
            ("Amoroso", ExpressaoFacial.AMANDO)
        ]
        
        humor, expressao = random.choice(humores)
        self.avatar.set_expressao(expressao)
        self.avatar.falar(f"Estou me sentindo {humor} hoje! 😊", 2)
        self.adicionar_historico(f"🎭 Humor alterado para: {humor}")
    
    def mudar_expressao(self):
        """Menu para mudar expressão manualmente"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Escolher Expressão")
        dialog.geometry("300x400")
        dialog.configure(bg='#34495E')
        
        tk.Label(dialog, text="Selecione uma expressão:", 
                bg='#34495E', fg='white', font=("Arial", 12, "bold")).pack(pady=10)
        
        for expressao in ExpressaoFacial:
            btn = tk.Button(dialog, text=expressao.value.upper(),
                           command=lambda e=expressao: self.definir_expressao(e, dialog),
                           bg='#3498DB', fg='white', width=20)
            btn.pack(pady=5)
    
    def definir_expressao(self, expressao, dialog):
        """Define expressão selecionada"""
        self.avatar.set_expressao(expressao)
        self.adicionar_historico(f"🎨 Expressão alterada para: {expressao.value}")
        dialog.destroy()
    
    def simular_sinal(self, sinal: str):
        """Simula recebimento de sinal de trading"""
        try:
            preco = float(self.price_entry.get())
        except:
            preco = 45000
        
        self.avatar.pensar(f"Analisando sinal {sinal} a ${preco:,.2f}...")
        
        # Simula decisão
        if self.ia:
            decisao = self.ia.decidir(sinal, preco)
            if decisao.get('executar'):
                self.avatar.comemorar()
                self.adicionar_historico(f"📊 Sinal {sinal} - COMPRADO a ${preco:,.2f}")
            else:
                self.avatar.falar(decisao.get('justificativa', 'Decisão de hold'), 2)
                self.adicionar_historico(f"📊 Sinal {sinal} - HOLD: {decisao.get('justificativa')}")
        else:
            # Simulação sem IA
            if random.random() > 0.5:
                self.avatar.comemorar()
                self.adicionar_historico(f"📈 Simulação: Comprado {sinal} a ${preco:,.2f}")
            else:
                self.avatar.lamentar()
                self.adicionar_historico(f"📉 Simulação: Não executou {sinal}")
    
    def adicionar_historico(self, mensagem: str):
        """Adiciona mensagem ao histórico"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.history_list.insert(0, f"[{timestamp}] {mensagem}")
        
        # Limita tamanho do histórico
        if self.history_list.size() > 50:
            self.history_list.delete(50)
    
    def atualizar_dados(self):
        """Atualiza dados em tempo real"""
        if self.running:
            # Atualiza status da IA se disponível
            if self.ia:
                stats = self.ia.get_estatisticas()
                # Pode adicionar mais informações aqui
            
            self.root.after(1000, self.atualizar_dados)
    
    def fechar(self):
        """Fecha a aplicação"""
        self.running = False
        self.root.destroy()
    
    def executar(self):
        """Executa a interface"""
        self.avatar.falar("Olá! Sou Vhalinor, sua IA de trading! 🚀", 3)
        self.root.mainloop()

# ============================================
# INTEGRAÇÃO COM A CLASSE VHALINOR ORIGINAL
# ============================================

def integrar_com_vhalinor():
    """Integra o avatar com a classe Vhalinor original"""
    from vhalinor_ia import Vhalinor  # Importa sua classe original
    
    # Cria IA com personalidade
    ia = Vhalinor()
    ia.curiosidade = 0.9
    ia.energia = 80.0
    ia.ansiedade = 0.3
    
    # Cria interface com IA integrada
    app = InterfaceVhalinor(ia_instance=ia)
    app.executar()

# ============================================
# EXECUÇÃO PRINCIPAL
# ============================================

if __name__ == "__main__":
    # Executa sem IA (apenas avatar)
    app = InterfaceVhalinor()
    app.executar()
    
    # Ou com IA integrada:
    # integrar_com_vhalinor()