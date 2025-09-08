import pandas as pd
from datetime import datetime, timedelta
from .ptax_extractor import download_ptax_to_data

def update_dataframe(
    start_date: datetime, 
    end_date: datetime, 
    df_existing: pd.DataFrame | None = None
) -> pd.DataFrame:
    
 
    if df_existing is None:
        df_existing = pd.DataFrame(columns=["Cotação de Compra", "Cotação de Venda"])
        df_existing.index.name = "Data e Hora"

    for i in range((end_date - start_date).days + 1):
        day = start_date + timedelta(days=i)
        df_day = download_ptax_to_data(day)
        if df_day is None:
            continue

 
        indexes_without_value = df_day.index[
            (df_day["Cotação de Compra"].isnull()) & (df_day["Cotação de Venda"].isnull())
        ]
        df_day = df_day.drop(indexes_without_value, errors="ignore")

        for idx, row in df_day.iterrows():
            buying, selling = row["Cotação de Compra"], row["Cotação de Venda"]
            if pd.notnull(buying) or pd.notnull(selling):
                df_existing.loc[idx, "Cotação de Compra"] = buying
                df_existing.loc[idx, "Cotação de Venda"] = selling


    df_existing.sort_index(inplace=True)

    return df_existing
