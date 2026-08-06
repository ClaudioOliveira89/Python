import streamlit as st
import requests


def normalize_brazilian_ticker(query):
    query = query.strip().upper()

    if query.endswith(".SA"):
        return query

    if len(query) >= 5 and any(char.isdigit() for char in query):
        return f"{query}.SA"

    return query


@st.cache_data(ttl=3600)
def search_yahoo_assets(query):
    url = "https://query2.finance.yahoo.com/v1/finance/search"

    params = {
        "q": query,
        "quotesCount": 20,
        "newsCount": 0
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        params=params,
        headers=headers,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    quotes = data.get("quotes", [])

    assets = {}

    for item in quotes:
        symbol = item.get("symbol")
        name = item.get("shortname") or item.get("longname") or symbol
        exchange = item.get("exchange", "")
        quote_type = item.get("quoteType", "")

        if not symbol:
            continue

        if quote_type != "EQUITY":
            continue

        label = f"{name} | {symbol} | {exchange}"

        assets[label] = symbol

    return assets


def render_sidebar():

    st.sidebar.title("Filtros")

    market_type = st.sidebar.selectbox(
        "Tipo de busca",
        options=[
            "Brasil / B3",
            "BDR",
            "Internacional Direta"
        ]
    )

    search_term = st.sidebar.text_input(
        "Digite o nome ou ticker",
        value="PETR4" if market_type == "Brasil / B3" else "AAPL"
    )

    if market_type in ["Brasil / B3", "BDR"]:
        search_query = normalize_brazilian_ticker(search_term)
    else:
        search_query = search_term.strip().upper()

    assets = search_yahoo_assets(search_query)

    if not assets:
        st.sidebar.warning("Nenhum ativo encontrado.")
        return None, None

    asset_name = st.sidebar.selectbox(
        "Selecione o ativo correto",
        options=list(assets.keys())
    )

    ticker = assets[asset_name]

    period_options = {
        "1 Mês": "1mo",
        "6 Meses": "6mo",
        "1 Ano": "1y"
    }

    selected_period = st.sidebar.selectbox(
        "Período",
        options=list(period_options.keys())
    )

    period = period_options[selected_period]

    st.sidebar.caption(f"Ticker usado: {ticker}")

    return ticker, period