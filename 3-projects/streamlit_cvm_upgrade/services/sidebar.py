"""Filtros globais e busca de ativos do dashboard."""

from __future__ import annotations

from dataclasses import dataclass

import requests
import streamlit as st


PERIODS = {
    "1 mês": "1mo",
    "3 meses": "3mo",
    "6 meses": "6mo",
    "1 ano": "1y",
    "2 anos": "2y",
    "5 anos": "5y",
    "Máximo": "max",
}

BENCHMARKS = {
    "Ibovespa": "^BVSP",
    "S&P 500": "^GSPC",
    "Nasdaq 100": "^NDX",
    "Dólar/real": "BRL=X",
    "Sem benchmark": None,
}

DEFAULT_PEERS = {
    "Brasil / B3": ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "WEGE3.SA", "BBAS3.SA"],
    "BDR": ["AAPL34.SA", "MSFT34.SA", "GOGL34.SA", "NVDC34.SA", "AMZO34.SA"],
    "Internacional": ["AAPL", "MSFT", "GOOGL", "NVDA", "AMZN"],
}


@dataclass(frozen=True)
class DashboardFilters:
    ticker: str
    period: str
    period_label: str
    benchmark: str | None
    benchmark_label: str
    market: str
    risk_free_rate: float


def normalize_ticker(query: str, market: str) -> str:
    """Normaliza tickers brasileiros sem alterar símbolos internacionais."""
    value = (query or "").strip().upper()
    if not value:
        return "PETR4.SA" if market == "Brasil / B3" else "AAPL"
    if (
        market in {"Brasil / B3", "BDR"}
        and any(character.isdigit() for character in value)
        and not value.endswith(".SA")
    ):
        return f"{value}.SA"
    return value


@st.cache_data(ttl="1h", max_entries=128, show_spinner=False)
def search_yahoo_assets(query: str) -> dict[str, str]:
    """Pesquisa ações e devolve rótulos legíveis associados aos tickers."""
    response = requests.get(
        "https://query2.finance.yahoo.com/v1/finance/search",
        params={"q": query, "quotesCount": 20, "newsCount": 0},
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10,
    )
    response.raise_for_status()

    assets: dict[str, str] = {}
    for item in response.json().get("quotes", []):
        symbol = item.get("symbol")
        if not symbol or item.get("quoteType") not in {"EQUITY", "ETF"}:
            continue
        name = item.get("shortname") or item.get("longname") or symbol
        exchange = item.get("exchange") or item.get("exchDisp") or "Mercado"
        assets[f"{name} · {symbol} · {exchange}"] = symbol
    return assets


def _update_search_results(market: str, search_term: str) -> None:
    direct_ticker = normalize_ticker(search_term, market)
    try:
        assets = search_yahoo_assets(direct_ticker)
    except (requests.RequestException, ValueError):
        assets = {}

    direct_label = f"Usar ticker diretamente · {direct_ticker}"
    st.session_state.asset_results = {direct_label: direct_ticker, **assets}
    st.session_state.asset_market = market


def render_sidebar() -> DashboardFilters:
    """Renderiza busca e filtros globais sem consultar a API a cada tecla digitada."""
    with st.sidebar:
        st.title(":material/query_stats: Fintech")
        st.caption("Inteligência de mercado e análise de ações")

        with st.form("asset_search", border=False):
            market = st.selectbox(
                "Mercado",
                options=list(DEFAULT_PEERS),
                index=0,
            )
            default_query = {
                "Brasil / B3": "PETR4",
                "BDR": "AAPL34",
                "Internacional": "AAPL",
            }[market]
            search_term = st.text_input(
                "Empresa ou ticker",
                value=default_query,
                placeholder="Ex.: PETR4, Vale ou AAPL",
            )
            submitted = st.form_submit_button(
                "Buscar ativo",
                icon=":material/search:",
                type="primary",
                width="stretch",
            )

        if submitted or "asset_results" not in st.session_state:
            _update_search_results(market, search_term)

        assets = st.session_state.get("asset_results", {})
        if not assets:
            _update_search_results(market, search_term)
            assets = st.session_state.asset_results

        selected_asset = st.selectbox(
            "Ativo selecionado",
            options=list(assets),
            help="A primeira opção sempre permite usar o ticker digitado diretamente.",
        )
        ticker = assets[selected_asset]

        period_label = st.pills(
            "Janela de análise",
            options=list(PERIODS),
            default="1 ano",
        ) or "1 ano"

        benchmark_label = st.selectbox(
            "Benchmark",
            options=list(BENCHMARKS),
            index=0,
        )

        advanced = st.expander(
            "Premissas de risco",
            icon=":material/tune:",
        )
        with advanced:
            risk_free_rate = st.number_input(
                "Taxa livre de risco anual (%)",
                min_value=0.0,
                max_value=40.0,
                value=10.0,
                step=0.25,
                help="Usada somente no cálculo do índice de Sharpe.",
            )

        st.caption(f"Ticker em uso: `{ticker}`")
        st.caption("Dados de mercado: Yahoo Finance")

    return DashboardFilters(
        ticker=ticker,
        period=PERIODS[period_label],
        period_label=period_label,
        benchmark=BENCHMARKS[benchmark_label],
        benchmark_label=benchmark_label,
        market=st.session_state.get("asset_market", market),
        risk_free_rate=risk_free_rate / 100,
    )
