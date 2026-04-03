#!/usr/bin/env python3
"""
Setup script for VHALINOR AI Geral v6.0
=====================================
Instalação do pacote de Inteligência Artificial Geral
"""

from setuptools import setup, find_packages
import os
import sys

# Verificar versão do Python
if sys.version_info < (3, 8):
    print("ERRO: VHALINOR AI Geral requer Python 3.8 ou superior")
    sys.exit(1)

# Ler informações do arquivo __init__.py
def get_version():
    try:
        with open("__init__.py", "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("__version__"):
                    return line.split("=")[1].strip().strip('"').strip("'")
    except FileNotFoundError:
        pass
    return "6.0.0"

def get_long_description():
    """Ler README.md se existir"""
    if os.path.exists("README.md"):
        with open("README.md", "r", encoding="utf-8") as f:
            return f.read()
    return """
VHALINOR AI Geral v6.0
======================

Módulo de Inteligência Artificial Geral (AGI) com sistemas cognitivos,
consciência artificial, sentiência artificial, raciocínio avançado e aprendizado contínuo.

Características principais:
- Consciência e Sentiência Artificial
- Raciocínio Avançado e Metacognição
- Aprendizado Profundo e Contínuo
- Análise de Padrões e Mercado Financeiro
- Processamento de Linguagem e Visão Computacional
- Arquitetura Neural Orgânica
- Neurogênese e Comunicação Neural
- Sistema Sensorial Completo
- Automação Inteligente
- Ética em AI

Este pacote contém 22 módulos especializados que formam um sistema completo
de Inteligência Artificial Geral.
"""

# Ler dependências
def get_requirements():
    """Ler requirements.txt se existir"""
    requirements = []
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r", encoding="utf-8") as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    # Dependências mínimas garantidas
    minimal_requirements = [
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "tensorflow>=2.8.0",
        "torch>=1.11.0",
        "matplotlib>=3.5.0",
        "seaborn>=0.11.0",
        "plotly>=5.0.0",
        "requests>=2.27.0",
        "beautifulsoup4>=4.10.0",
        "nltk>=3.7",
        "spacy>=3.4.0",
        "transformers>=4.17.0",
        "opencv-python>=4.5.5",
        "pillow>=9.0.0",
        "PyPDF2>=2.0.0",
        "pdfplumber>=0.6.0",
        "yfinance>=0.1.70",
        "ta>=0.8.0",
        "websockets>=10.0",
        "asyncio-mqtt>=0.10.0",
        "pydantic>=1.9.0",
        "typer>=0.4.0",
        "rich>=12.0.0",
        "loguru>=0.6.0",
        "python-dotenv>=0.19.0",
        "psutil>=5.9.0",
        "memory-profiler>=0.60.0",
    ]
    
    # Combinar dependências
    all_requirements = list(set(requirements + minimal_requirements))
    return all_requirements

# Configuração do setup
setup(
    name="vhalinor-ai-geral",
    version=get_version(),
    author="VHALINOR Team",
    author_email="team@vhalinor.ai",
    description="Inteligência Artificial Geral com sistemas cognitivos avançados",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/vhalinor/ai-geral",
    project_urls={
        "Bug Tracker": "https://github.com/vhalinor/ai-geral/issues",
        "Documentation": "https://vhalinor-ai-geral.readthedocs.io/",
        "Source Code": "https://github.com/vhalinor/ai-geral",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=get_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "pre-commit>=2.17.0",
        ],
        "docs": [
            "sphinx>=4.5.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.17.0",
        ],
        "gpu": [
            "tensorflow-gpu>=2.8.0",
            "torch-audio>=0.11.0",
            "torchvision>=0.12.0",
        ],
        "quantum": [
            "qiskit>=0.36.0",
            "cirq>=0.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "vhalinor-ai=ai_geral.cli:main",
            "vhalinor-dashboard=ai_geral.dashboard:main",
            "vhalinor-trader=ai_geral.trader:main",
        ],
    },
    include_package_data=True,
    package_data={
        "ai_geral": [
            "data/*.json",
            "models/*.pkl",
            "config/*.yaml",
            "assets/*",
        ],
    },
    zip_safe=False,
    keywords=[
        "artificial intelligence",
        "machine learning",
        "deep learning",
        "neural networks",
        "consciousness",
        "sentience",
        "cognitive computing",
        "trading",
        "financial analysis",
        "nlp",
        "computer vision",
        "quantum computing",
    ],
)
