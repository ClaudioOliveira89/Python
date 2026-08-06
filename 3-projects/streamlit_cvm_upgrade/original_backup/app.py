import streamlit as st
from services.sidebar import render_sidebar
from services.yahoo_service import get_stock_data
from services.metrics import render_metrics
from services.charts import render_price_chart


st.markdown("""
    <style>
        /* Remove borda do text_input */
        [data-testid="stTextInput"] > div {
            box-shadow: none !important;
            border: none !important;
        }

        /* Remove borda do selectbox */
        [data-testid="stSelectbox"] > div > div {
            border: none !important;
            box-shadow: none !important;
        }
        

        /* Remove o foco azul/vermelho ao clicar */
        [data-testid="stTextInput"] input:focus,
        [data-testid="stSelectbox"] > div > div:focus {
            border: none !important;
            box-shadow: none !important;
            outline: none !important;
        }
       
    </style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Stocks Analytics Dashboard",
    page_icon="assets/images/logo.png",
    layout="wide"
)

st.markdown("""
    <h1 style='
        text-align: center;
        font-size: 42px;
        margin-top: -20px;
        margin-bottom: 30px;
    '>
       
    </h1>
""", unsafe_allow_html=True)
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image(
        "images/Analytics2.png",
        width=1200
    )

st.markdown("""
    <h1 style='
        text-align: center;
        font-size: 50px;
        margin-top: -20px;
        margin-bottom: 30px;
    '>
        Analytics for Financial Markets
    </h1>
""", unsafe_allow_html=True)
ticker, period = render_sidebar()

df = get_stock_data(
    ticker=ticker,
    period=period
)

render_metrics(df)

render_price_chart(df, ticker)