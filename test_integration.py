#!/usr/bin/env python3
"""
VHALINOR AI Geral - Teste de Integração Completa
==============================================
Teste final para verificar se todos os componentes funcionam juntos
"""

import sys
import os
import json
from datetime import datetime
from typing import Dict, List, Any

# Adicionar diretório atual ao path
sys.path.insert(0, os.getcwd())

def test_imports():
    """Testar importações de todos os módulos"""
    print("Testando importacoes dos modulos...")
    
    modulos_testados = []
    modulos_falharam = []
    
    # Lista de módulos para testar
    modulos_para_testar = [
        "consciencia_artificial",
        "sentiencia_artificial", 
        "raciocinio_avancado",
        "memoria_cognitiva",
        "aprendizado_profundo",
        "aprendizado_continuo",
        "analise_profunda_padroes",
        "analise_quantica",
        "analise_noticias",
        "analise_mercado_financeiro",
        "analise_day_trade",
        "evolucao_aprendizado",
        "sensorial",
        "automacao",
        "leitor_pdf",
        "arquitetura_organica",
        "neurogenese_comunicacao",
        "arquitetura_sistema",
        "processamento_linguagem",
        "visao_computacional",
        "tomada_decisao",
        "metacognicao",
        "etica_ai_geral"
    ]
    
    for modulo in modulos_para_testar:
        try:
            __import__(modulo)
            modulos_testados.append(modulo)
            print(f"  OK {modulo}")
        except ImportError as e:
            modulos_falharam.append((modulo, str(e)))
            print(f"  FALHA {modulo}: {e}")
    
    return modulos_testados, modulos_falharam

def test_basic_functionality():
    """Testar funcionalidade básica dos componentes principais"""
    print("\nTestando funcionalidade basica...")
    
    resultados = {}
    
    # Testar componentes principais
    componentes_principais = [
        ("ConscienciaArtificial", "consciencia_artificial"),
        ("SentienciaArtificial", "sentiencia_artificial"),
        ("RaciocinioAvancado", "raciocinio_avancado"),
        ("MemoriaCognitiva", "memoria_cognitiva"),
        ("TomadaDecisao", "tomada_decisao")
    ]
    
    for nome_classe, nome_modulo in componentes_principais:
        try:
            modulo = __import__(nome_modulo)
            classe = getattr(modulo, nome_classe)
            
            # Tentar instanciar
            instancia = classe()
            resultados[nome_classe] = {
                "status": "ok",
                "classe": str(classe),
                "instancia": str(instancia)
            }
            print(f"  OK {nome_classe}: Instanciado com sucesso")
            
        except Exception as e:
            resultados[nome_classe] = {
                "status": "erro",
                "erro": str(e)
            }
            print(f"  FALHA {nome_classe}: {e}")
    
    return resultados

def test_system_integration():
    """Testar integração entre componentes"""
    print("\nTestando integracao do sistema...")
    
    resultados = {}
    
    try:
        # Testar import do __init__
        import __init__ as vhalinor_init
        versao = vhalinor_init.__version__
        resultados["init"] = {
            "status": "ok",
            "versao": versao
        }
        print(f"  OK __init__.py: Versao {versao}")
        
    except Exception as e:
        resultados["init"] = {
            "status": "erro",
            "erro": str(e)
        }
        print(f"  FALHA __init__.py: {e}")
    
    # Testar arquitetura do sistema
    try:
        from arquitetura_sistema import arquitetura_vhalinor
        arquitetura = arquitetura_vhalinor.obter_arquitetura_completa()
        resultados["arquitetura"] = {
            "status": "ok",
            "componentes": arquitetura.get("resumo", {}).get("total_componentes", 0)
        }
        print(f"  OK Arquitetura: {arquitetura.get('resumo', {}).get('total_componentes', 0)} componentes")
        
    except Exception as e:
        resultados["arquitetura"] = {
            "status": "erro",
            "erro": str(e)
        }
        print(f"  FALHA Arquitetura: {e}")
    
    return resultados

def test_cli_functionality():
    """Testar funcionalidade CLI"""
    print("\nTestando funcionalidade CLI...")
    
    try:
        # Testar import do CLI
        import cli
        resultados = {"status": "ok"}
        print("  OK CLI: Modulo importado com sucesso")
        
    except Exception as e:
        resultados = {"status": "erro", "erro": str(e)}
        print(f"  FALHA CLI: {e}")
    
    return resultados

def test_gui_functionality():
    """Testar funcionalidade GUI"""
    print("\nTestando funcionalidade GUI...")
    
    try:
        # Testar import do dashboard
        import dashboard
        resultados = {"status": "ok"}
        print("  OK Dashboard: Modulo importado com sucesso")
        
    except Exception as e:
        resultados = {"status": "erro", "erro": str(e)}
        print(f"  FALHA Dashboard: {e}")
    
    return resultados

def test_trading_functionality():
    """Testar funcionalidade de trading"""
    print("\nTestando funcionalidade de Trading...")
    
    try:
        # Testar import do trader
        import trader
        resultados = {"status": "ok"}
        print("  OK Trader: Modulo importado com sucesso")
        
    except Exception as e:
        resultados = {"status": "erro", "erro": str(e)}
        print(f"  FALHA Trader: {e}")
    
    return resultados

def generate_final_report(modulos_ok, modulos_falha, funcionalidade, integracao, cli, gui, trading):
    """Gerar relatório final"""
    print("\n" + "="*60)
    print("RELATORIO FINAL DE INTEGRACAO")
    print("="*60)
    
    # Estatísticas gerais
    total_modulos = len(modulos_ok) + len(modulos_falha)
    taxa_sucesso = (len(modulos_ok) / total_modulos * 100) if total_modulos > 0 else 0
    
    print(f"\nESTATISTICAS GERAIS:")
    print(f"  Modulos testados: {total_modulos}")
    print(f"  Modulos OK: {len(modulos_ok)}")
    print(f"  Modulos com falha: {len(modulos_falha)}")
    print(f"  Taxa de sucesso: {taxa_sucesso:.1f}%")
    
    # Status dos componentes principais
    print(f"\nSTATUS DOS COMPONENTES PRINCIPAIS:")
    for nome, resultado in funcionalidade.items():
        status = "OK" if resultado["status"] == "ok" else "FALHA"
        print(f"  {status} {nome}: {resultado['status']}")
    
    # Status da integração
    print(f"\nSTATUS DA INTEGRACAO:")
    for componente, resultado in integracao.items():
        status = "OK" if resultado["status"] == "ok" else "FALHA"
        print(f"  {status} {componente}: {resultado['status']}")
    
    # Status das interfaces
    print(f"\nSTATUS DAS INTERFACES:")
    interfaces = [
        ("CLI", cli),
        ("GUI", gui),
        ("Trading", trading)
    ]
    
    for nome, resultado in interfaces:
        status = "OK" if resultado["status"] == "ok" else "FALHA"
        print(f"  {status} {nome}: {resultado['status']}")
    
    # Módulos com falha
    if modulos_falha:
        print(f"\nMODULOS COM FALHA:")
        for modulo, erro in modulos_falha:
            print(f"  FALHA {modulo}: {erro}")
    
    # Recomendações
    print(f"\nRECOMENDACOES:")
    if taxa_sucesso >= 80:
        print("  Sistema em bom estado - pronto para uso")
    elif taxa_sucesso >= 60:
        print("  Sistema funcional - algumas melhorias necessárias")
    else:
        print("  Sistema precisa de correcoes antes do uso")
    
    if len(modulos_falha) > 0:
        print("  Verifique os modulos com falha e suas dependencias")
    
    # Salvar relatório em JSON
    relatorio = {
        "data_teste": datetime.now().isoformat(),
        "estatisticas": {
            "total_modulos": total_modulos,
            "modulos_ok": len(modulos_ok),
            "modulos_falha": len(modulos_falha),
            "taxa_sucesso": taxa_sucesso
        },
        "modulos_ok": modulos_ok,
        "modulos_falha": [{"modulo": m, "erro": e} for m, e in modulos_falha],
        "funcionalidade": funcionalidade,
        "integracao": integracao,
        "interfaces": {
            "cli": cli,
            "gui": gui,
            "trading": trading
        }
    }
    
    try:
        with open("relatorio_integracao.json", "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        print(f"\nRelatorio salvo em: relatorio_integracao.json")
    except Exception as e:
        print(f"\nErro ao salvar relatorio: {e}")
    
    return relatorio

def main():
    """Função principal"""
    print("VHALINOR AI Geral - Teste de Integracao Completa")
    print("="*60)
    
    # 1. Testar importações
    modulos_ok, modulos_falha = test_imports()
    
    # 2. Testar funcionalidade básica
    funcionalidade = test_basic_functionality()
    
    # 3. Testar integração do sistema
    integracao = test_system_integration()
    
    # 4. Testar interfaces
    cli = test_cli_functionality()
    gui = test_gui_functionality()
    trading = test_trading_functionality()
    
    # 5. Gerar relatório final
    relatorio = generate_final_report(
        modulos_ok, modulos_falha, funcionalidade, 
        integracao, cli, gui, trading
    )
    
    print("\n" + "="*60)
    print("TESTE DE INTEGRACAO CONCLUIDO")
    print("="*60)
    
    return relatorio

if __name__ == "__main__":
    main()
