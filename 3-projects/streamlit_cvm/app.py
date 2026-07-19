"""Dashboard financeiro para análise de ações brasileiras e internacionais."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from services.charts import (
    dividends_chart,
    drawdown_chart,
    financial_history_chart,
    normalized_performance_chart,
    price_chart,
    technical_chart,
)
from services.indicators import (
    add_technical_indicators,
    calculate_relative_metrics,
    calculate_risk_metrics,
    peer_summary,
)
from services.metrics import (
    format_compact,
    format_currency,
    format_number,
    format_percent,
    fundamentals_table,
    render_fundamental_cards,
    render_market_metrics,
    render_primary_metrics,
    safe_float,
)
from services.sidebar import DEFAULT_PEERS, DashboardFilters, render_sidebar
from services.yahoo_service import (
    MarketDataError,
    clear_market_caches,
    get_company_info,
    get_dividends,
    get_financial_statements,
    get_peer_prices,
    get_stock_data,
)


st.set_page_config(
    page_title="Fintech · Análise de ações",
    page_icon=":material/query_stats:",
    layout="wide",
    initial_sidebar_state="expanded",
)


PLOTLY_CONFIG = {
    "displaylogo": False,
    "responsive": True,
    "modeBarButtonsToRemove": ["lasso2d", "select2d"],
}

STATEMENT_LABELS = {
    "Total Revenue": "Receita total",
    "Gross Profit": "Lucro bruto",
    "Operating Income": "Resultado operacional",
    "EBIT": "EBIT",
    "EBITDA": "EBITDA",
    "Net Income": "Lucro líquido",
    "Total Assets": "Ativos totais",
    "Current Assets": "Ativos circulantes",
    "Cash Cash Equivalents And Short Term Investments": "Caixa e equivalentes",
    "Total Debt": "Dívida total",
    "Stockholders Equity": "Patrimônio líquido",
    "Operating Cash Flow": "Fluxo de caixa operacional",
    "Free Cash Flow": "Fluxo de caixa livre",
    "Capital Expenditure": "Investimentos (Capex)",
    "Repurchase Of Capital Stock": "Recompra de ações",
    "Cash Dividends Paid": "Dividendos pagos",
}

STATEMENT_PRIORITY = {
    "Resultado": [
        "Total Revenue",
        "Gross Profit",
        "Operating Income",
        "EBIT",
        "EBITDA",
        "Net Income",
    ],
    "Balanço": [
        "Total Assets",
        "Current Assets",
        "Cash Cash Equivalents And Short Term Investments",
        "Total Debt",
        "Stockholders Equity",
    ],
    "Fluxo de caixa": [
        "Operating Cash Flow",
        "Free Cash Flow",
        "Capital Expenditure",
        "Repurchase Of Capital Stock",
        "Cash Dividends Paid",
    ],
}


def plot(fig) -> None:
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CONFIG)


def _company_name(info: dict, ticker: str) -> str:
    return info.get("longName") or info.get("shortName") or ticker


def _updated_label(history: pd.DataFrame) -> str:
    last_date = pd.Timestamp(history.index.max())
    return last_date.strftime("%d/%m/%Y")


def _safe_position(current: float, low: float | None, high: float | None) -> float | None:
    if low is None or high is None or high <= low:
        return None
    return max(0.0, min(1.0, (current - low) / (high - low)))


def render_company_header(ticker: str, info: dict, history: pd.DataFrame) -> None:
    name = _company_name(info, ticker)
    sector = info.get("sector") or "Setor não informado"
    exchange = info.get("fullExchangeName") or info.get("exchange") or "Mercado"
    currency = info.get("currency") or "BRL"

    title_col, action_col = st.columns([5, 1], vertical_alignment="center")
    with title_col:
        st.title(f":material/monitoring: {name}")
        with st.container(horizontal=True):
            st.badge(ticker, color="blue")
            st.badge(sector, color="gray")
            st.badge(exchange, color="gray")
        st.caption(
            f"Moeda: {currency} · última cotação disponível: {_updated_label(history)} · "
            "dados com possível atraso"
        )
    with action_col:
        if st.button(
            "Atualizar",
            icon=":material/refresh:",
            width="stretch",
            help="Limpa o cache local e solicita novamente os dados à fonte.",
        ):
            clear_market_caches()
            st.rerun()


def render_risk_kpis(history: pd.DataFrame, risk_free_rate: float) -> None:
    metrics = calculate_risk_metrics(history, risk_free_rate)
    with st.container(horizontal=True):
        st.metric("Retorno da janela", format_percent(metrics["total_return"]), border=True)
        st.metric("Retorno anualizado", format_percent(metrics["annual_return"]), border=True)
        st.metric("Volatilidade anual", format_percent(metrics["volatility"]), border=True)
        st.metric("Sharpe", format_number(metrics["sharpe"], 2), border=True)
        st.metric("Drawdown máximo", format_percent(metrics["max_drawdown"]), border=True)


def render_overview(
    filters: DashboardFilters,
    history: pd.DataFrame,
    info: dict,
) -> None:
    st.subheader("Visão executiva")
    render_market_metrics(history, info)

    chart_col, snapshot_col = st.columns([2.25, 1])
    with chart_col.container(border=True, height="stretch"):
        controls = st.columns([1, 2], vertical_alignment="bottom")
        with controls[0]:
            chart_type = st.segmented_control(
                "Visualização",
                options=["Linha", "Candles"],
                default="Linha",
            ) or "Linha"
        with controls[1]:
            overlays = st.pills(
                "Médias móveis",
                options=["MM20", "MM50", "MM200"],
                default=["MM20", "MM50"],
                selection_mode="multi",
            ) or []
        plot(price_chart(history, filters.ticker, chart_type, tuple(overlays)))

    close = history["Close"].dropna().astype(float)
    current = float(close.iloc[-1])
    low_52 = safe_float(info.get("fiftyTwoWeekLow"))
    high_52 = safe_float(info.get("fiftyTwoWeekHigh"))
    position = _safe_position(current, low_52, high_52)
    currency = info.get("currency") or "BRL"

    with snapshot_col.container(border=True, height="stretch"):
        st.subheader("Retrato de mercado")
        st.metric("Beta", format_number(info.get("beta"), 2))
        st.metric("Preço-alvo médio", format_currency(info.get("targetMeanPrice"), currency))
        st.metric("Volume médio", format_compact(info.get("averageVolume")))
        st.metric("Ações em circulação", format_compact(info.get("sharesOutstanding")))
        st.caption("Faixa de 52 semanas")
        if position is not None:
            st.progress(
                position,
                text=(
                    f"{format_currency(low_52, currency)}  →  "
                    f"{format_currency(high_52, currency)}"
                ),
            )
        else:
            st.caption("Faixa indisponível para este ativo.")

    st.subheader("Retorno e risco")
    render_risk_kpis(history, filters.risk_free_rate)

    dividends = get_dividends(filters.ticker)
    description = info.get("longBusinessSummary")
    detail_col, dividend_col = st.columns(2)

    with detail_col.container(border=True, height="stretch"):
        st.subheader("Sobre a empresa")
        if description:
            st.write(description)
        else:
            st.caption("Descrição corporativa não disponível na fonte.")
        website = info.get("website")
        if website:
            st.link_button("Site da companhia", website, icon=":material/open_in_new:")

    with dividend_col.container(border=True, height="stretch"):
        st.subheader("Histórico de proventos")
        if dividends.empty:
            st.caption("Não há proventos disponíveis para este ativo.")
        else:
            plot(dividends_chart(dividends.tail(80), currency))


def _statement_for_display(statement: pd.DataFrame, statement_name: str) -> pd.DataFrame:
    preferred = [row for row in STATEMENT_PRIORITY[statement_name] if row in statement.index]
    if not preferred:
        preferred = list(statement.index[:12])
    display = statement.loc[preferred].rename(index=STATEMENT_LABELS).T.sort_index(ascending=False)
    display.index = [pd.Timestamp(date).year for date in display.index]
    display.index.name = "Ano"
    return display / 1_000_000


def render_fundamentals(filters: DashboardFilters, info: dict) -> None:
    st.subheader("Fundamentos")
    st.caption("Múltiplos e margens usam os dados mais recentes disponibilizados pela fonte.")
    render_fundamental_cards(info)

    detail, context = st.columns([2, 1])
    with detail.container(border=True, height="stretch"):
        st.subheader("Matriz de indicadores")
        st.dataframe(
            fundamentals_table(info),
            hide_index=True,
            width="stretch",
            column_config={
                "Categoria": st.column_config.TextColumn("Categoria", pinned=True),
                "Indicador": st.column_config.TextColumn("Indicador"),
                "Valor": st.column_config.TextColumn("Valor"),
            },
        )
    with context.container(border=True, height="stretch"):
        st.subheader("Contexto corporativo")
        context_rows = {
            "Setor": info.get("sector") or "—",
            "Indústria": info.get("industry") or "—",
            "País": info.get("country") or "—",
            "Funcionários": format_compact(info.get("fullTimeEmployees")),
            "Valor da firma": format_compact(info.get("enterpriseValue")),
            "Recomendação da fonte": info.get("recommendationKey") or "—",
        }
        st.dataframe(
            pd.DataFrame(context_rows.items(), columns=["Campo", "Valor"]),
            hide_index=True,
            width="stretch",
        )

    with st.spinner("Carregando demonstrações financeiras..."):
        statements = get_financial_statements(filters.ticker)
    if not statements:
        st.info(
            "As demonstrações financeiras não estão disponíveis para este ativo na fonte atual.",
            icon=":material/info:",
        )
        return

    currency = info.get("financialCurrency") or info.get("currency") or "BRL"
    income = statements.get("Resultado")
    if income is not None:
        chart = financial_history_chart(income, currency)
        if chart is not None:
            with st.container(border=True):
                st.subheader("Evolução dos resultados")
                plot(chart)

    statement_name = st.segmented_control(
        "Demonstração",
        options=list(statements),
        default=next(iter(statements)),
    ) or next(iter(statements))
    selected = _statement_for_display(statements[statement_name], statement_name)
    with st.container(border=True):
        st.subheader(f"{statement_name} · {currency} milhões")
        st.dataframe(
            selected,
            width="stretch",
            column_config={
                column: st.column_config.NumberColumn(column, format="%.1f")
                for column in selected.columns
            },
        )
        st.caption("Valores anuais, convertidos para milhões. Sinais negativos foram preservados.")


def render_technical(filters: DashboardFilters, history: pd.DataFrame) -> None:
    st.subheader("Análise técnica e risco")
    technical = add_technical_indicators(history)
    latest = technical.iloc[-1]
    close = safe_float(latest.get("Close"))

    with st.container(horizontal=True):
        st.metric("RSI (14)", format_number(latest.get("RSI"), 1), border=True)
        st.metric("MACD", format_number(latest.get("MACD"), 3), border=True)
        st.metric(
            "Distância da MM20",
            format_percent(close / latest.get("MM20") - 1)
            if close and safe_float(latest.get("MM20"))
            else "—",
            border=True,
        )
        st.metric(
            "Distância da MM200",
            format_percent(close / latest.get("MM200") - 1)
            if close and safe_float(latest.get("MM200"))
            else "—",
            border=True,
        )

    with st.container(border=True):
        plot(technical_chart(history, filters.ticker))

    render_risk_kpis(history, filters.risk_free_rate)
    with st.container(border=True):
        st.subheader("Drawdown histórico")
        plot(drawdown_chart(history))

    st.caption(
        "Indicadores técnicos descrevem comportamento passado e não constituem recomendação de investimento."
    )


def _benchmark_comparison(
    filters: DashboardFilters,
    history: pd.DataFrame,
) -> None:
    if not filters.benchmark:
        st.info("Selecione um benchmark na barra lateral para habilitar esta análise.")
        return

    try:
        benchmark = get_stock_data(filters.benchmark, filters.period)
    except MarketDataError as exc:
        st.warning(str(exc), icon=":material/warning:")
        return

    prices = pd.concat(
        [
            history["Close"].rename(filters.ticker),
            benchmark["Close"].rename(filters.benchmark_label),
        ],
        axis=1,
    )
    with st.container(border=True):
        st.subheader(f"{filters.ticker} vs. {filters.benchmark_label}")
        plot(normalized_performance_chart(prices))

    asset_risk = calculate_risk_metrics(history, filters.risk_free_rate)
    benchmark_risk = calculate_risk_metrics(benchmark, filters.risk_free_rate)
    relative = calculate_relative_metrics(history, benchmark)
    with st.container(horizontal=True):
        st.metric("Retorno do ativo", format_percent(asset_risk["total_return"]), border=True)
        st.metric("Retorno do benchmark", format_percent(benchmark_risk["total_return"]), border=True)
        st.metric("Correlação", format_number(relative["correlation"], 2), border=True)
        st.metric("Beta da janela", format_number(relative["beta"], 2), border=True)
        st.metric("Alfa anualizado", format_percent(relative["alpha"]), border=True)


def render_comparison(filters: DashboardFilters, history: pd.DataFrame) -> None:
    st.subheader("Comparação relativa")
    _benchmark_comparison(filters, history)

    st.subheader("Grupo de pares")
    defaults = DEFAULT_PEERS.get(filters.market, DEFAULT_PEERS["Internacional"])
    options = sorted(set(defaults + [filters.ticker]))
    default_selection = [filters.ticker] + [ticker for ticker in defaults if ticker != filters.ticker][:3]
    peers = st.multiselect(
        "Ativos para comparar",
        options=options,
        default=default_selection,
        accept_new_options=True,
        max_selections=6,
        help="Digite um ticker adicional e pressione Enter para incluí-lo.",
    )
    peers = list(dict.fromkeys(ticker.strip().upper() for ticker in peers if ticker.strip()))
    if len(peers) < 2:
        st.info("Selecione pelo menos dois ativos para montar o grupo de comparação.")
        return

    try:
        with st.spinner("Carregando o grupo de comparação..."):
            prices = get_peer_prices(tuple(peers), filters.period)
    except MarketDataError as exc:
        st.warning(str(exc), icon=":material/warning:")
        return

    if prices.shape[1] < 2:
        st.warning("Poucos ativos retornaram cotações válidas para a comparação.")
        return

    chart_col, table_col = st.columns([1.7, 1])
    with chart_col.container(border=True, height="stretch"):
        st.subheader("Desempenho normalizado")
        plot(normalized_performance_chart(prices))
    with table_col.container(border=True, height="stretch"):
        st.subheader("Ranking da janela")
        summary = peer_summary(prices)
        st.dataframe(
            summary,
            hide_index=True,
            width="stretch",
            column_config={
                "Ativo": st.column_config.TextColumn("Ativo", pinned=True),
                "Retorno": st.column_config.NumberColumn("Retorno", format="percent"),
                "Retorno anualizado": st.column_config.NumberColumn("Anualizado", format="percent"),
                "Volatilidade": st.column_config.NumberColumn("Volatilidade", format="percent"),
                "Drawdown máximo": st.column_config.NumberColumn("Drawdown", format="percent"),
            },
        )


def render_data(filters: DashboardFilters, history: pd.DataFrame, info: dict) -> None:
    st.subheader("Dados e transparência")
    st.caption("Explore os registros usados nos cálculos ou baixe a série para sua própria análise.")

    display = history.reset_index()
    date_column = display.columns[0]
    display = display.rename(columns={date_column: "Data"})
    visible_columns = [
        column
        for column in ["Data", "Open", "High", "Low", "Close", "Adj Close", "Volume", "Dividends"]
        if column in display.columns
    ]
    display = display[visible_columns]
    currency = info.get("currency") or "BRL"
    symbol = {"BRL": "R$", "USD": "US$", "EUR": "€"}.get(currency, currency)

    with st.container(border=True):
        st.dataframe(
            display,
            hide_index=True,
            width="stretch",
            height=520,
            column_config={
                "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY", pinned=True),
                "Open": st.column_config.NumberColumn("Abertura", format=f"{symbol} %.2f"),
                "High": st.column_config.NumberColumn("Máxima", format=f"{symbol} %.2f"),
                "Low": st.column_config.NumberColumn("Mínima", format=f"{symbol} %.2f"),
                "Close": st.column_config.NumberColumn("Fechamento", format=f"{symbol} %.2f"),
                "Adj Close": st.column_config.NumberColumn("Ajustado", format=f"{symbol} %.2f"),
                "Volume": st.column_config.NumberColumn("Volume", format="compact"),
                "Dividends": st.column_config.NumberColumn("Dividendos", format=f"{symbol} %.4f"),
            },
        )
        csv = history.reset_index().to_csv(index=False).encode("utf-8-sig")
        st.download_button(
            "Baixar histórico em CSV",
            data=csv,
            file_name=f"{filters.ticker.replace('^', '')}_{filters.period}.csv",
            mime="text/csv",
            icon=":material/download:",
        )

    dividends = get_dividends(filters.ticker)
    if not dividends.empty:
        dividend_data = dividends.rename("Valor").reset_index()
        dividend_data.columns = ["Data", "Valor"]
        with st.container(border=True):
            st.subheader("Eventos de proventos")
            st.dataframe(
                dividend_data.sort_values("Data", ascending=False),
                hide_index=True,
                width="stretch",
                column_config={
                    "Data": st.column_config.DatetimeColumn("Data", format="DD/MM/YYYY"),
                    "Valor": st.column_config.NumberColumn("Valor por ação", format=f"{symbol} %.4f"),
                },
            )

    st.info(
        "As cotações, fundamentos e demonstrações são obtidos do Yahoo Finance. "
        "Para decisões profissionais, confira os números nos documentos oficiais da CVM/B3 ou do regulador local.",
        icon=":material/database:",
    )


filters = render_sidebar()

try:
    with st.spinner(f"Carregando {filters.ticker}..."):
        history = get_stock_data(filters.ticker, filters.period)
        company_info = get_company_info(filters.ticker)
except MarketDataError as error:
    st.error(str(error), icon=":material/error:")
    st.caption("Confirme o ticker, verifique sua conexão e tente atualizar novamente.")
    st.stop()

render_company_header(filters.ticker, company_info, history)
render_primary_metrics(history, company_info)

view = st.segmented_control(
    "Área de análise",
    options=["Visão geral", "Fundamentos", "Técnica", "Comparação", "Dados"],
    default="Visão geral",
    width="stretch",
)

if view == "Fundamentos":
    render_fundamentals(filters, company_info)
elif view == "Técnica":
    render_technical(filters, history)
elif view == "Comparação":
    render_comparison(filters, history)
elif view == "Dados":
    render_data(filters, history, company_info)
else:
    render_overview(filters, history, company_info)

st.caption(
    "Conteúdo informativo. Este dashboard não oferece recomendação individualizada nem substitui análise profissional."
)
