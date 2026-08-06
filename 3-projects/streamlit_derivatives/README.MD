# Fintech · análise de ações

Dashboard financeiro em Streamlit para explorar ações brasileiras, BDRs e ativos internacionais. A interface reúne preço, fundamentos, demonstrações financeiras, indicadores técnicos, risco, comparação com benchmarks e exportação dos dados.

## Principais recursos

- Busca de ações e ETFs pelo nome ou ticker.
- Tema profissional azul e branco, com layout responsivo.
- Cotação, variação, valor de mercado, P/L e dividend yield.
- Candlestick, volume e médias móveis de 20, 50 e 200 períodos.
- RSI, MACD, bandas de Bollinger e drawdown.
- Retorno anualizado, volatilidade, Sharpe e VaR histórico.
- Comparação normalizada com Ibovespa, S&P 500, Nasdaq 100 ou dólar.
- Ranking de até seis ativos pares.
- Múltiplos, margens, crescimento, endividamento e proventos.
- Resultado, balanço e fluxo de caixa anuais.
- Tabela histórica e download em CSV.

## Instalação

Se o ambiente virtual existente não abrir no seu terminal, recrie-o para garantir uma instalação limpa e reproduzível:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Se o comando `py` não estiver disponível, instale o Python 3.13 e marque a opção para adicioná-lo ao `PATH`.

## Execução

```powershell
streamlit run app.py
```

O Streamlit abrirá o dashboard em `http://localhost:8501`.

## Estrutura

```text
streamlit_cvm/
├── .streamlit/config.toml       # identidade visual
├── app.py                       # interface e navegação
├── services/
│   ├── charts.py                # gráficos Plotly
│   ├── indicators.py            # indicadores técnicos e risco
│   ├── metrics.py               # formatação e KPIs
│   ├── sidebar.py               # busca e filtros globais
│   └── yahoo_service.py         # acesso e cache dos dados
└── requirements.txt
```

## Fontes e limitações

As cotações, os indicadores e as demonstrações financeiras são obtidos do Yahoo Finance e podem ter atraso, lacunas ou diferenças em relação aos documentos regulatórios. Para análises profissionais, confira os valores nos documentos oficiais da CVM/B3 ou do regulador do mercado correspondente.

Este projeto é informativo e não constitui recomendação de investimento.
