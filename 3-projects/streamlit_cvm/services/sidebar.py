import streamlit as st


def render_sidebar():

    st.sidebar.title("Filtros")

    stocks = {
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Google": "GOOGL",
        "Amazon": "AMZN",
        "Tesla": "TSLA",
        "NVIDIA": "NVDA",
        "Meta": "META",
        "Netflix": "NFLX",
        "Petrobras": "PETR4.SA",
        "Vale": "VALE3.SA",
        "Itaú": "ITUB4.SA",
        "Banco do Brasil": "BBAS3.SA",
        "Nubank": "NU",
        "Porto Seguro": "PSSA3.SA"
    }

    stock_name = st.sidebar.selectbox(
        "Selecione a ação",
        options=list(stocks.keys())
    )

    ticker = stocks[stock_name]

    period_options = {
        "1 Mês": "1mo",
        "6 Meses": "6mo",
        "1 Ano": "1y"
    }

    selected_period = st.sidebar.selectbox(
        "Período",
        list(period_options.keys())
    )

    period = period_options[selected_period]

    return ticker, period