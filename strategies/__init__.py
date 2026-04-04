from .breakout import BreakoutStrategy
from .momentum import MomentumStrategy
from .mean_reversion import MeanReversionStrategy
from .vwap import VWAPStrategy
from .ema_crossover import EMACrossoverStrategy
from .scalping import ScalpingStrategy

ALL_STRATEGIES = [
    BreakoutStrategy(),
    MomentumStrategy(),
    MeanReversionStrategy(),
    VWAPStrategy(),
    EMACrossoverStrategy(),
    ScalpingStrategy(),
]