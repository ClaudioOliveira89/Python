"""Formatação e apresentação dos principais indicadores financeiros."""

from __future__ import annotations

import math
from typing import Any

import pandas as pd
import streamlit as st


CURRENCY_SYMBOLS = {
    "BRL": "R$",
    "USD": "US$",
    "EUR": "€",
    "GBP": "£",
}


def safe_float(value: Any) -> float | None:
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    return number if math.isfinite(number) else None


def format_number(value: Any, decimals: int = 2, suffix: str = "") -> str:
    number = safe_float(value)
    if number is None:
        return "—"
    formatted = f"{number:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"{formatted}{suffix}"


def format_compact(value: Any) -> str:
    number = safe_float(value)
    if number is None:
        return "—"

    absolute = abs(number)
    for divisor, suffix in (
        (1_000_000_000_000, " tri"),
        (1_000_000_000, " bi"),
        (1_000_000, " mi"),
        (1_000, " mil"),
    ):
        if absolute >= divisor:
            return f"{format_number(number / divisor, 2)}{suffix}"
    return format_number(number, 0)


def format_currency(value: Any, currency: str = "BRL", compact: bool = False) -> str:
    symbol = CURRENCY_SYMBOLS.get(currency, currency or "")
    body = format_compact(value) if compact else format_number(value, 2)
    return "—" if body == "—" else f"{symbol} {body}".strip()


def normalize_fraction(value: Any) -> float | None:
    """Normaliza percentuais que algumas fontes entregam como 4,2 ou 0,042."""
    number = safe_float(value)
    if number is None:
        return None
    return number / 100 if abs(number) > 1 else number


def format_percent(value: Any, normalize: bool = False) -> str:
    number = normalize_fraction(value) if normalize else safe_float(value)
    return "—" if number is None else format_number(number * 100, 2, "%")


def format_multiple(value: Any) -> str:
    number = safe_float(value)
    return "—" if number is None else format_number(number, 2, "x")


def _last_prices(history: pd.DataFrame) -> tuple[pd.Series, float, float, float]:
    close = history["Close"].dropna().astype(float)
    if len(close) < 2:
        raise ValueError("São necessárias pelo menos duas cotações para calcular a variação.")
    current = float(close.iloc[-1])
    previous = float(close.iloc[-2])
    change = (current / previous - 1) if previous else 0.0
    return close, current, previous, change


def render_primary_metrics(history: pd.DataFrame, info: dict) -> None:
    """Exibe os KPIs executivos com componentes nativos e sparklines."""
    close, current, _, change = _last_prices(history)
    currency = info.get("currency") or "BRL"
    market_cap = info.get("marketCap")
    trailing_pe = info.get("trailingPE")
    dividend_yield = info.get("dividendYield")

    with st.container(horizontal=True):
        st.metric(
            "Cotação",
            format_currency(current, currency),
            f"{change:+.2%} no dia",
            border=True,
            chart_data=close.tail(30).tolist(),
            chart_type="line",
        )
        st.metric(
            "Valor de mercado",
            format_currency(market_cap, currency, compact=True),
            border=True,
        )
        st.metric(
            "P/L",
            format_multiple(trailing_pe),
            border=True,
        )
        st.metric(
            "Dividend yield",
            format_percent(dividend_yield, normalize=True),
            border=True,
        )


def render_market_metrics(history: pd.DataFrame, info: dict) -> None:
    """Exibe estatísticas de negociação e posicionamento em 52 semanas."""
    close, current, _, _ = _last_prices(history)
    currency = info.get("currency") or "BRL"
    high_52 = safe_float(info.get("fiftyTwoWeekHigh"))
    low_52 = safe_float(info.get("fiftyTwoWeekLow"))
    volume = info.get("regularMarketVolume")
    average_volume = info.get("averageVolume")

    position = None
    if high_52 is not None and low_52 is not None and high_52 > low_52:
        position = (current - low_52) / (high_52 - low_52)

    period_high = float(close.max())
    period_low = float(close.min())

    with st.container(horizontal=True):
        st.metric(
            "Máxima da janela",
            format_currency(period_high, currency),
            border=True,
        )
        st.metric(
            "Mínima da janela",
            format_currency(period_low, currency),
            border=True,
        )
        st.metric(
            "Posição em 52 semanas",
            format_percent(position),
            border=True,
        )
        st.metric(
            "Volume / média",
            f"{format_compact(volume)} / {format_compact(average_volume)}",
            border=True,
        )


def fundamentals_table(info: dict) -> pd.DataFrame:
    """Cria uma matriz categorizada de fundamentos para exploração."""
    rows = [
        ("Valuation", "P/L", format_multiple(info.get("trailingPE"))),
        ("Valuation", "P/L projetado", format_multiple(info.get("forwardPE"))),
        ("Valuation", "P/VP", format_multiple(info.get("priceToBook"))),
        ("Valuation", "EV/EBITDA", format_multiple(info.get("enterpriseToEbitda"))),
        ("Valuation", "Preço/vendas", format_multiple(info.get("priceToSalesTrailing12Months"))),
        ("Rentabilidade", "ROE", format_percent(info.get("returnOnEquity"))),
        ("Rentabilidade", "ROA", format_percent(info.get("returnOnAssets"))),
        ("Rentabilidade", "Margem bruta", format_percent(info.get("grossMargins"))),
        ("Rentabilidade", "Margem operacional", format_percent(info.get("operatingMargins"))),
        ("Rentabilidade", "Margem líquida", format_percent(info.get("profitMargins"))),
        ("Crescimento", "Receita", format_percent(info.get("revenueGrowth"))),
        ("Crescimento", "Lucro", format_percent(info.get("earningsGrowth"))),
        ("Solidez", "Dívida/patrimônio", format_percent(info.get("debtToEquity"), normalize=True)),
        ("Solidez", "Liquidez corrente", format_multiple(info.get("currentRatio"))),
        ("Solidez", "Caixa total", format_compact(info.get("totalCash"))),
        ("Solidez", "Dívida total", format_compact(info.get("totalDebt"))),
        ("Mercado", "Beta", format_number(info.get("beta"), 2)),
        ("Proventos", "Dividend yield", format_percent(info.get("dividendYield"), normalize=True)),
        ("Proventos", "Payout", format_percent(info.get("payoutRatio"))),
    ]
    return pd.DataFrame(rows, columns=["Categoria", "Indicador", "Valor"])


def render_fundamental_cards(info: dict) -> None:
    """Destaca os fundamentos mais úteis antes da tabela detalhada."""
    groups = [
        (
            "Valuation",
            [
                ("P/L", format_multiple(info.get("trailingPE"))),
                ("P/VP", format_multiple(info.get("priceToBook"))),
                ("EV/EBITDA", format_multiple(info.get("enterpriseToEbitda"))),
            ],
        ),
        (
            "Rentabilidade",
            [
                ("ROE", format_percent(info.get("returnOnEquity"))),
                ("Margem líquida", format_percent(info.get("profitMargins"))),
                ("Margem operacional", format_percent(info.get("operatingMargins"))),
            ],
        ),
        (
            "Solidez e dividendos",
            [
                ("Dívida/patrimônio", format_percent(info.get("debtToEquity"), normalize=True)),
                ("Liquidez corrente", format_multiple(info.get("currentRatio"))),
                ("Dividend yield", format_percent(info.get("dividendYield"), normalize=True)),
            ],
        ),
    ]

    columns = st.columns(3)
    for column, (title, values) in zip(columns, groups):
        with column.container(border=True, height="stretch"):
            st.subheader(title)
            for label, value in values:
                st.metric(label, value)
