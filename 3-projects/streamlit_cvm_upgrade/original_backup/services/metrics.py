import streamlit as st


def format_currency(value, prefix="R$"):
    return (
        f"{prefix} {value:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )


def render_metrics(df):

    if df is None or df.empty:
        st.warning("Não há dados disponíveis para este ativo.")
        return

    if "Close" not in df.columns:
        st.warning("A coluna Close não foi encontrada nos dados.")
        return

    close_prices = df["Close"].dropna()

    if len(close_prices) < 2:
        st.warning("Dados insuficientes para calcular as métricas deste ativo.")
        return

    current = close_prices.iloc[-1]
    previous = close_prices.iloc[-2]

    if previous == 0:
        st.warning("Não foi possível calcular a variação porque a cotação anterior é zero.")
        return

    variation = ((current - previous) / previous) * 100

    current_color = "green" if current > previous else "red"
    previous_color = "green" if previous > current else "red"
    variation_color = "green" if variation > 0 else "red"

    current_value = format_currency(current)
    previous_value = format_currency(previous)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="
            padding:20px;
            border-radius:15px;
            background-color:rgba(0,0,0,0);
            border:1px solid rgba(128,128,128,0.2);
            backdrop-filter: blur(10px);
            text-align:center;
        ">
            <h4>Cotação Atual</h4>
            <h2 style="color:{current_color};">
                {current_value}
            </h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="
            padding:20px;
            border-radius:15px;
            background-color:rgba(0,0,0,0);
            border:1px solid rgba(128,128,128,0.2);
            backdrop-filter: blur(10px);
            text-align:center;
        ">
            <h4>Cotação Anterior</h4>
            <h2 style="color:{previous_color};">
                {previous_value}
            </h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="
            padding:20px;
            border-radius:15px;
            background-color:rgba(0,0,0,0);
            border:1px solid rgba(128,128,128,0.2);
            backdrop-filter: blur(10px);
            text-align:center;
        ">
            <h4>Variação</h4>
            <h2 style="color:{variation_color};">
                {variation:.2f}%
            </h2>
        </div>
        """, unsafe_allow_html=True)