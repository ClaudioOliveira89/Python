import pandas as pd 
from src.config.settings import PTAX_FILE

def loading_excel() -> pd.DataFrame:
    if not PTAX_FILE.exists():
        df = pd.DataFrame(columns=["Cotação de Compra", "Cotação de Venda"])
        df.index.name = "Data e Hora"
        return df 
    
    df = pd.read_excel(PTAX_FILE)
    df.columns = df.columns.str.strip()
    df = df.loc[:, ~df.columns.duplicated()]
    df["Data e Hora"] = pd.to_datetime(df["Data e Hora"], dayfirst=True, errors="coerce")
    df.set_index("Data e Hora", inplace=True)
    df.index = df.index.round("S")

    for col in ["Cotação de Compra", "Cotação de Venda"]:
        if col not in df.columns:
            df[col] = pd.NA
    
    return df

def save_excel(df: pd.DataFrame):
    df_reset = df.copy().reset_index()
    for col in ["Cotação de Compra", "Cotação de Venda"]:
        df_reset[col] = pd.to_numeric(df_reset[col], errors="coerce")
        df_reset[col] = df_reset[col].map(lambda x: f"{x: .4f}".replace(".", ",") if pd.notnull(x) else "")
    df_reset["Data e Hora"] = df_reset["Data e Hora"].dt.strftime("%d/%m/%Y %H:%M:%S")

    backup_file = PTAX_FILE.with_name(f"ptax_{pd.Timestamp.now():%Y%m%d_%H%M%S}.xlsx")
    df_reset.to_excel(backup_file, index=False)
    print(f"[LOAD] Backup saved as: {backup_file}")

    