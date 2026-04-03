# VHALINOR AI Geral v6.0.0 - Guia de Uso Rápido
# ============================================

## 🚀 Como Começar

### 1. Ativar o Ambiente Virtual
```bash
# Windows
activate_vhalinor.bat

# Ou manualmente
vhalinor_env\Scripts\activate
```

### 2. Testar a Instalação
```bash
python test_installation.py
```

### 3. Executar o Sistema

#### Interface de Linha de Comando (CLI)
```bash
python cli.py --help
python cli.py status
python cli.py chat "Olá, como você está?"
python cli.py analisar PETR4
python cli.py demo --tipo completo
```

#### Interface Gráfica (GUI)
```bash
python dashboard.py
```

#### Dashboard Web (Streamlit)
```bash
# Instalar streamlit primeiro
pip install streamlit streamlit-plotly-events

# Executar
streamlit run web_dashboard.py
```

#### Sistema de Trading
```bash
python trader.py
```

#### Exemplos e Demonstrações
```bash
python examples.py
```

#### Teste de Integração
```bash
python test_integration.py
```

## 📋 Estrutura do Projeto

```
ai_geral/
├── 🧠 Módulos Cognitivos
│   ├── consciencia_artificial.py      # Consciência e autoconsciência
│   ├── sentiencia_artificial.py       # Emoções e experiência subjetiva
│   ├── raciocinio_avancado.py         # Lógica e inferência
│   ├── memoria_cognitiva.py           # Memória de longo prazo
│   └── metacognicao.py                # Pensamento sobre pensamento
│
├── 🎓 Aprendizado e Evolução
│   ├── aprendizado_profundo.py         # Deep Learning
│   ├── aprendizado_continuo.py         # Lifelong learning
│   ├── evolucao_aprendizado.py         # Evolução natural de modelos
│   └── arquitetura_organica.py        # Cérebro biológico simulado
│
├── 📊 Análise e Processamento
│   ├── analise_mercado_financeiro.py  # Análise financeira
│   ├── analise_day_trade.py            # Day trading
│   ├── analise_noticias.py             # Análise de notícias
│   ├── processamento_linguagem.py     # NLP avançado
│   ├── visao_computacional.py          # Computer vision
│   └── leitor_pdf.py                  # Processamento de PDFs
│
├── 🔧 Sistemas e Automação
│   ├── automacao.py                   # Automação inteligente
│   ├── tomada_decisao.py              # Tomada de decisão
│   ├── arquitetura_sistema.py         # Arquitetura completa
│   └── neurogenese_comunicacao.py     # Neurogênese
│
├── 🌐 Interfaces
│   ├── cli.py                         # Interface linha de comando
│   ├── dashboard.py                   # Interface gráfica (Tkinter)
│   ├── web_dashboard.py               # Dashboard web (Streamlit)
│   └── trader.py                      # Sistema de trading
│
└── 📝 Utilitários
    ├── setup.py                       # Instalação do pacote
    ├── requirements.txt               # Dependências
    ├── install.py                     # Instalador automatizado
    ├── examples.py                    # Exemplos e demos
    ├── test_integration.py            # Teste de integração
    └── README.md                      # Documentação completa
```

## 🎯 Exemplos de Uso

### Consciência Artificial
```python
from consciencia_artificial import ConscienciaArtificial

consciencia = ConscienciaArtificial()
consciencia.inicializar()
estado = consciencia.obter_estado()
print(f"Nível de consciência: {estado.nivel}")
```

### Análise de Mercado
```python
from analise_mercado_financeiro import AnaliseMercadoFinanceiro

analise = AnaliseMercadoFinanceiro()
resultado = analise.analisar_ativo("PETR4")
print(f"Recomendação: {resultado['recomendacao']}")
```

### Processamento de Linguagem
```python
from processamento_linguagem import ProcessamentoLinguagem

nlp = ProcessamentoLinguagem()
resultado = nlp.analisar_completo("O mercado está em alta hoje")
print(f"Sentimento: {resultado['sentimento']}")
```

### Sistema de Trading
```python
from trader import VhalinorTradingSystem

trading = VhalinorTradingSystem(capital_inicial=10000)
analise = trading.analisar_ativo_completo("PETR4")
print(f"Decisão: {analise['decisao_final']['acao']}")
```

## 🔧 Configuração

### Variáveis de Ambiente
```bash
# Configurar API keys (opcional)
export OPENAI_API_KEY="sua_key"
export ALPHA_VANTAGE_API_KEY="sua_key"
```

### Arquivo de Configuração
```json
{
  "version": "6.0.0",
  "features": {
    "consciousness": true,
    "sentience": true,
    "deep_learning": true,
    "trading": true
  },
  "performance": {
    "max_memory_usage": "8GB",
    "parallel_processing": true
  }
}
```

## 📊 Monitoramento e Logs

### Ver Logs
```bash
# Logs em tempo real
tail -f logs/vhalinor.log

# Logs específicos
tail -f logs/consciencia.log
tail -f logs/trading.log
```

### Métricas de Performance
```python
from arquitetura_sistema import arquitetura_vhalinor

metricas = arquitetura_vhalinor.obter_metricas()
print(f"Componentes ativos: {metricas['componentes_ativos']}")
```

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Criar branch (`git checkout -b feature/nova-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push (`git push origin feature/nova-feature`)
5. Criar Pull Request

### Diretrizes
- Seguir PEP 8
- Adicionar testes
- Documentar funções
- Usar type hints

## 🆘 Suporte

### Comandos Úteis
```bash
# Verificar instalação
python test_installation.py

# Testar integração completa
python test_integration.py

# Executar demonstração completa
python examples.py

# Ver status do sistema
python cli.py status
```

### Resolução de Problemas

#### Erros Comuns
1. **ModuleNotFoundError**: Instale as dependências faltantes
   ```bash
   pip install -r requirements.txt
   ```

2. **UnicodeEncodeError**: Use o ambiente virtual
   ```bash
   activate_vhalinor.bat
   ```

3. **ImportError**: Verifique se está no diretório correto
   ```bash
   cd ai_geral
   ```

## 📈 Performance

### Otimizações
- Use o ambiente virtual para isolamento
- Configure a memória máxima para uso
- Ative o processamento paralelo quando possível
- Monitore o uso de CPU e memória

### Recomendações de Hardware
- **Mínimo**: 8GB RAM, CPU dual-core
- **Recomendado**: 16GB RAM, CPU quad-core
- **Ideal**: 32GB RAM, CPU octa-core, GPU para deep learning

## 🎉 Divirta-se!

Explore todos os módulos e descubra o poder da Inteligência Artificial Geral VHALINOR!

---
**VHALINOR AI Geral v6.0.0 - O futuro da inteligência artificial está aqui**
