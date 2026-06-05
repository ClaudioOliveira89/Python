import streamlit as st

from services.sidebar import render_sidebar
from services.yahoo_service import get_stock_data
from services.metrics import render_metrics
from services.charts import render_price_chart


st.set_page_config(
    page_title="Stocks Analytics Dashboard",
    page_icon="images/logo.png",
    layout="wide"
)
st.title("Analytics for Financial Markets")



col1, col2, col3 = st.columns([1, 2, 3])

with col3:
    st.image(
        "images/Analytics3.png",
        width=600
    )

st.markdown("<br>", unsafe_allow_html=True)




def render_dashboard():

    ticker, period = render_sidebar()

    df = get_stock_data(
        ticker=ticker,
        period=period
    )

    render_metrics(df)

    render_price_chart(df, ticker)




render_dashboard()