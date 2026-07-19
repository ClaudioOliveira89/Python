"""Camada de acesso aos dados de mercado fornecidos pelo Yahoo Finance."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd
import streamlit as st
import yfinance as yf


class MarketDataError(RuntimeError):
    """Erro amigável para falhas na fonte de dados de mercado."""


def _clean_ticker(ticker: str) -> str:
    value = (ticker or "").strip().upper()
    if not value:
        raise MarketDataError("Informe um ticker válido para continuar.")
    return value


@st.cache_data(ttl="15m", max_entries=128, show_spinner=False)
def get_stock_data(ticker: str, period: str = "1y") -> pd.DataFrame:
    """Retorna OHLCV e eventos do ativo, com índice ordenado e sem duplicatas."""
    ticker = _clean_ticker(ticker)
    try:
        data = yf.Ticker(ticker).history(
            period=period,
            interval="1d",
            auto_adjust=False,
            actions=True,
        )
    except Exception as exc:
        raise MarketDataError(f"Não foi possível carregar as cotações de {ticker}.") from exc

    if data is None or data.empty:
        raise MarketDataError(f"Nenhuma cotação foi encontrada para {ticker}.")

    data = data.copy()
    data.index = pd.to_datetime(data.index)
    data = data[~data.index.duplicated(keep="last")].sort_index()
    return data


@st.cache_data(ttl="2h", max_entries=128, show_spinner=False)
def get_company_info(ticker: str) -> dict:
    """Carrega cadastro, múltiplos e indicadores fundamentalistas do ativo."""
    ticker = _clean_ticker(ticker)
    stock = yf.Ticker(ticker)

    try:
        info = stock.get_info() or {}
    except Exception:
        info = {}

    if not info:
        try:
            info = dict(stock.fast_info)
        except Exception:
            info = {}

    info.setdefault("symbol", ticker)
    return info


@st.cache_data(ttl="6h", max_entries=64, show_spinner=False)
def get_financial_statements(ticker: str) -> dict[str, pd.DataFrame]:
    """Retorna DRE, balanço e fluxo de caixa anuais quando disponíveis."""
    ticker = _clean_ticker(ticker)
    stock = yf.Ticker(ticker)
    statements: dict[str, pd.DataFrame] = {}

    sources = {
        "Resultado": "income_stmt",
        "Balanço": "balance_sheet",
        "Fluxo de caixa": "cashflow",
    }
    for label, attribute in sources.items():
        try:
            frame = getattr(stock, attribute)
            if frame is not None and not frame.empty:
                frame = frame.copy()
                frame.columns = pd.to_datetime(frame.columns)
                statements[label] = frame.sort_index(axis=1)
        except Exception:
            continue

    return statements


@st.cache_data(ttl="2h", max_entries=128, show_spinner=False)
def get_dividends(ticker: str) -> pd.Series:
    """Retorna o histórico completo de proventos disponibilizado pela fonte."""
    ticker = _clean_ticker(ticker)
    try:
        dividends = yf.Ticker(ticker).dividends
    except Exception:
        return pd.Series(dtype="float64", name="Dividendo")

    if dividends is None or dividends.empty:
        return pd.Series(dtype="float64", name="Dividendo")

    dividends = dividends.copy()
    dividends.index = pd.to_datetime(dividends.index)
    dividends.name = "Dividendo"
    return dividends.sort_index()


@st.cache_data(ttl="30m", max_entries=64, show_spinner=False)
def get_peer_prices(tickers: tuple[str, ...], period: str = "1y") -> pd.DataFrame:
    """Carrega preços de fechamento de vários ativos para comparação relativa."""
    clean = tuple(dict.fromkeys(_clean_ticker(ticker) for ticker in tickers))
    if not clean:
        return pd.DataFrame()

    try:
        downloaded = yf.download(
            list(clean),
            period=period,
            interval="1d",
            auto_adjust=False,
            progress=False,
            group_by="column",
            threads=True,
        )
    except Exception as exc:
        raise MarketDataError("Não foi possível carregar os ativos de comparação.") from exc

    if downloaded is None or downloaded.empty:
        raise MarketDataError("A fonte não retornou dados para a comparação.")

    if isinstance(downloaded.columns, pd.MultiIndex):
        try:
            close = downloaded["Close"].copy()
        except KeyError as exc:
            raise MarketDataError("Os preços de fechamento não vieram na resposta.") from exc
    else:
        if "Close" not in downloaded:
            raise MarketDataError("Os preços de fechamento não vieram na resposta.")
        close = downloaded[["Close"]].rename(columns={"Close": clean[0]})

    if isinstance(close, pd.Series):
        close = close.to_frame(name=clean[0])

    close.index = pd.to_datetime(close.index)
    close = close.dropna(axis=1, how="all").sort_index()
    return close


def clear_market_caches() -> None:
    """Limpa apenas os caches desta camada para uma atualização manual."""
    for loader in (
        get_stock_data,
        get_company_info,
        get_financial_statements,
        get_dividends,
        get_peer_prices,
    ):
        loader.clear()


def available_statement_items(
    statement: pd.DataFrame,
    preferred: Iterable[str],
) -> list[str]:
    """Seleciona linhas financeiras relevantes sem assumir que todas existem."""
    return [item for item in preferred if item in statement.index]
