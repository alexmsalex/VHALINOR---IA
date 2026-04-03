@echo off
echo Ativando ambiente VHALINOR AI Geral...
call "vhalinor_env\Scripts\activate.bat"
echo Ambiente VHALINOR ativado!
echo.
echo Comandos disponíveis:
echo   python test_installation.py  - Testar instalação
echo   python -c "import sys; print('Python:', sys.version)"
echo   python -c "import numpy, pandas; print('NumPy:', numpy.__version__, 'Pandas:', pandas.__version__)"
echo.
echo Para usar os módulos VHALINOR:
echo   import sys
echo   sys.path.insert(0, '.')
echo   # Importe os módulos desejados
echo.
python -c "import sys; sys.path.insert(0, '.'); print('VHALINOR AI Geral v6.0.0 pronto!')"
