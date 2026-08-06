import streamlit as st
import plotly.express as px

def render_price_chart(df, ticker):

    fig = px.line(
        df,
        x=df.index,
        y="Close",
        title=f"{ticker} - Histórico de Preços"
    )

    fig.update_layout(
        xaxis=dict(
            tickformat="%d/%m/%Y"
        ),
        xaxis_title="Data",
        yaxis_title="Preço (R$)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )