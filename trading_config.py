"""
Configurações de Trading para o Bot VHALINOR-IA
Centraliza todos os parâmetros de trading com validações e documentação
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional
from enum import Enum
import json
from pathlib import Path

# ============================================
# ENUMS PARA VALORES VÁLIDOS
# ============================================

class IntervaloTempo(Enum):
    """Intervalos de candle disponíveis na Binance"""
    MINUTO_1 = "1m"
    MINUTO_3 = "3m"
    MINUTO_5 = "5m"
    MINUTO_15 = "15m"
    MINUTO_30 = "30m"
    HORA_1 = "1h"
    HORA_2 = "2h"
    HORA_4 = "4h"
    HORA_6 = "6h"
    HORA_8 = "8h"
    HORA_12 = "12h"
    DIA_1 = "1d"
    DIA_3 = "3d"
    SEMANA_1 = "1w"
    
    @classmethod
    def listar(cls):
        return [intervalo.value for intervalo in cls]

class SimboloMoeda(Enum):
    """Pares de trading populares"""
    BTC_USDT = "BTCUSDT"
    ETH_USDT = "ETHUSDT"
    BNB_USDT = "BNBUSDT"
    ADA_USDT = "ADAUSDT"
    SOL_USDT = "SOLUSDT"
    XRP_USDT = "XRPUSDT"
    DOGE_USDT = "DOGEUSDT"
    DOT_USDT = "DOTUSDT"
    MATIC_USDT = "MATICUSDT"
    
    @classmethod
    def listar(cls):
        return [simbolo.value for simbolo in cls]

# ============================================
# CONFIGURAÇÃO PRINCIPAL
# ============================================

@dataclass
class TradingConfig:
    """
    Configurações completas de trading para o bot
    
    Attributes:
        symbol: Par de trading (ex: BTCUSDT)
        interval: Intervalo de candles (ex: 1m, 5m, 1h)
        quantity: Quantidade base por trade (em moeda base, ex: BTC)
        risk_per_trade: Risco por trade (% do capital, 0.01 = 1%)
        max_positions: Número máximo de posições simultâneas
        stop_loss_percent: Stop loss em porcentagem (ex: 2.0 = 2%)
        take_profit_percent: Take profit em porcentagem
        trailing_stop: Usar trailing stop
        trailing_stop_percent: Percentual do trailing stop
        min_volume_24h: Volume mínimo em 24h (USDT)
        max_spread_percent: Spread máximo permitido (%)
        slippage_tolerance: Tolerância de slippage (%)
        order_timeout: Timeout para ordens (segundos)
        retry_attempts: Tentativas de retry em caso de falha
    """
    
    # Configurações básicas
    symbol: str = "BTCUSDT"
    interval: str = "1m"
    quantity: float = 0.001
    risk_per_trade: float = 0.01
    
    # Gerenciamento de risco
    max_positions: int = 3
    stop_loss_percent: float = 2.0
    take_profit_percent: float = 4.0
    trailing_stop: bool = False
    trailing_stop_percent: float = 1.0
    
    # Filtros de mercado
    min_volume_24h: float = 1000000  # 1 milhão USDT
    max_spread_percent: float = 0.5  # 0.5%
    min_liquidity: float = 10000  # 10k USDT
    
    # Execução de ordens
    slippage_tolerance: float = 0.1  # 0.1%
    order_timeout: int = 30  # segundos
    retry_attempts: int = 3
    retry_delay: int = 5  # segundos
    
    # Limites de trading
    max_daily_trades: int = 50
    max_position_size_usdt: float = 1000  # Máximo por posição em USDT
    min_order_value_usdt: float = 10  # Mínimo por ordem
    
    # Modo de operação
    use_testnet: bool = True
    paper_trading: bool = False  # Simular trades sem executar
    log_trades: bool = True
    save_trade_history: bool = True
    
    # Meta informações
    version: str = "1.0.0"
    description: str = "Configuração padrão para trading automatizado"
    
    def __post_init__(self):
        """Validações automáticas após inicialização"""
        self.validate()
    
    def validate(self) -> bool:
        """
        Valida todos os parâmetros de configuração
        
        Returns:
            bool: True se válido
            
        Raises:
            ValueError: Se algum parâmetro for inválido
        """
        # Valida symbol
        if not isinstance(self.symbol, str) or len(self.symbol) < 6:
            raise ValueError(f"Symbol inválido: {self.symbol}")
        
        # Valida interval
        if self.interval not in IntervaloTempo.listar():
            raise ValueError(f"Intervalo inválido: {self.interval}. Use: {IntervaloTempo.listar()}")
        
        # Valida quantity
        if self.quantity <= 0:
            raise ValueError(f"Quantidade deve ser positiva: {self.quantity}")
        if self.quantity > 100:
            raise ValueError(f"Quantidade muito alta: {self.quantity}")
        
        # Valida risk_per_trade
        if not 0 < self.risk_per_trade <= 0.5:
            raise ValueError(f"risk_per_trade deve estar entre 0 e 0.5: {self.risk_per_trade}")
        
        # Valida stop loss e take profit
        if self.stop_loss_percent <= 0:
            raise ValueError(f"stop_loss_percent deve ser positivo: {self.stop_loss_percent}")
        if self.take_profit_percent <= self.stop_loss_percent:
            raise ValueError(f"take_profit_percent ({self.take_profit_percent}) deve ser maior que stop_loss_percent ({self.stop_loss_percent})")
        
        # Valida trailing stop
        if self.trailing_stop and self.trailing_stop_percent <= 0:
            raise ValueError(f"trailing_stop_percent deve ser positivo: {self.trailing_stop_percent}")
        
        # Valida limites
        if self.max_daily_trades < 1:
            raise ValueError(f"max_daily_trades deve ser >= 1: {self.max_daily_trades}")
        if self.min_order_value_usdt < 10:
            raise ValueError(f"min_order_value_usdt muito baixo (mínimo 10 USDT): {self.min_order_value_usdt}")
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte configuração para dicionário"""
        return {
            'basic': {
                'symbol': self.symbol,
                'interval': self.interval,
                'quantity': self.quantity,
                'risk_per_trade': self.risk_per_trade
            },
            'risk_management': {
                'max_positions': self.max_positions,
                'stop_loss_percent': self.stop_loss_percent,
                'take_profit_percent': self.take_profit_percent,
                'trailing_stop': self.trailing_stop,
                'trailing_stop_percent': self.trailing_stop_percent
            },
            'market_filters': {
                'min_volume_24h': self.min_volume_24h,
                'max_spread_percent': self.max_spread_percent,
                'min_liquidity': self.min_liquidity
            },
            'order_execution': {
                'slippage_tolerance': self.slippage_tolerance,
                'order_timeout': self.order_timeout,
                'retry_attempts': self.retry_attempts,
                'retry_delay': self.retry_delay
            },
            'limits': {
                'max_daily_trades': self.max_daily_trades,
                'max_position_size_usdt': self.max_position_size_usdt,
                'min_order_value_usdt': self.min_order_value_usdt
            },
            'mode': {
                'use_testnet': self.use_testnet,
                'paper_trading': self.paper_trading,
                'log_trades': self.log_trades,
                'save_trade_history': self.save_trade_history
            },
            'metadata': {
                'version': self.version,
                'description': self.description
            }
        }
    
    def save_to_file(self, filename: str = "trading_config.json"):
        """Salva configuração em arquivo JSON"""
        with open(filename, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"✅ Configuração salva em {filename}")
    
    @classmethod
    def load_from_file(cls, filename: str = "trading_config.json") -> 'TradingConfig':
        """Carrega configuração de arquivo JSON"""
        if not Path(filename).exists():
            raise FileNotFoundError(f"Arquivo {filename} não encontrado")
        
        with open(filename, 'r') as f:
            data = json.load(f)
        
        # Extrai valores do JSON
        basic = data.get('basic', {})
        risk = data.get('risk_management', {})
        market = data.get('market_filters', {})
        order = data.get('order_execution', {})
        limits = data.get('limits', {})
        mode = data.get('mode', {})
        
        return cls(
            symbol=basic.get('symbol', 'BTCUSDT'),
            interval=basic.get('interval', '1m'),
            quantity=basic.get('quantity', 0.001),
            risk_per_trade=basic.get('risk_per_trade', 0.01),
            max_positions=risk.get('max_positions', 3),
            stop_loss_percent=risk.get('stop_loss_percent', 2.0),
            take_profit_percent=risk.get('take_profit_percent', 4.0),
            trailing_stop=risk.get('trailing_stop', False),
            trailing_stop_percent=risk.get('trailing_stop_percent', 1.0),
            min_volume_24h=market.get('min_volume_24h', 1000000),
            max_spread_percent=market.get('max_spread_percent', 0.5),
            min_liquidity=market.get('min_liquidity', 10000),
            slippage_tolerance=order.get('slippage_tolerance', 0.1),
            order_timeout=order.get('order_timeout', 30),
            retry_attempts=order.get('retry_attempts', 3),
            retry_delay=order.get('retry_delay', 5),
            max_daily_trades=limits.get('max_daily_trades', 50),
            max_position_size_usdt=limits.get('max_position_size_usdt', 1000),
            min_order_value_usdt=limits.get('min_order_value_usdt', 10),
            use_testnet=mode.get('use_testnet', True),
            paper_trading=mode.get('paper_trading', False),
            log_trades=mode.get('log_trades', True),
            save_trade_history=mode.get('save_trade_history', True)
        )
    
    def get_position_size_usdt(self, current_price: float, capital_usdt: float) -> float:
        """
        Calcula tamanho da posição baseado no risco
        
        Args:
            current_price: Preço atual do ativo
            capital_usdt: Capital total em USDT
        
        Returns:
            float: Tamanho da posição em USDT
        """
        risk_amount = capital_usdt * self.risk_per_trade
        position_size = risk_amount / (self.stop_loss_percent / 100)
        
        # Aplica limites
        position_size = min(position_size, self.max_position_size_usdt)
        position_size = max(position_size, self.min_order_value_usdt)
        
        # Converte para quantidade do ativo
        quantity = position_size / current_price
        
        return quantity
    
    def display(self):
        """Exibe configuração formatada"""
        print("\n" + "="*60)
        print(f"📊 CONFIGURAÇÕES DE TRADING - {self.version}")
        print("="*60)
        
        print("\n📈 PARÂMETROS BÁSICOS:")
        print(f"  • Par de trading: {self.symbol}")
        print(f"  • Intervalo: {self.interval}")
        print(f"  • Quantidade por trade: {self.quantity} {self.symbol.replace('USDT', '')}")
        print(f"  • Risco por trade: {self.risk_per_trade*100}% do capital")
        
        print("\n🛡️ GERENCIAMENTO DE RISCO:")
        print(f"  • Máx. posições simultâneas: {self.max_positions}")
        print(f"  • Stop Loss: {self.stop_loss_percent}%")
        print(f"  • Take Profit: {self.take_profit_percent}%")
        if self.trailing_stop:
            print(f"  • Trailing Stop: {self.trailing_stop_percent}%")
        
        print("\n🔍 FILTROS DE MERCADO:")
        print(f"  • Volume mínimo 24h: ${self.min_volume_24h:,.0f}")
        print(f"  • Spread máximo: {self.max_spread_percent}%")
        
        print("\n⚙️ LIMITES OPERACIONAIS:")
        print(f"  • Trades por dia: {self.max_daily_trades}")
        print(f"  • Posição máxima: ${self.max_position_size_usdt:,.0f}")
        print(f"  • Ordem mínima: ${self.min_order_value_usdt:,.0f}")
        
        print("\n🎮 MODO DE OPERAÇÃO:")
        print(f"  • Testnet: {'✅' if self.use_testnet else '❌'}")
        print(f"  • Paper Trading: {'✅' if self.paper_trading else '❌'}")
        print(f"  • Log de trades: {'✅' if self.log_trades else '❌'}")
        
        print("\n" + "="*60)

# ============================================
# PERFIS PRÉ-CONFIGURADOS
# ============================================

class PerfilTrading:
    """Perfis de configuração pré-definidos"""
    
    @staticmethod
    def conservador() -> TradingConfig:
        """Perfil conservador - baixo risco"""
        return TradingConfig(
            quantity=0.0005,
            risk_per_trade=0.005,  # 0.5%
            max_positions=2,
            stop_loss_percent=1.5,
            take_profit_percent=3.0,
            max_daily_trades=20,
            max_position_size_usdt=500
        )
    
    @staticmethod
    def moderado() -> TradingConfig:
        """Perfil moderado - risco médio"""
        return TradingConfig(
            quantity=0.001,
            risk_per_trade=0.01,  # 1%
            max_positions=3,
            stop_loss_percent=2.0,
            take_profit_percent=4.0,
            trailing_stop=True,
            trailing_stop_percent=1.0,
            max_daily_trades=50,
            max_position_size_usdt=1000
        )
    
    @staticmethod
    def agressivo() -> TradingConfig:
        """Perfil agressivo - alto risco"""
        return TradingConfig(
            quantity=0.002,
            risk_per_trade=0.02,  # 2%
            max_positions=5,
            stop_loss_percent=3.0,
            take_profit_percent=6.0,
            trailing_stop=True,
            trailing_stop_percent=2.0,
            max_daily_trades=100,
            max_position_size_usdt=2000,
            min_volume_24h=500000
        )
    
    @staticmethod
    def scalping() -> TradingConfig:
        """Perfil Scalping - trades muito curtos"""
        return TradingConfig(
            interval="1m",
            quantity=0.0005,
            risk_per_trade=0.003,  # 0.3%
            max_positions=1,
            stop_loss_percent=0.5,
            take_profit_percent=1.0,
            max_daily_trades=200,
            max_position_size_usdt=300,
            slippage_tolerance=0.05
        )
    
    @staticmethod
    def swing_trade() -> TradingConfig:
        """Perfil Swing Trade - posições mais longas"""
        return TradingConfig(
            interval="1h",
            quantity=0.002,
            risk_per_trade=0.015,  # 1.5%
            max_positions=4,
            stop_loss_percent=4.0,
            take_profit_percent=8.0,
            trailing_stop=True,
            trailing_stop_percent=2.0,
            max_daily_trades=10,
            max_position_size_usdt=1500
        )

# ============================================
# USO PRÁTICO
# ============================================

if __name__ == "__main__":
    # Exemplo 1: Configuração padrão
    config = TradingConfig()
    config.display()
    
    # Exemplo 2: Carregar perfil específico
    print("\n" + "="*60)
    print("PERFIL MODERADO")
    config_moderado = PerfilTrading.moderado()
    config_moderado.display()
    
    # Exemplo 3: Salvar configuração
    config.save_to_file("minha_config.json")
    
    # Exemplo 4: Calcular tamanho de posição
    preco_btc = 45000
    capital_total = 10000
    quantidade = config.get_position_size_usdt(preco_btc, capital_total)
    print(f"\n💡 Tamanho da posição sugerido: {quantidade:.4f} BTC (${quantidade * preco_btc:,.2f})")