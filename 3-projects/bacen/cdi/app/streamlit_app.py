import sys
import pandas as pd
import streamlit as st
from pathlib import Path
from src.storage.parquet_storage import load_cdi_parquet, filter_cdi_by_date


BASE_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = BASE_DIR / "src"

sys.path.append(str(BASE_DIR))

PARQUET_PATH = BASE_DIR / "data" / "processed" / "cdi_bacen.parquet"


st.set_page_config(
    page_title="CDI Bacen",
    layout="wide"
)


@st.cache_data
def load_data():
    return load_cdi_parquet(PARQUET_PATH)


def format_date_br(date_value):
    return date_value.strftime("%d/%m/%Y")


def format_percent_br(value, decimals=2):
    return f"{value:.{decimals}f}%".replace(".", ",")


def format_decimal_br(value, decimals=6):
    return f"{value:.{decimals}f}".replace(".", ",")


df = load_data()

st.title("CDI Bacen")

st.caption("Base carregada a partir do arquivo Parquet processado pelo pipeline.")



# FILTRO DE DATA

min_date = df["data"].min().date()
max_date = df["data"].max().date()

st.sidebar.header("Filtros")

date_range = st.sidebar.date_input(
    "Selecione o período",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = min_date
    end_date = max_date


df_filtered = filter_cdi_by_date(
    df=df,
    start_date=start_date,
    end_date=end_date
)




st.sidebar.header("Buscar data específica")

selected_date = st.sidebar.date_input(
    "Data para consulta",
    value=max_date,
    min_value=min_date,
    max_value=max_date,
    format="DD/MM/YYYY"
)

df_selected = df[df["data"].dt.date == selected_date]



# MÉTRICAS PRINCIPAIS


st.subheader("Resumo do período")

if df_filtered.empty:
    st.warning("Nenhum dado encontrado para o período selecionado.")
    st.stop()


last_row = df_filtered.sort_values("data").iloc[-1]
first_row = df_filtered.sort_values("data").iloc[0]

variacao_taxa_aa = (
    last_row["taxa_cdi_aa_pct"] -
    first_row["taxa_cdi_aa_pct"]
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Primeira data",
    value=format_date_br(first_row["data"])
)

col2.metric(
    label="Última data",
    value=format_date_br(last_row["data"])
)

col3.metric(
    label="CDI anual atual",
    value=format_percent_br(last_row["taxa_cdi_aa_pct"]),
    delta=format_percent_br(variacao_taxa_aa),
)

col4.metric(
    label="Fator diário atual",
    value=format_decimal_br(last_row["fator_diario"], 6)
)





st.subheader("Consulta por data específica")

if df_selected.empty:
    st.info("Não existe CDI para essa data. Pode ser fim de semana, feriado ou data sem divulgação.")
else:
    selected_row = df_selected.iloc[0]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Data",
        format_date_br(selected_row["data"])
    )

    c2.metric(
        "CDI diário",
        format_percent_br(selected_row["taxa_cdi_ad_pct"], 6)
    )

    c3.metric(
        "CDI anual",
        format_percent_br(selected_row["taxa_cdi_aa_pct"], 2)
    )

    c4.metric(
        "CDI anual decimal",
        format_decimal_br(selected_row["taxa_cdi_aa_decimal"], 6)
    )



# GRÁFICO DE VARIAÇÃO


st.subheader("Variação do CDI anual equivalente")

chart_df = df_filtered.set_index("data")[["taxa_cdi_aa_pct"]]

st.line_chart(chart_df)

st.subheader("Tabela CDI")

df_view = df_filtered.copy()

df_view["data"] = df_view["data"].dt.strftime("%d/%m/%Y")

df_view = df_view.rename(
    columns={
        "data": "Data",
        "taxa_cdi_ad_pct": "CDI diário (%)",
        "taxa_cdi_ad_decimal": "CDI diário decimal",
        "fator_diario": "Fator diário",
        "taxa_cdi_aa_pct": "CDI anual (%)",
        "taxa_cdi_aa_decimal": "CDI anual decimal",
    }
)

st.dataframe(
    df_view,
    use_container_width=True,
    hide_index=True
)