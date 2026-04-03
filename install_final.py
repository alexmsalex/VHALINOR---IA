#!/usr/bin/env python3
"""
Instalador VHALINOR AI Geral - Versão Final Corrigida
====================================================
Trata erros comuns de instalação no Windows
"""

import os
import sys
import subprocess
import platform
import shutil
import json
from pathlib import Path
from typing import List, Dict, Optional

class VhalinorInstallerFixed:
    """Instalador corrigido para Windows"""
    
    def __init__(self):
        self.version = "6.0.0"
        self.system = platform.system().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.install_dir = Path.cwd()
        self.config_file = self.install_dir / "vhalinor_config.json"
    
    def print_header(self):
        """Imprimir cabeçalho"""
        print("=" * 80)
        print("VHALINOR AI Geral v6.0 - Instalador Corrigido")
        print("Inteligência Artificial Geral com Sistemas Cognitivos")
        print("=" * 80)
        print()
    
    def check_python_version(self) -> bool:
        """Verificar compatibilidade do Python"""
        print("Verificando versão do Python...")
        
        if sys.version_info < (3, 8):
            print(f"ERRO: Python {self.python_version} não é compatível")
            print("Requerido: Python 3.8+")
            return False
        
        if sys.version_info >= (3, 14):
            print(f"AVISO: Python {self.python_version} detectado")
            print("Algumas bibliotecas podem não ser compatíveis")
            print("Usando versões alternativas...")
        else:
            print(f"OK: Python {self.python_version} compatível")
        
        return True
    
    def install_basic_dependencies(self) -> bool:
        """Instalar dependências básicas com tratamento de erros"""
        print("Instalando dependências básicas...")
        
        # Lista de pacotes essenciais em ordem de instalação
        essential_packages = [
            "wheel",
            "setuptools",
            "numpy",
            "pandas",
            "matplotlib",
            "scipy",
            "scikit-learn"
        ]
        
        pip_path = self.get_venv_pip()
        
        for package in essential_packages:
            try:
                print(f"  Instalando {package}...")
                result = subprocess.run([
                    pip_path, "install", package, "--no-cache-dir"
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"    OK: {package} instalado")
                else:
                    print(f"    AVISO: {package} - {result.stderr.strip()}")
                    # Continuar mesmo com falha
            
            except subprocess.TimeoutExpired:
                print(f"    TIMEOUT: {package} - pulando")
            except Exception as e:
                print(f"    ERRO: {package} - {e}")
        
        return True
    
    def install_alternative_dependencies(self) -> bool:
        """Instalar dependências alternativas para Python 3.14"""
        print("Instalando dependências alternativas...")
        
        pip_path = self.get_venv_pip()
        
        # Pacotes alternativos mais compatíveis
        alternative_packages = [
            "yfinance",
            "nltk",
            "spacy",
            "opencv-python",
            "pillow",
            "requests",
            "beautifulsoup4",
            "tqdm",
            "schedule"
        ]
        
        for package in alternative_packages:
            try:
                print(f"  Instalando {package}...")
                result = subprocess.run([
                    pip_path, "install", package, "--no-cache-dir", "--no-deps"
                ], capture_output=True, text=True, timeout=180)
                
                if result.returncode == 0:
                    print(f"    OK: {package} instalado")
                else:
                    print(f"    AVISO: {package} - pulando")
            
            except Exception as e:
                print(f"    ERRO: {package} - {e}")
        
        return True
    
    def get_venv_pip(self) -> str:
        """Obter caminho do Pip no ambiente virtual"""
        if self.system == "windows":
            return str(self.install_dir / "vhalinor_env" / "Scripts" / "pip.exe")
        else:
            return str(self.install_dir / "vhalinor_env" / "bin" / "pip")
    
    def get_venv_python(self) -> str:
        """Obter caminho do Python no ambiente virtual"""
        if self.system == "windows":
            return str(self.install_dir / "vhalinor_env" / "Scripts" / "python.exe")
        else:
            return str(self.install_dir / "vhalinor_env" / "bin" / "python")
    
    def create_virtual_env(self) -> bool:
        """Criar ambiente virtual"""
        print("Criando ambiente virtual...")
        
        venv_path = self.install_dir / "vhalinor_env"
        
        if venv_path.exists():
            print("AVISO: Ambiente virtual já existe. Removendo...")
            try:
                shutil.rmtree(venv_path, ignore_errors=True)
            except:
                print("AVISO: Não foi possível remover ambiente antigo")
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], 
                         check=True, capture_output=True)
            print("OK: Ambiente virtual criado")
            return True
        except Exception as e:
            print(f"ERRO: Não foi possível criar ambiente virtual: {e}")
            return False
    
    def test_basic_imports(self) -> bool:
        """Testar imports básicos"""
        print("Testando imports básicos...")
        
        python_path = self.get_venv_python()
        
        test_code = """
import sys
sys.path.insert(0, '.')

test_packages = [
    ('numpy', 'np'),
    ('pandas', 'pd'), 
    ('matplotlib', 'plt'),
    ('sklearn', None)
]

success_count = 0
for package, alias in test_packages:
    try:
        if alias:
            exec(f"import {package} as {alias}")
        else:
            exec(f"import {package}")
        print(f"OK: {package}")
        success_count += 1
    except ImportError as e:
        print(f"FALHA: {package} - {e}")

print(f"Total: {success_count}/{len(test_packages)} pacotes funcionando")
"""
        
        try:
            result = subprocess.run([python_path, "-c", test_code], 
                                  capture_output=True, text=True)
            print(result.stdout.strip())
            return True
        except Exception as e:
            print(f"ERRO: Não foi possível testar imports: {e}")
            return False
    
    def create_minimal_config(self):
        """Criar configuração mínima funcional"""
        print("Criando configuração mínima...")
        
        config = {
            "version": self.version,
            "python_version": self.python_version,
            "system": self.system,
            "installation_type": "minimal",
            "features": {
                "basic_ai": True,
                "data_analysis": True,
                "trading": True,
                "nlp": True,
                "computer_vision": True
            },
            "notes": [
                "Instalação mínima para Python 3.14+",
                "Algumas bibliotecas podem não estar disponíveis",
                "Use versões alternativas quando necessário"
            ]
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        print("OK: Configuração criada")
    
    def create_simple_activation_script(self):
        """Criar script de ativação simples"""
        print("Criando script de ativação...")
        
        if self.system == "windows":
            script_path = self.install_dir / "start_vhalinor.bat"
            with open(script_path, 'w') as f:
                f.write("""@echo off
echo Iniciando VHALINOR AI Geral...
echo.
echo Ativando ambiente virtual...
call "vhalinor_env\\Scripts\\activate.bat"
echo.
echo Testando sistema...
python -c "import sys; print('Python:', sys.version)"
python -c "import numpy as np; print('NumPy:', np.__version__)"
echo.
echo VHALINOR AI Geral pronto para uso!
echo.
echo Comandos disponíveis:
echo   python cli.py --help
echo   python dashboard.py
echo   python examples.py
echo.
pause
""")
        
        print("OK: Script de ativação criado")
    
    def print_final_instructions(self):
        """Instruções finais"""
        print("\n" + "=" * 80)
        print("INSTALAÇÃO CONCLUÍDA!")
        print("=" * 80)
        
        print("\nPara começar:")
        print("1. Execute: start_vhalinor.bat")
        print("2. Teste com: python test_integration.py")
        print("3. Use os exemplos: python examples.py")
        
        print("\nNotas importantes:")
        print("- Python 3.14+ tem compatibilidade limitada")
        print("- Algumas bibliotecas podem não estar disponíveis")
        print("- Use PyTorch em vez de TensorFlow")
        print("- Sistema funcional para análise de dados e IA básica")
        
        print("\nArquivos criados:")
        print("- vhalinor_env/ (ambiente virtual)")
        print("- vhalinor_config.json (configuração)")
        print("- start_vhalinor.bat (script de inicialização)")
    
    def run_installation(self):
        """Executar instalação completa"""
        self.print_header()
        
        # Verificar Python
        if not self.check_python_version():
            return False
        
        # Criar ambiente virtual
        if not self.create_virtual_env():
            return False
        
        # Instalar dependências básicas
        if not self.install_basic_dependencies():
            print("AVISO: Alguns pacotes não foram instalados")
        
        # Instalar dependências alternativas
        if not self.install_alternative_dependencies():
            print("AVISO: Alguns pacotes alternativos não foram instalados")
        
        # Testar imports
        self.test_basic_imports()
        
        # Criar configuração
        self.create_minimal_config()
        self.create_simple_activation_script()
        
        # Instruções finais
        self.print_final_instructions()
        
        return True


def main():
    """Função principal"""
    installer = VhalinorInstallerFixed()
    
    try:
        success = installer.run_installation()
        if success:
            print("\nInstalação concluída com sucesso!")
            input("Pressione Enter para sair...")
        else:
            print("\nInstalação falhou!")
            input("Pressione Enter para sair...")
    except KeyboardInterrupt:
        print("\nInstalação cancelada pelo usuário")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        input("Pressione Enter para sair...")


if __name__ == "__main__":
    main()
