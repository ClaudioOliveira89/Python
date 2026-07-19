"""Cálculos técnicos, de risco e de comparação entre ativos."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


TRADING_DAYS = 252


def add_technical_indicators(history: pd.DataFrame) -> pd.DataFrame:
    """Adiciona médias, bandas, RSI, MACD, retornos e drawdown ao OHLCV."""
    data = history.copy()
    close = pd.to_numeric(data["Close"], errors="coerce")

    for window in (20, 50, 200):
        data[f"MM{window}"] = close.rolling(window, min_periods=window).mean()

    rolling_std = close.rolling(20, min_periods=20).std()
    data["Banda superior"] = data["MM20"] + 2 * rolling_std
    data["Banda inferior"] = data["MM20"] - 2 * rolling_std

    delta = close.diff()
    gains = delta.clip(lower=0).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    losses = (-delta.clip(upper=0)).ewm(alpha=1 / 14, adjust=False, min_periods=14).mean()
    relative_strength = gains / losses.replace(0, np.nan)
    data["RSI"] = 100 - (100 / (1 + relative_strength))

    ema_12 = close.ewm(span=12, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    data["MACD"] = ema_12 - ema_26
    data["Sinal MACD"] = data["MACD"].ewm(span=9, adjust=False).mean()
    data["Histograma MACD"] = data["MACD"] - data["Sinal MACD"]

    data["Retorno diário"] = close.pct_change(fill_method=None)
    data["Retorno acumulado"] = (1 + data["Retorno diário"].fillna(0)).cumprod() - 1
    data["Drawdown"] = close / close.cummax() - 1
    return data


def calculate_risk_metrics(
    history: pd.DataFrame,
    annual_risk_free_rate: float = 0.0,
) -> dict[str, float | None]:
    """Calcula retorno, volatilidade, Sharpe, VaR e drawdown máximo."""
    close = pd.to_numeric(history["Close"], errors="coerce").dropna()
    returns = close.pct_change(fill_method=None).dropna()
    if len(close) < 2 or returns.empty:
        return {
            "total_return": None,
            "annual_return": None,
            "volatility": None,
            "sharpe": None,
            "max_drawdown": None,
            "var_95": None,
        }

    total_return = close.iloc[-1] / close.iloc[0] - 1
    years = max(len(returns) / TRADING_DAYS, 1 / TRADING_DAYS)
    annual_return = (1 + total_return) ** (1 / years) - 1 if total_return > -1 else -1.0
    volatility = returns.std(ddof=1) * math.sqrt(TRADING_DAYS)
    sharpe = (
        (annual_return - annual_risk_free_rate) / volatility
        if volatility and math.isfinite(volatility)
        else None
    )
    drawdown = close / close.cummax() - 1

    return {
        "total_return": float(total_return),
        "annual_return": float(annual_return),
        "volatility": float(volatility),
        "sharpe": float(sharpe) if sharpe is not None else None,
        "max_drawdown": float(drawdown.min()),
        "var_95": float(returns.quantile(0.05)),
    }


def calculate_relative_metrics(
    asset_history: pd.DataFrame,
    benchmark_history: pd.DataFrame,
) -> dict[str, float | None]:
    """Calcula correlação, beta e alfa anualizados contra um benchmark."""
    joined = pd.concat(
        [
            asset_history["Close"].rename("Ativo"),
            benchmark_history["Close"].rename("Benchmark"),
        ],
        axis=1,
        join="inner",
    ).dropna()
    returns = joined.pct_change(fill_method=None).dropna()
    if len(returns) < 3:
        return {"correlation": None, "beta": None, "alpha": None}

    benchmark_variance = returns["Benchmark"].var(ddof=1)
    beta = (
        returns["Ativo"].cov(returns["Benchmark"]) / benchmark_variance
        if benchmark_variance
        else None
    )
    asset_annual = returns["Ativo"].mean() * TRADING_DAYS
    benchmark_annual = returns["Benchmark"].mean() * TRADING_DAYS
    alpha = asset_annual - (beta * benchmark_annual) if beta is not None else None

    return {
        "correlation": float(returns["Ativo"].corr(returns["Benchmark"])),
        "beta": float(beta) if beta is not None else None,
        "alpha": float(alpha) if alpha is not None else None,
    }


def normalize_prices(prices: pd.DataFrame, base: float = 100.0) -> pd.DataFrame:
    """Rebaseia cada série para uma base comum usando o primeiro valor válido."""
    clean = prices.sort_index().copy()
    normalized = pd.DataFrame(index=clean.index)
    for column in clean.columns:
        series = clean[column].dropna()
        if not series.empty and series.iloc[0] != 0:
            normalized[column] = clean[column] / series.iloc[0] * base
    return normalized.dropna(how="all")


def peer_summary(prices: pd.DataFrame) -> pd.DataFrame:
    """Resume desempenho e risco de cada ativo em uma tabela comparável."""
    rows: list[dict] = []
    for ticker in prices.columns:
        history = pd.DataFrame({"Close": prices[ticker]}).dropna()
        metrics = calculate_risk_metrics(history)
        rows.append(
            {
                "Ativo": ticker,
                "Retorno": metrics["total_return"],
                "Retorno anualizado": metrics["annual_return"],
                "Volatilidade": metrics["volatility"],
                "Drawdown máximo": metrics["max_drawdown"],
            }
        )
    return pd.DataFrame(rows).sort_values("Retorno", ascending=False, na_position="last")
