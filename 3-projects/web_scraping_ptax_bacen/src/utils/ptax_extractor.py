import requests
import pandas as pd
from datetime import datetime
from src.config.settings import PTAX_ENDPOINT

def download_ptax_to_data(date_obj: datetime) -> pd.DataFrame | None:
    date_str = date_obj.strftime("%m-%d-%Y")
    url = PTAX_ENDPOINT.format(date=date_str)

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"[EXTRACT] Error {response.status_code} for {date_obj.strftime('%d/%m/%Y')}")
            return None
    except requests.RequestException as e:
        print(f"[EXTRACT] Request failed for {date_obj.strftime('%d/%m/%Y')}: {e}")
        return None

    data = response.json()
    if not data.get("value"):
        print(f"[EXTRACT] No quotation for {date_obj.strftime('%d/%m/%Y')}")
        return None

    df = pd.DataFrame(data["value"])
    df["dataHoraCotacao"] = pd.to_datetime(df["dataHoraCotacao"])
    df.rename(columns={
        "dataHoraCotacao": "Data e Hora",
        "cotacaoCompra": "Cotação de Compra",
        "cotacaoVenda": "Cotação de Venda"
    }, inplace=True)

    df.set_index("Data e Hora", inplace=True)
    df.index = df.index.round("S")

    return df[["Cotação de Compra", "Cotação de Venda"]]
