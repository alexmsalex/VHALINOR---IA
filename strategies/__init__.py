# strategies/__init__.py
"""
Pacote de estratégias de trading da VHALINOR I.A.

Este módulo contém todas as estratégias implementadas e fornece
uma interface unificada para acessá-las.
"""

import logging
from typing import Dict, List, Optional, Type
from pathlib import Path
import importlib

# Importar classes base
from ..strategy_base import Strategy, TimeFrame

# Importar estratégias concretas
from .breakout import BreakoutStrategy
from .momentum import MomentumStrategy
from .mean_reversion import MeanReversionStrategy
from .vwap import VWAPStrategy
from .ema_crossover import EMACrossoverStrategy
from .scalping import ScalpingStrategy

logger = logging.getLogger(__name__)

# ============================================================================
# Lista de instâncias (modo legado - compatível)
# ============================================================================

def _create_strategy_instances() -> List[Strategy]:
    """
    Cria instâncias de todas as estratégias com configurações padrão.
    Usa os parâmetros definidos no método __init__ de cada estratégia.
    """
    return [
        BreakoutStrategy(),
        MomentumStrategy(),
        MeanReversionStrategy(),
        VWAPStrategy(),
        EMACrossoverStrategy(),
        ScalpingStrategy(),
    ]

ALL_STRATEGIES = _create_strategy_instances()

# ============================================================================
# Acesso avançado
# ============================================================================

# Mapeamento nome -> classe (para instanciação sob demanda)
STRATEGY_CLASSES: Dict[str, Type[Strategy]] = {
    "breakout": BreakoutStrategy,
    "momentum": MomentumStrategy,
    "mean_reversion": MeanReversionStrategy,
    "vwap": VWAPStrategy,
    "ema_crossover": EMACrossoverStrategy,
    "scalping": ScalpingStrategy,
}

# Mapeamento nome -> instância padrão (para acesso rápido)
STRATEGY_INSTANCES: Dict[str, Strategy] = {
    s.name.lower(): s for s in ALL_STRATEGIES
}


def get_strategy(name: str) -> Optional[Strategy]:
    """
    Retorna uma instância padrão da estratégia pelo nome.
    
    Args:
        name: Nome da estratégia (case-insensitive)
        
    Returns:
        Instância da estratégia ou None se não encontrada
    """
    key = name.lower().replace(" ", "_")
    return STRATEGY_INSTANCES.get(key)


def get_strategy_class(name: str) -> Optional[Type[Strategy]]:
    """Retorna a classe da estratégia pelo nome."""
    key = name.lower().replace(" ", "_")
    return STRATEGY_CLASSES.get(key)


def create_strategy(name: str, **kwargs) -> Optional[Strategy]:
    """
    Cria uma nova instância da estratégia com parâmetros customizados.
    
    Args:
        name: Nome da estratégia
        **kwargs: Parâmetros para o construtor da estratégia
        
    Returns:
        Nova instância ou None se estratégia não existe
    """
    strategy_class = get_strategy_class(name)
    if strategy_class:
        return strategy_class(**kwargs)
    logger.warning(f"Estratégia '{name}' não encontrada")
    return None


def list_strategies() -> List[Dict[str, any]]:
    """
    Retorna metadados de todas as estratégias disponíveis.
    
    Returns:
        Lista de dicionários com informações de cada estratégia
    """
    strategies_info = []
    for strategy in ALL_STRATEGIES:
        info = {
            "name": strategy.name,
            "risk_percent": strategy.risk_percent,
            "timeframe": strategy.timeframe.value,
            "min_history_bars": strategy.min_history_bars,
            "require_volume": strategy.require_volume,
            "cooldown_bars": strategy.cooldown_bars,
            "class": strategy.__class__.__name__,
        }
        strategies_info.append(info)
    return strategies_info


def filter_strategies_by_timeframe(timeframe: TimeFrame) -> List[Strategy]:
    """Retorna estratégias compatíveis com um determinado timeframe."""
    return [s for s in ALL_STRATEGIES if s.timeframe == timeframe]


def filter_strategies_by_risk(max_risk_percent: float) -> List[Strategy]:
    """Retorna estratégias com risco percentual <= max_risk_percent."""
    return [s for s in ALL_STRATEGIES if s.risk_percent <= max_risk_percent]


def reload_strategies():
    """
    Recarrega as instâncias das estratégias (útil após alterações de configuração).
    """
    global ALL_STRATEGIES, STRATEGY_INSTANCES
    ALL_STRATEGIES = _create_strategy_instances()
    STRATEGY_INSTANCES = {s.name.lower(): s for s in ALL_STRATEGIES}
    logger.info("Estratégias recarregadas")


# ============================================================================
# Importação dinâmica (para estratégias adicionais em plugins)
# ============================================================================

def discover_strategies(plugin_dir: str = "strategies/custom"):
    """
    Descobre e carrega automaticamente estratégias de arquivos Python em um diretório.
    Útil para estratégias customizadas sem modificar o núcleo.
    
    Args:
        plugin_dir: Caminho relativo para o diretório de plugins
        
    Returns:
        Lista de estratégias encontradas
    """
    discovered = []
    plugin_path = Path(plugin_dir)
    
    if not plugin_path.exists():
        logger.debug(f"Diretório de plugins não encontrado: {plugin_dir}")
        return discovered
    
    for py_file in plugin_path.glob("*.py"):
        if py_file.name.startswith("_"):
            continue
        
        module_name = f"strategies.custom.{py_file.stem}"
        try:
            module = importlib.import_module(module_name)
            # Procurar classes que são subclasses de Strategy
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if (isinstance(attr, type) and 
                    issubclass(attr, Strategy) and 
                    attr is not Strategy):
                    strategy_instance = attr()
                    discovered.append(strategy_instance)
                    logger.info(f"Estratégia descoberta: {strategy_instance.name}")
        except Exception as e:
            logger.error(f"Erro ao carregar {py_file.name}: {e}")
    
    return discovered


# ============================================================================
# Compatibilidade com código legado (mantém ALL_STRATEGIES)
# ============================================================================

# Opcional: estender ALL_STRATEGIES com estratégias descobertas
# _custom_strategies = discover_strategies()
# ALL_STRATEGIES.extend(_custom_strategies)
# STRATEGY_INSTANCES.update({s.name.lower(): s for s in _custom_strategies})

# ============================================================================
# Exemplo de uso (se executar diretamente)
# ============================================================================

if __name__ == "__main__":
    # Teste rápido
    print("=== Estratégias disponíveis ===")
    for info in list_strategies():
        print(f"  {info['name']}: risco={info['risk_percent']}%, tf={info['timeframe']}")
    
    print("\n=== Acessando estratégia por nome ===")
    strat = get_strategy("momentum")
    if strat:
        print(f"Encontrado: {strat}")
    
    print("\n=== Estratégias com timeframe H1 ===")
    h1_strats = filter_strategies_by_timeframe(TimeFrame.H1)
    for s in h1_strats:
        print(f"  {s.name}")