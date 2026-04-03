#!/usr/bin/env python3
"""
VHALINOR AI Geral CLI - Interface de Linha de Comando
====================================================
Interface principal para interação com todos os módulos do sistema
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

try:
    from consciencia_artificial import ConscienciaArtificial, EstadoConsciencia
    from sentiencia_artificial import SentienciaArtificial, EstadoEmocional
    from raciocinio_avancado import RaciocinioAvancado
    from memoria_cognitiva import MemoriaCognitiva
    from aprendizado_profundo import AprendizadoProfundo
    from analise_mercado_financeiro import AnaliseMercadoFinanceiro
    from processamento_linguagem import ProcessamentoLinguagem
    from visao_computacional import VisaoComputacional
    from automacao import AutomacaoInteligente
    from tomada_decisao import TomadaDecisao
except ImportError as e:
    print(f"ERRO: Não foi possível importar módulos VHALINOR: {e}")
    print("Certifique-se de que todos os arquivos .py estão no diretório atual.")
    sys.exit(1)


class VhalinorCLI:
    """Interface principal do VHALINOR AI Geral"""
    
    def __init__(self):
        self.version = "6.0.0"
        self.consciencia = None
        self.sentiencia = None
        self.raciocinio = None
        self.memoria = None
        self.aprendizado = None
        self.mercado = None
        self.linguagem = None
        self.visao = None
        self.automacao = None
        self.decisao = None
        
        # Inicializar componentes principais
        self._inicializar_sistema()
    
    def _inicializar_sistema(self):
        """Inicializar todos os componentes do sistema"""
        print("🧠 Inicializando VHALINOR AI Geral...")
        
        try:
            # Consciência Artificial
            self.consciencia = ConscienciaArtificial()
            self.consciencia.inicializar()
            print("✅ Consciência Artificial inicializada")
            
            # Sentiência Artificial
            self.sentiencia = SentienciaArtificial()
            self.sentiencia.inicializar()
            print("✅ Sentiência Artificial inicializada")
            
            # Raciocínio Avançado
            self.raciocinio = RaciocinioAvancado()
            print("✅ Raciocínio Avançado inicializado")
            
            # Memória Cognitiva
            self.memoria = MemoriaCognitiva()
            print("✅ Memória Cognitiva inicializada")
            
            # Aprendizado Profundo
            self.aprendizado = AprendizadoProfundo()
            print("✅ Aprendizado Profundo inicializado")
            
            # Análise de Mercado
            self.mercado = AnaliseMercadoFinanceiro()
            print("✅ Análise de Mercado inicializada")
            
            # Processamento de Linguagem
            self.linguagem = ProcessamentoLinguagem()
            print("✅ Processamento de Linguagem inicializado")
            
            # Visão Computacional
            self.visao = VisaoComputacional()
            print("✅ Visão Computacional inicializada")
            
            # Automação Inteligente
            self.automacao = AutomacaoInteligente()
            print("✅ Automação Inteligente inicializada")
            
            # Tomada de Decisão
            self.decisao = TomadaDecisao()
            print("✅ Tomada de Decisão inicializada")
            
            print("🎉 Sistema VHALINOR AI Geral inicializado com sucesso!")
            
        except Exception as e:
            print(f"❌ Erro na inicialização: {e}")
    
    def status_sistema(self) -> Dict[str, Any]:
        """Obter status completo do sistema"""
        status = {
            "versao": self.version,
            "data_hora": datetime.now().isoformat(),
            "componentes": {}
        }
        
        # Status consciência
        if self.consciencia:
            estado = self.consciencia.obter_estado()
            status["componentes"]["consciencia"] = {
                "status": "ativo",
                "nivel": getattr(estado, 'nivel', 'desconhecido'),
                "autoconsciencia": getattr(estado, 'autoconsciencia', False)
            }
        
        # Status sentiência
        if self.sentiencia:
            estado_emocional = self.sentiencia.obter_estado_emocional()
            status["componentes"]["sentiencia"] = {
                "status": "ativo",
                "emocao_dominante": getattr(estado_emocional, 'emocao_dominante', 'neutra'),
                "intensidade": getattr(estado_emocional, 'intensidade', 0.5)
            }
        
        # Status memória
        if self.memoria:
            status["componentes"]["memoria"] = {
                "status": "ativo",
                "memorias_armazenadas": len(getattr(self.memoria, 'memorias', [])),
                "capacidade_usada": getattr(self.memoria, 'capacidade_usada', 0)
            }
        
        return status
    
    def processar_comando(self, comando: str) -> str:
        """Processar comando usando raciocínio avançado"""
        if not self.raciocinio:
            return "Raciocínio não disponível"
        
        try:
            # Analisar comando
            analise = self.raciocinio.analisar_comando(comando)
            
            # Tomada de decisão
            decisao = self.decisao.processar_comando(comando, analise)
            
            # Gerar resposta
            resposta = self.linguagem.gerar_resposta(decisao) if self.linguagem else str(decisao)
            
            # Armazenar na memória
            if self.memoria:
                self.memoria.armazenar_interacao(comando, resposta)
            
            return resposta
            
        except Exception as e:
            return f"Erro ao processar comando: {e}"
    
    def analisar_mercado(self, ativo: str, timeframe: str = "1d") -> Dict[str, Any]:
        """Analisar ativo do mercado financeiro"""
        if not self.mercado:
            return {"erro": "Módulo de mercado não disponível"}
        
        try:
            analise = self.mercado.analisar_ativo(ativo, timeframe)
            
            # Enriquecer análise com raciocínio
            if self.raciocinio:
                insights = self.raciocinio.gerar_insights_mercado(analise)
                analise["insights"] = insights
            
            return analise
            
        except Exception as e:
            return {"erro": f"Falha na análise: {e}"}
    
    def processar_texto(self, texto: str) -> Dict[str, Any]:
        """Processar texto usando NLP avançado"""
        if not self.linguagem:
            return {"erro": "Módulo de linguagem não disponível"}
        
        try:
            resultado = self.linguagem.analisar_completo(texto)
            
            # Adicionar análise emocional
            if self.sentiencia:
                emocional = self.sentiencia.analisar_sentimento_texto(texto)
                resultado["analise_emocional"] = emocional
            
            return resultado
            
        except Exception as e:
            return {"erro": f"Falha no processamento: {e}"}
    
    def executar_automação(self, tarefa: str) -> Dict[str, Any]:
        """Executar tarefa automatizada"""
        if not self.automacao:
            return {"erro": "Módulo de automação não disponível"}
        
        try:
            resultado = self.automacao.executar_tarefa(tarefa)
            return resultado
        except Exception as e:
            return {"erro": f"Falha na automação: {e}"}


def criar_parser():
    """Criar parser de argumentos da CLI"""
    parser = argparse.ArgumentParser(
        description="VHALINOR AI Geral - Interface de Linha de Comando",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  vhalinor-ai status                    # Ver status do sistema
  vhalinor-ai chat "Olá, como você está?"  # Conversar com a IA
  vhalinor-ai analisar PETR4           # Analisar ativo PETR4
  vhalinor-ai nlp "O mercado está em alta"  # Processar texto
  vhalinor-ai auto "analisar dados"    # Executar automação
        """
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version="VHALINOR AI Geral v6.0.0"
    )
    
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")
    
    # Status
    status_parser = subparsers.add_parser("status", help="Ver status do sistema")
    
    # Chat
    chat_parser = subparsers.add_parser("chat", help="Conversar com a IA")
    chat_parser.add_argument("mensagem", help="Mensagem para a IA")
    
    # Analisar mercado
    mercado_parser = subparsers.add_parser("analisar", help="Analisar ativo do mercado")
    mercado_parser.add_argument("ativo", help="Símbolo do ativo (ex: PETR4)")
    mercado_parser.add_argument("--timeframe", default="1d", help="Timeframe (padrão: 1d)")
    
    # NLP
    nlp_parser = subparsers.add_parser("nlp", help="Processar texto")
    nlp_parser.add_argument("texto", help="Texto para processar")
    
    # Automação
    auto_parser = subparsers.add_parser("auto", help="Executar automação")
    auto_parser.add_argument("tarefa", help="Tarefa para automatizar")
    
    # Demo
    demo_parser = subparsers.add_parser("demo", help="Executar demonstração")
    demo_parser.add_argument("--tipo", choices=["consciencia", "mercado", "nlp", "completo"], 
                           default="completo", help="Tipo de demonstração")
    
    return parser


def cmd_status(args, cli: VhalinorCLI):
    """Comando status"""
    print("📊 Status do Sistema VHALINOR AI Geral")
    print("=" * 50)
    
    status = cli.status_sistema()
    
    print(f"Versão: {status['versao']}")
    print(f"Data/Hora: {status['data_hora']}")
    print()
    
    print("Componentes:")
    for componente, info in status["componentes"].items():
        print(f"  {componente.capitalize()}: {info['status']}")
        for chave, valor in info.items():
            if chave != "status":
                print(f"    {chave}: {valor}")


def cmd_chat(args, cli: VhalinorCLI):
    """Comando chat"""
    print(f"💬 Você: {args.mensagem}")
    
    resposta = cli.processar_comando(args.mensagem)
    print(f"🤖 VHALINOR: {resposta}")


def cmd_analisar(args, cli: VhalinorCLI):
    """Comando analisar mercado"""
    print(f"📈 Analisando ativo: {args.ativo} (timeframe: {args.timeframe})")
    
    resultado = cli.analisar_mercado(args.ativo, args.timeframe)
    
    if "erro" in resultado:
        print(f"❌ {resultado['erro']}")
    else:
        print("✅ Análise concluída:")
        for chave, valor in resultado.items():
            if chave != "erro":
                print(f"  {chave}: {valor}")


def cmd_nlp(args, cli: VhalinorCLI):
    """Comando NLP"""
    print(f"📝 Processando texto: '{args.texto}'")
    
    resultado = cli.processar_texto(args.texto)
    
    if "erro" in resultado:
        print(f"❌ {resultado['erro']}")
    else:
        print("✅ Análise concluída:")
        for chave, valor in resultado.items():
            if chave != "erro":
                print(f"  {chave}: {valor}")


def cmd_auto(args, cli: VhalinorCLI):
    """Comando automação"""
    print(f"🤖 Executando automação: {args.tarefa}")
    
    resultado = cli.executar_automação(args.tarefa)
    
    if "erro" in resultado:
        print(f"❌ {resultado['erro']}")
    else:
        print("✅ Automação concluída:")
        for chave, valor in resultado.items():
            if chave != "erro":
                print(f"  {chave}: {valor}")


def cmd_demo(args, cli: VhalinorCLI):
    """Comando demonstração"""
    print(f"🎭 Demonstração: {args.tipo}")
    print("=" * 50)
    
    if args.tipo == "consciencia":
        print("Demonstração de Consciência Artificial")
        if cli.consciencia:
            estado = cli.consciencia.obter_estado()
            print(f"Estado de consciência: {getattr(estado, 'nivel', 'desconhecido')}")
            print(f"Autoconsciência: {getattr(estado, 'autoconsciencia', False)}")
    
    elif args.tipo == "mercado":
        print("Demonstração de Análise de Mercado")
        resultado = cli.analisar_mercado("PETR4", "1d")
        print(f"Resultado: {resultado}")
    
    elif args.tipo == "nlp":
        print("Demonstração de Processamento de Linguagem")
        texto = "O mercado financeiro está otimista com as novas perspectivas econômicas"
        resultado = cli.processar_texto(texto)
        print(f"Resultado: {resultado}")
    
    elif args.tipo == "completo":
        print("Demonstração Completa do Sistema")
        
        # 1. Status
        print("\n1️⃣ Status do Sistema:")
        cmd_status(None, cli)
        
        # 2. Chat
        print("\n2️⃣ Conversa com a IA:")
        cmd_chat(type('Args', (), {'mensagem': 'Olá! Como você está se sentindo hoje?'})(), cli)
        
        # 3. Análise de mercado
        print("\n3️⃣ Análise de Mercado:")
        cmd_analisar(type('Args', (), {'ativo': 'PETR4', 'timeframe': '1d'})(), cli)
        
        # 4. NLP
        print("\n4️⃣ Processamento de Linguagem:")
        cmd_nlp(type('Args', (), {'texto': 'A inteligência artificial está revolucionando o mercado'})(), cli)


def main():
    """Função principal da CLI"""
    parser = criar_parser()
    args = parser.parse_args()
    
    if not args.comando:
        parser.print_help()
        return
    
    try:
        # Inicializar CLI
        cli = VhalinorCLI()
        
        # Executar comando
        if args.comando == "status":
            cmd_status(args, cli)
        elif args.comando == "chat":
            cmd_chat(args, cli)
        elif args.comando == "analisar":
            cmd_analisar(args, cli)
        elif args.comando == "nlp":
            cmd_nlp(args, cli)
        elif args.comando == "auto":
            cmd_auto(args, cli)
        elif args.comando == "demo":
            cmd_demo(args, cli)
        else:
            print(f"Comando desconhecido: {args.comando}")
            parser.print_help()
    
    except KeyboardInterrupt:
        print("\n\n👋 Encerrando VHALINOR AI Geral...")
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
