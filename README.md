# 🧠 VHALINOR-IA

**Bot de trading automatizado com inteligência artificial simbólica para análise técnica na Binance**

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Binance](https://img.shields.io/badge/Binance-API-yellow)

## 📋 Sobre o Projeto

VHALINOR-IA é um robô de trading que utiliza indicadores técnicos (RSI e MACD) para tomar decisões automatizadas de compra e venda no mercado de criptomoedas. O sistema inclui uma camada de "consciência" simulada que adiciona personalidade às decisões de trading.

## ✨ Funcionalidades

- 🤖 **IA Simbólica**: Classe `Vhalinor` com atributos de "energia" e "curiosidade"
- 📊 **Indicadores Técnicos**: RSI (14 períodos) e MACD para análise de momentum
- 🔄 **Trading Automático**: Executa ordens de mercado na Binance
- 📝 **Logging Completo**: Registro detalhado de todas as operações
- 🛡️ **Tratamento de Erros**: Gerencia falhas de API e reconexão automática
- 🧪 **Modo Testnet**: Suporte para ambiente de testes da Binance

## 🚀 Como Funciona

### Estratégia de Trading

| Condição | Ação |
|----------|------|
| RSI < 30 (sobrevenda) + MACD cruzamento bullish | **COMPRA** |
| RSI > 70 (sobrecompra) + MACD cruzamento bearish | **VENDA** |

### Loop Principal
1. Coleta dados de candles do par BTCUSDT (1 minuto)
2. Calcula indicadores técnicos
3. Avalia sinais de entrada/saída
4. Executa ordem se sinal for detectado
5. Aguarda 60 segundos e repete

## 📦 Pré-requisitos

```bash
pip install python-binance pandas ta