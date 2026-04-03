@echo off
echo ========================================
echo VHALINOR AI Geral v6.0 - Inicializacao
echo ========================================
echo.

echo Verificando ambiente...
python --version
echo.

echo Testando importacoes basicas...
python -c "
import sys
print('Python:', sys.version)
try:
    import numpy as np
    print('OK: NumPy', np.__version__)
except ImportError:
    print('AVISO: NumPy nao disponivel')

try:
    import pandas as pd
    print('OK: Pandas', pd.__version__)
except ImportError:
    print('AVISO: Pandas nao disponivel')

try:
    import matplotlib.pyplot as plt
    print('OK: Matplotlib', matplotlib.__version__)
except ImportError:
    print('AVISO: Matplotlib nao disponivel')

try:
    import sklearn
    print('OK: Scikit-learn', sklearn.__version__)
except ImportError:
    print('AVISO: Scikit-learn nao disponivel')
"

echo.
echo Testando sistema VHALINOR...
python test_integration.py

echo.
echo ========================================
echo VHALINOR AI Geral pronto para uso!
echo ========================================
echo.
echo Comandos disponiveis:
echo   python cli.py --help
echo   python dashboard.py
echo   python examples.py
echo   python trader.py
echo.
echo Para mais informacoes, leia QUICKSTART.md
echo.
pause
