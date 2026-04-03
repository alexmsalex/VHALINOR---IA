@echo off
echo Iniciando VHALINOR AI Geral...
echo.
echo Ativando ambiente virtual...
call "vhalinor_env\Scripts\activate.bat"
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
