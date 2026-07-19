import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Simulador Monte Carlo", layout="wide")

st.title("Simulador Monte Carlo - Ativo Financeiro")

st.sidebar.header("Parâmetros")

preco_inicial = st.sidebar.number_input(
    "Preço inicial",
    min_value=1.0,
    value=100.0,
    step=1.0
)

retorno_esperado = st.sidebar.slider(
    "Retorno esperado ao ano (%)",
    min_value=-50.0,
    max_value=100.0,
    value=12.0,
    step=1.0
) / 100

volatilidade = st.sidebar.slider(
    "Volatilidade ao ano (%)",
    min_value=1.0,
    max_value=100.0,
    value=25.0,
    step=1.0
) / 100

anos = st.sidebar.slider(
    "Anos",
    min_value=1,
    max_value=10,
    value=1
)

simulacoes = st.sidebar.slider(
    "Número de simulações",
    min_value=100,
    max_value=10000,
    value=1000,
    step=100
)

qtd_linhas_grafico = st.sidebar.slider(
    "Caminhos exibidos no gráfico",
    min_value=10,
    max_value=200,
    value=50
)

seed = st.sidebar.number_input(
    "Seed aleatória",
    min_value=0,
    value=42,
    step=1
)

dias_por_ano = 252
dias = anos * dias_por_ano
dt = 1 / dias_por_ano

rng = np.random.default_rng(seed)

z = rng.normal(0, 1, size=(dias, simulacoes))

retornos = (
    (retorno_esperado - 0.5 * volatilidade ** 2) * dt
    + volatilidade * np.sqrt(dt) * z
)

precos = preco_inicial * np.exp(np.cumsum(retornos, axis=0))
precos = np.vstack([np.full(simulacoes, preco_inicial), precos])

precos_finais = precos[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("Preço médio final", f"R$ {np.mean(precos_finais):,.2f}")
col2.metric("Mediana final", f"R$ {np.median(precos_finais):,.2f}")
col3.metric("Percentil 5%", f"R$ {np.percentile(precos_finais, 5):,.2f}")
col4.metric(
    "Prob. abaixo do inicial",
    f"{np.mean(precos_finais < preco_inicial) * 100:.2f}%"
)

df_precos = pd.DataFrame(
    precos[:, :qtd_linhas_grafico],
    columns=[f"Simulação {i + 1}" for i in range(qtd_linhas_grafico)]
)

df_precos["Dia"] = range(len(df_precos))

df_long = df_precos.melt(
    id_vars="Dia",
    var_name="Simulação",
    value_name="Preço"
)

fig = px.line(
    df_long,
    x="Dia",
    y="Preço",
    color="Simulação",
    title="Caminhos simulados do ativo"
)

st.plotly_chart(fig, use_container_width=True)

df_finais = pd.DataFrame({"Preço final": precos_finais})

fig_hist = px.histogram(
    df_finais,
    x="Preço final",
    nbins=60,
    title="Distribuição dos preços finais"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Resumo estatístico")

resumo = pd.DataFrame({
    "Indicador": [
        "Preço inicial",
        "Preço médio final",
        "Mediana final",
        "Percentil 5%",
        "Percentil 95%",
        "Menor preço final",
        "Maior preço final",
        "Probabilidade de perda"
    ],
    "Valor": [
        preco_inicial,
        np.mean(precos_finais),
        np.median(precos_finais),
        np.percentile(precos_finais, 5),
        np.percentile(precos_finais, 95),
        np.min(precos_finais),
        np.max(precos_finais),
        np.mean(precos_finais < preco_inicial) * 100
    ]
})

st.dataframe(resumo, use_container_width=True)