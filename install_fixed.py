#!/usr/bin/env python3
"""
Instalador Automatizado VHALINOR AI Geral v6.0
==============================================
Script completo para instalação e configuração do sistema
"""

import os
import sys
import subprocess
import platform
import shutil
import json
from pathlib import Path
from typing import List, Dict, Optional

class VhalinorInstaller:
    """Classe principal do instalador VHALINOR AI Geral"""
    
    def __init__(self):
        self.version = "6.0.0"
        self.system = platform.system().lower()
        self.python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        self.install_dir = Path.cwd()
        self.config_file = self.install_dir / "vhalinor_config.json"
    
    def print_color(self, text: str, color: str = 'white'):
        """Imprimir texto sem cores (compatibilidade Windows)"""
        print(text)
    
    def print_header(self):
        """Imprimir cabeçalho do instalador"""
        self.print_color("=" * 80)
        self.print_color("VHALINOR AI Geral v6.0 - Instalador Automatizado")
        self.print_color("Inteligência Artificial Geral com Sistemas Cognitivos Avançados")
        self.print_color("=" * 80)
        print()
    
    def check_requirements(self) -> bool:
        """Verificar requisitos do sistema"""
        self.print_color("Verificando requisitos do sistema...")
        
        # Verificar Python
        if sys.version_info < (3, 8):
            self.print_color(f"ERRO: Python {self.python_version} detectado. Requerido: Python 3.8+")
            return False
        
        self.print_color(f"OK: Python {self.python_version} compatível")
        
        # Verificar pip
        try:
            import pip
            self.print_color("OK: Pip disponível")
        except ImportError:
            self.print_color("ERRO: Pip não encontrado")
            return False
        
        # Verificar espaço em disco (aproximado)
        try:
            stat = shutil.disk_usage('/')
            free_gb = stat.free / (1024**3)
            if free_gb < 5:
                self.print_color(f"AVISO: Apenas {free_gb:.1f}GB livres. Recomendado: 10GB+")
            else:
                self.print_color(f"OK: {free_gb:.1f}GB livres em disco")
        except:
            pass
        
        # Verificar memória RAM
        try:
            import psutil
            ram_gb = psutil.virtual_memory().total / (1024**3)
            if ram_gb < 8:
                self.print_color(f"AVISO: Apenas {ram_gb:.1f}GB RAM. Recomendado: 16GB+")
            else:
                self.print_color(f"OK: {ram_gb:.1f}GB RAM disponíveis")
        except ImportError:
            self.print_color("INFO: Não foi possível verificar RAM (psutil não instalado)")
        
        return True
    
    def create_virtual_env(self) -> bool:
        """Criar ambiente virtual"""
        self.print_color("Criando ambiente virtual...")
        
        venv_path = self.install_dir / "vhalinor_env"
        
        if venv_path.exists():
            self.print_color("AVISO: Ambiente virtual já existe. Removendo...")
            shutil.rmtree(venv_path, ignore_errors=True)
        
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_path)], 
                         check=True, capture_output=True)
            self.print_color("OK: Ambiente virtual criado")
            return True
        except subprocess.CalledProcessError as e:
            self.print_color(f"ERRO: Erro ao criar ambiente virtual: {e}")
            return False
    
    def get_venv_python(self) -> str:
        """Obter caminho do Python no ambiente virtual"""
        if self.system == "windows":
            return str(self.install_dir / "vhalinor_env" / "Scripts" / "python.exe")
        else:
            return str(self.install_dir / "vhalinor_env" / "bin" / "python")
    
    def get_venv_pip(self) -> str:
        """Obter caminho do Pip no ambiente virtual"""
        if self.system == "windows":
            return str(self.install_dir / "vhalinor_env" / "Scripts" / "pip.exe")
        else:
            return str(self.install_dir / "vhalinor_env" / "bin" / "pip")
    
    def upgrade_pip(self) -> bool:
        """Atualizar pip no ambiente virtual"""
        self.print_color("Atualizando pip...")
        
        pip_path = self.get_venv_pip()
        try:
            # Tentar atualizar pip, mas não falhar se não der certo
            result = subprocess.run([pip_path, "install", "--upgrade", "pip"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.print_color("OK: Pip atualizado com sucesso")
            else:
                # Se falhar, verificar se pip está funcionando
                self.print_color("AVISO: Pip não pode ser atualizado, mas está funcional")
                # Testar se pip está funcionando
                test_result = subprocess.run([pip_path, "--version"], 
                                            capture_output=True, text=True)
                if test_result.returncode == 0:
                    self.print_color(f"OK: Pip versão {test_result.stdout.strip()} está funcional")
                else:
                    self.print_color("ERRO: Pip não está funcionando")
                    return False
            
            return True
            
        except Exception as e:
            self.print_color(f"AVISO: Aviso ao atualizar pip: {e}")
            # Tentar verificar se pip está funcionando mesmo assim
            try:
                test_result = subprocess.run([pip_path, "--version"], 
                                            capture_output=True, text=True)
                if test_result.returncode == 0:
                    self.print_color(f"OK: Pip versão {test_result.stdout.strip()} está funcional")
                    return True
                else:
                    self.print_color("ERRO: Pip não está funcionando")
                    return False
            except:
                self.print_color("ERRO: Erro crítico com pip")
                return False
    
    def install_dependencies(self) -> bool:
        """Instalar dependências"""
        self.print_color("Instalando dependências...")
        
        pip_path = self.get_venv_pip()
        requirements_path = self.install_dir / "requirements.txt"
        
        if not requirements_path.exists():
            self.print_color("ERRO: Arquivo requirements.txt não encontrado")
            return False
        
        try:
            # Instalar dependências básicas primeiro
            basic_deps = ["wheel", "setuptools"]
            for dep in basic_deps:
                subprocess.run([pip_path, "install", dep], 
                             check=True, capture_output=True)
            
            # Instalar requirements.txt
            subprocess.run([pip_path, "install", "-r", str(requirements_path)], 
                         check=True, capture_output=True)
            
            self.print_color("OK: Dependências instaladas")
            return True
        except subprocess.CalledProcessError as e:
            self.print_color(f"ERRO: Erro ao instalar dependências: {e}")
            return False
    
    def install_package(self) -> bool:
        """Instalar o pacote VHALINOR"""
        self.print_color("Instalando VHALINOR AI Geral...")
        
        pip_path = self.get_venv_pip()
        
        try:
            # Instalar em modo desenvolvimento
            subprocess.run([pip_path, "install", "-e", "."], 
                         check=True, capture_output=True)
            
            self.print_color("OK: VHALINOR AI Geral instalado")
            return True
        except subprocess.CalledProcessError as e:
            self.print_color(f"ERRO: Erro ao instalar pacote: {e}")
            return False
    
    def create_directories(self):
        """Criar diretórios necessários"""
        self.print_color("Criando estrutura de diretórios...")
        
        directories = [
            "data",
            "models",
            "logs",
            "config",
            "cache",
            "exports",
            "temp",
            "user_data"
        ]
        
        for dir_name in directories:
            dir_path = self.install_dir / dir_name
            dir_path.mkdir(exist_ok=True)
            self.print_color(f"OK: Diretório criado: {dir_name}")
    
    def create_config_file(self):
        """Criar arquivo de configuração"""
        self.print_color("Criando arquivo de configuração...")
        
        config = {
            "version": self.version,
            "install_date": str(Path.cwd()),
            "python_version": self.python_version,
            "system": self.system,
            "paths": {
                "data_dir": str(self.install_dir / "data"),
                "models_dir": str(self.install_dir / "models"),
                "logs_dir": str(self.install_dir / "logs"),
                "config_dir": str(self.install_dir / "config"),
                "cache_dir": str(self.install_dir / "cache")
            },
            "features": {
                "consciousness": True,
                "sentience": True,
                "metacognition": True,
                "deep_learning": True,
                "computer_vision": True,
                "nlp": True,
                "financial_analysis": True,
                "quantum_computing": False,
                "sensorial_system": True
            },
            "performance": {
                "max_memory_usage": "8GB",
                "gpu_acceleration": False,
                "parallel_processing": True,
                "cache_size": "1GB"
            }
        }
        
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.print_color("OK: Arquivo de configuração criado")
    
    def test_installation(self) -> bool:
        """Testar instalação"""
        self.print_color("Testando instalação...")
        
        python_path = self.get_venv_python()
        
        try:
            # Testar import básico
            test_code = """
import sys
sys.path.insert(0, '.')
try:
    import ai_geral
    print("SUCCESS: Import successful")
    print(f"Version: {ai_geral.__version__}")
    print(f"Author: {ai_geral.__author__}")
except Exception as e:
    print(f"ERROR: {e}")
    sys.exit(1)
"""
            
            result = subprocess.run([python_path, "-c", test_code], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                self.print_color("OK: Teste de importação bem-sucedido")
                self.print_color(result.stdout.strip())
                return True
            else:
                self.print_color("ERRO: Teste de importação falhou")
                self.print_color(result.stderr.strip())
                return False
                
        except Exception as e:
            self.print_color(f"ERRO: Erro durante teste: {e}")
            return False
    
    def create_scripts(self):
        """Criar scripts de ativação"""
        self.print_color("Criando scripts de ativação...")
        
        # Script Windows
        if self.system == "windows":
            activate_script = self.install_dir / "activate_vhalinor.bat"
            with open(activate_script, 'w') as f:
                f.write(f"""@echo off
echo Ativando ambiente VHALINOR AI Geral...
call "{self.install_dir}\\vhalinor_env\\Scripts\\activate.bat"
echo Ambiente VHALINOR ativado!
echo.
echo Comandos disponíveis:
echo   vhalinor-ai          - Iniciar interface principal
echo   vhalinor-dashboard   - Iniciar dashboard
echo   vhalinor-trader      - Iniciar trader AI
echo.
python -c "import ai_geral; print('VHALINOR AI Geral v' + ai_geral.__version__ + ' pronto!')"
""")
        
        # Script Linux/Mac
        else:
            activate_script = self.install_dir / "activate_vhalinor.sh"
            with open(activate_script, 'w') as f:
                f.write(f"""#!/bin/bash
echo "Ativando ambiente VHALINOR AI Geral..."
source "{self.install_dir}/vhalinor_env/bin/activate"
echo "Ambiente VHALINOR ativado!"
echo
echo "Comandos disponíveis:"
echo "  vhalinor-ai          - Iniciar interface principal"
echo "  vhalinor-dashboard   - Iniciar dashboard"
echo "  vhalinor-trader      - Iniciar trader AI"
echo
python -c "import ai_geral; print('VHALINOR AI Geral v' + ai_geral.__version__ + ' pronto!')")
""")
            os.chmod(activate_script, 0o755)
        
        self.print_color("OK: Scripts de ativação criados")
    
    def print_summary(self):
        """Imprimir resumo da instalação"""
        self.print_color("\n" + "=" * 80)
        self.print_color("INSTALAÇÃO CONCLUÍDA COM SUCESSO!")
        self.print_color("=" * 80)
        
        self.print_color("\nResumo da instalação:")
        self.print_color(f"   Versão: {self.version}")
        self.print_color(f"   Python: {self.python_version}")
        self.print_color(f"   Sistema: {self.system}")
        self.print_color(f"   Diretório: {self.install_dir}")
        
        self.print_color("\nPara começar:")
        if self.system == "windows":
            self.print_color("   1. execute: activate_vhalinor.bat")
        else:
            self.print_color("   1. source activate_vhalinor.sh")
        
        self.print_color("   2. vhalinor-ai --help")
        self.print_color("   3. vhalinor-dashboard")
        
        self.print_color("\nDocumentação e exemplos:")
        self.print_color("   - Leia README.md para mais informações")
        self.print_color("   - Configure em config/vhalinor_config.json")
        self.print_color("   - Logs em logs/")
        
        self.print_color("\nNotas importantes:")
        self.print_color("   - Ative sempre o ambiente virtual antes de usar")
        self.print_color("   - Requer 8GB+ RAM para melhor performance")
        self.print_color("   - GPU opcional para deep learning")
        
        self.print_color("\n" + "=" * 80)
    
    def run_installation(self):
        """Executar instalação completa"""
        self.print_header()
        
        # Verificar requisitos
        if not self.check_requirements():
            self.print_color("\nERRO: Requisitos não atendidos. Instalação cancelada.")
            return False
        
        # Criar ambiente virtual
        if not self.create_virtual_env():
            return False
        
        # Atualizar pip
        if not self.upgrade_pip():
            return False
        
        # Instalar dependências
        if not self.install_dependencies():
            return False
        
        # Instalar pacote
        if not self.install_package():
            return False
        
        # Criar estrutura
        self.create_directories()
        self.create_config_file()
        self.create_scripts()
        
        # Testar instalação
        if not self.test_installation():
            self.print_color("\nAVISO: Instalação concluída com avisos. Verifique os logs.")
        
        self.print_summary()
        return True


def main():
    """Função principal"""
    installer = VhalinorInstaller()
    
    try:
        success = installer.run_installation()
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    except KeyboardInterrupt:
        installer.print_color("\n\nInstalação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        installer.print_color(f"\nERRO: Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
