import streamlit as st


def render_metrics(df):

    current = df["Close"].iloc[-1]
    previous = df["Close"].iloc[-2]

    variation = ((current - previous) / previous) * 100

    current_color = "green" if current > previous else "red"
    previous_color = "green" if previous > current else "red"
    variation_color = "green" if variation > 0 else "red"

    current_value = (
        f"R$ {current:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

    previous_value = (
        f"R$ {previous:,.2f}"
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )

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