from datetime import datetime
from src.utils.ptax_transformer import update_dataframe
from src.utils.ptax_loader import loading_excel, save_excel

def run_ptax_pipeline(start_date_str: str, end_date_str: str):
  
    start_date = datetime.strptime(start_date_str, "%d-%m-%Y")
    end_date = datetime.today() if end_date_str.lower() == "hoje" else datetime.strptime(end_date_str, "%d-%m-%Y")

  
    df_existing = loading_excel()

    df_updated = update_dataframe(start_date, end_date, df_existing)

    if df_updated.empty:
        print("[PIPELINE] No data updated.")
        return

    save_excel(df_updated)
    print("[PIPELINE] Completed successfully.")
