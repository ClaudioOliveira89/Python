"""Gráficos Plotly padronizados para o dashboard financeiro."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from services.indicators import add_technical_indicators, normalize_prices


BLUE = "#0B66C3"
LIGHT_BLUE = "#72B7FF"
NAVY = "#0B1F3A"
GREEN = "#138A5B"
RED = "#D64545"
GOLD = "#C88A00"
VIOLET = "#6D5BD0"
GRID = "rgba(100, 116, 139, 0.16)"


def _base_layout(fig: go.Figure, height: int, hovermode: str = "x unified") -> go.Figure:
    fig.update_layout(
        template="streamlit",
        height=height,
        margin=dict(l=20, r=20, t=35, b=20),
        hovermode=hovermode,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.update_xaxes(showgrid=False, rangeslider_visible=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig


def price_chart(
    history: pd.DataFrame,
    ticker: str,
    chart_type: str = "Linha",
    overlays: tuple[str, ...] = (),
) -> go.Figure:
    """Constrói preço/candlestick, médias e volume em painéis sincronizados."""
    data = add_technical_indicators(history)
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.76, 0.24],
    )

    if chart_type == "Candles" and {"Open", "High", "Low", "Close"}.issubset(data.columns):
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=ticker,
                increasing_line_color=GREEN,
                decreasing_line_color=RED,
            ),
            row=1,
            col=1,
        )
    else:
        fig.add_trace(
            go.Scatter(
                x=data.index,
                y=data["Close"],
                name=ticker,
                mode="lines",
                line=dict(color=BLUE, width=2.4),
            ),
            row=1,
            col=1,
        )

    overlay_colors = {"MM20": LIGHT_BLUE, "MM50": GOLD, "MM200": VIOLET}
    for overlay in overlays:
        if overlay in data.columns:
            fig.add_trace(
                go.Scatter(
                    x=data.index,
                    y=data[overlay],
                    name=overlay,
                    mode="lines",
                    line=dict(color=overlay_colors.get(overlay, NAVY), width=1.4),
                ),
                row=1,
                col=1,
            )

    if "Volume" in data.columns:
        if "Open" in data.columns:
            volume_colors = [
                GREEN if close >= open_ else RED
                for close, open_ in zip(data["Close"], data["Open"])
            ]
        else:
            volume_colors = BLUE
        fig.add_trace(
            go.Bar(
                x=data.index,
                y=data["Volume"],
                name="Volume",
                marker_color=volume_colors,
                opacity=0.6,
            ),
            row=2,
            col=1,
        )

    fig.update_yaxes(title_text="Preço", row=1, col=1)
    fig.update_yaxes(title_text="Volume", row=2, col=1)
    return _base_layout(fig, height=570)


def technical_chart(history: pd.DataFrame, ticker: str) -> go.Figure:
    """Constrói painel técnico com Bollinger, RSI e MACD."""
    data = add_technical_indicators(history)
    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.055,
        row_heights=[0.52, 0.22, 0.26],
    )

    fig.add_trace(
        go.Scatter(x=data.index, y=data["Close"], name=ticker, line=dict(color=BLUE, width=2.2)),
        row=1,
        col=1,
    )
    for name, color in (("MM20", LIGHT_BLUE), ("MM50", GOLD), ("MM200", VIOLET)):
        fig.add_trace(
            go.Scatter(x=data.index, y=data[name], name=name, line=dict(color=color, width=1.2)),
            row=1,
            col=1,
        )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Banda superior"],
            name="Bollinger",
            line=dict(color="rgba(114,183,255,0.45)", width=1),
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Banda inferior"],
            name="Bollinger inferior",
            line=dict(color="rgba(114,183,255,0.45)", width=1),
            fill="tonexty",
            fillcolor="rgba(114,183,255,0.08)",
            showlegend=False,
        ),
        row=1,
        col=1,
    )

    fig.add_trace(
        go.Scatter(x=data.index, y=data["RSI"], name="RSI (14)", line=dict(color=VIOLET, width=1.8)),
        row=2,
        col=1,
    )
    fig.add_hline(y=70, line_dash="dot", line_color=RED, row=2, col=1)
    fig.add_hline(y=30, line_dash="dot", line_color=GREEN, row=2, col=1)

    histogram_colors = [GREEN if value >= 0 else RED for value in data["Histograma MACD"].fillna(0)]
    fig.add_trace(
        go.Bar(
            x=data.index,
            y=data["Histograma MACD"],
            name="Histograma",
            marker_color=histogram_colors,
            opacity=0.55,
        ),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(x=data.index, y=data["MACD"], name="MACD", line=dict(color=BLUE, width=1.5)),
        row=3,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Sinal MACD"],
            name="Sinal",
            line=dict(color=GOLD, width=1.3),
        ),
        row=3,
        col=1,
    )

    fig.update_yaxes(title_text="Preço", row=1, col=1)
    fig.update_yaxes(title_text="RSI", range=[0, 100], row=2, col=1)
    fig.update_yaxes(title_text="MACD", row=3, col=1)
    return _base_layout(fig, height=760)


def normalized_performance_chart(prices: pd.DataFrame, base: float = 100.0) -> go.Figure:
    """Compara séries rebaseadas, evitando a distorção de moedas e preços absolutos."""
    normalized = normalize_prices(prices, base=base)
    fig = go.Figure()
    palette = [BLUE, GREEN, VIOLET, GOLD, RED, LIGHT_BLUE, NAVY]
    for index, column in enumerate(normalized.columns):
        fig.add_trace(
            go.Scatter(
                x=normalized.index,
                y=normalized[column],
                name=str(column),
                mode="lines",
                line=dict(color=palette[index % len(palette)], width=2.2),
            )
        )
    fig.add_hline(y=base, line_dash="dot", line_color="rgba(100,116,139,0.55)")
    fig.update_yaxes(title_text=f"Base {base:.0f}")
    return _base_layout(fig, height=460)


def drawdown_chart(history: pd.DataFrame) -> go.Figure:
    """Mostra perdas desde o último pico da série."""
    data = add_technical_indicators(history)
    fig = go.Figure(
        go.Scatter(
            x=data.index,
            y=data["Drawdown"] * 100,
            name="Drawdown",
            mode="lines",
            line=dict(color=RED, width=1.8),
            fill="tozeroy",
            fillcolor="rgba(214,69,69,0.15)",
        )
    )
    fig.update_yaxes(title_text="Drawdown (%)", ticksuffix="%")
    return _base_layout(fig, height=340)


def financial_history_chart(statement: pd.DataFrame, currency: str) -> go.Figure | None:
    """Plota receita, EBITDA e lucro líquido anuais quando existirem."""
    preferred = ["Total Revenue", "EBITDA", "Net Income"]
    available = [row for row in preferred if row in statement.index]
    if not available:
        return None

    labels = {
        "Total Revenue": "Receita",
        "EBITDA": "EBITDA",
        "Net Income": "Lucro líquido",
    }
    fig = go.Figure()
    colors = {"Total Revenue": BLUE, "EBITDA": LIGHT_BLUE, "Net Income": GREEN}
    ordered = statement.loc[available].sort_index(axis=1)
    for row in available:
        fig.add_trace(
            go.Bar(
                x=[date.year for date in ordered.columns],
                y=ordered.loc[row] / 1_000_000,
                name=labels[row],
                marker_color=colors[row],
            )
        )
    fig.update_layout(barmode="group")
    fig.update_yaxes(title_text=f"{currency} milhões")
    return _base_layout(fig, height=430, hovermode="x")


def dividends_chart(dividends: pd.Series, currency: str) -> go.Figure:
    """Agrega proventos por ano para reduzir ruído visual."""
    annual = dividends.groupby(dividends.index.year).sum()
    fig = go.Figure(
        go.Bar(
            x=annual.index.astype(str),
            y=annual.values,
            name="Proventos",
            marker_color=BLUE,
            text=[f"{value:.2f}" for value in annual.values],
            textposition="outside",
        )
    )
    fig.update_yaxes(title_text=f"{currency} por ação")
    return _base_layout(fig, height=340, hovermode="x")
