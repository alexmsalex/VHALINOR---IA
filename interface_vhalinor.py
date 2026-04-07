# vhalinor_interface.py
import os
import sys
import logging
import signal
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

class VhalinorInterface:
    """Interface principal para o sistema VHALINOR I.A."""
    
    def __init__(self):
        self.logger: Optional[logging.Logger] = None
        self.config: Dict[str, Any] = {}
        self.start_time: Optional[datetime] = None
        self.running = False
        
    def setup_logging(self, log_level: str = "INFO", log_dir: str = "logs") -> logging.Logger:
        """Configura o sistema de logging com rotação de arquivos."""
        # Criar diretório de logs se não existir
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # Configurar nível de log
        level = getattr(logging, log_level.upper(), logging.INFO)
        
        # Nome do arquivo de log com data
        log_file = log_path / f"vhalinor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Configurar logging
        logging.basicConfig(
            level=level,
            format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[
                logging.FileHandler(log_file, encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"📝 Sistema de logging inicializado - Arquivo: {log_file}")
        return self.logger
    
    def load_config(self, config_file: Optional[str] = None) -> Dict[str, Any]:
        """Carrega configurações de um arquivo JSON."""
        default_config = {
            "trading": {
                "exchange": "binance",
                "market_type": "futures",
                "symbols": ["BTC/USDT", "ETH/USDT"],
                "timeframe": "5m",
                "max_positions": 3,
                "risk_per_trade": 0.02  # 2% risk per trade
            },
            "strategy": {
                "name": "adaptive_ml",
                "parameters": {
                    "rsi_period": 14,
                    "bb_period": 20,
                    "atr_period": 14
                }
            },
            "system": {
                "headless": True,
                "debug": False,
                "max_retries": 3,
                "heartbeat_interval": 60  # seconds
            }
        }
        
        if config_file and Path(config_file).exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # Merge configs (deep merge would be better)
                    default_config.update(user_config)
                self.logger.info(f"⚙️ Configuração carregada de: {config_file}")
            except Exception as e:
                self.logger.warning(f"⚠️ Erro ao carregar configuração: {e}. Usando padrão.")
        else:
            self.logger.info("⚙️ Usando configuração padrão")
            
        self.config = default_config
        return self.config
    
    def save_config(self, config_file: str = "config.json"):
        """Salva a configuração atual em arquivo."""
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            self.logger.info(f"💾 Configuração salva em: {config_file}")
        except Exception as e:
            self.logger.error(f"❌ Erro ao salvar configuração: {e}")
    
    def check_environment(self) -> bool:
        """Verifica se o ambiente está pronto para execução."""
        self.logger.info("🔍 Verificando ambiente...")
        issues = []
        
        # Verificar Python version
        if sys.version_info < (3, 8):
            issues.append(f"Python {sys.version_info.major}.{sys.version_info.minor} - Recomendado >= 3.8")
        
        # Verificar diretórios necessários
        required_dirs = ["logs", "data", "models", "reports"]
        for dir_name in required_dirs:
            Path(dir_name).mkdir(exist_ok=True)
            self.logger.debug(f"Diretório verificado: {dir_name}")
        
        # Verificar módulos críticos
        critical_modules = ['ccxt', 'pandas', 'numpy']
        for module in critical_modules:
            try:
                __import__(module)
                self.logger.debug(f"✅ Módulo {module} disponível")
            except ImportError:
                issues.append(f"Módulo {module} não encontrado. Instale com: pip install {module}")
        
        if issues:
            self.logger.warning("⚠️ Problemas encontrados:")
            for issue in issues:
                self.logger.warning(f"   - {issue}")
            return False
        
        self.logger.info("✅ Ambiente verificado com sucesso")
        return True
    
    def signal_handler(self, signum, frame):
        """Trata sinais do sistema para desligamento gracioso."""
        self.logger.info(f"\n🛑 Recebido sinal {signum}. Iniciando desligamento gracioso...")
        self.shutdown()
        sys.exit(0)
    
    def shutdown(self):
        """Executa procedimentos de desligamento."""
        self.running = False
        if self.start_time:
            runtime = datetime.now() - self.start_time
            self.logger.info(f"⏱️  Tempo total de execução: {runtime}")
        
        # Aqui você pode adicionar mais cleanup se necessário
        self.logger.info("👋 VHALINOR I.A encerrado")
    
    def print_banner(self):
        """Exibe banner do sistema."""
        banner = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██╗   ██╗██╗  ██╗ █████╗ ██╗     ██╗███╗   ██╗ ██████╗ ██████╗ ║
║   ██║   ██║██║  ██║██╔══██╗██║     ██║████╗  ██║██╔═══██╗██╔══██╗║
║   ██║   ██║███████║███████║██║     ██║██╔██╗ ██║██║   ██║██████╔╝║
║   ██║   ██║██╔══██║██╔══██║██║     ██║██║╚██╗██║██║   ██║██╔══██╗║
║   ╚██████╔╝██║  ██║██║  ██║███████╗██║██║ ╚████║╚██████╔╝██║  ██║║
║    ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝║
║                                                          ║
║           Intelligent Autonomous Trading System         ║
║                    Headless Mode Ready                   ║
╚══════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def run(self, args):
        """Executa o sistema principal."""
        # Configurar handlers de sinal
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Exibir banner
        if not args.quiet:
            self.print_banner()
        
        # Configurar logging
        log_level = args.log_level or "INFO"
        self.setup_logging(log_level=log_level)
        
        # Carregar configuração
        self.load_config(args.config)
        
        # Verificar ambiente
        if not self.check_environment():
            if not args.force:
                self.logger.error("❌ Ambiente não satisfaz requisitos. Use --force para ignorar.")
                sys.exit(1)
            self.logger.warning("⚠️ Continuando mesmo com problemas no ambiente (--force ativado)")
        
        # Iniciar sistema
        self.start_time = datetime.now()
        self.running = True
        
        self.logger.info("🚀 Iniciando VHALINOR I.A - Modo Headless")
        self.logger.info(f"📅 Data/Hora: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"🏦 Exchange: {self.config['trading']['exchange'].upper()} Futures")
        self.logger.info(f"📊 Símbolos: {', '.join(self.config['trading']['symbols'])}")
        self.logger.info(f"⚙️  Modo debug: {self.config['system']['debug']}")
        
        # Importar e executar o main da VHALINOR
        try:
            from vhalinor.main import VhalinorTradingSystem
            
            # Criar instância do sistema de trading
            trading_system = VhalinorTradingSystem(config=self.config, logger=self.logger)
            
            # Iniciar o loop de trading
            self.logger.info("✅ Módulos carregados. Iniciando loop de trading...")
            trading_system.run()  # Assumindo que run() é o método principal
            
        except ImportError as e:
            self.logger.error(f"❌ Erro ao importar módulo principal: {e}")
            self.logger.error("   Certifique-se que vhalinor/main.py existe e contém VhalinorTradingSystem")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"❌ Erro fatal durante execução: {e}", exc_info=True)
            sys.exit(1)
        finally:
            self.shutdown()


def parse_arguments():
    """Parse argumentos de linha de comando."""
    parser = argparse.ArgumentParser(
        description="VHALINOR I.A - Sistema Autônomo de Trading Inteligente",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "-c", "--config",
        type=str,
        default="config.json",
        help="Arquivo de configuração JSON (padrão: config.json)"
    )
    
    parser.add_argument(
        "-l", "--log-level",
        type=str,
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Nível de logging (padrão: INFO)"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Modo silencioso (sem banner)"
    )
    
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="Forçar execução mesmo com problemas no ambiente"
    )
    
    parser.add_argument(
        "--save-config",
        action="store_true",
        help="Salvar configuração padrão e sair"
    )
    
    return parser.parse_args()


def main():
    """Função principal."""
    args = parse_arguments()
    interface = VhalinorInterface()
    
    # Se solicitado, salvar configuração padrão
    if args.save_config:
        interface.setup_logging(log_level="INFO")
        interface.load_config(None)
        interface.save_config(args.config)
        print(f"✅ Configuração padrão salva em: {args.config}")
        sys.exit(0)
    
    # Executar interface
    interface.run(args)


if __name__ == "__main__":
    main()