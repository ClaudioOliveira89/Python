from pathlib import Path
from datetime import datetime
from utils.fetcher import fetch_page, parse_table
from utils.write import write_to_excel
from config.config_loader import URL as BASE_URL

def run_pipeline(date: str = None):

    if date is None:
        date_obj = datetime.now()
    else:
        date_obj = datetime.strptime(date, "%Y-%m-%d")

 
    date_str = date_obj.strftime("%d/%m/%Y")      # para URL versão em português. 
    data1_str = date_obj.strftime("%Y%m%d")       # for URL version in english. 
    date_str_file = date_obj.strftime("%d_%m_%Y") # file


    url_parts = BASE_URL.split("?")[0]
    taxa = "DOL"
    URL = f"{url_parts}?Data={date_str}&Data1={data1_str}&slcTaxa={taxa}"


    OUTPUT_FILE = Path(f"report/DI_dolar_{date_str_file}.xlsx")

  
    html = fetch_page(URL)
    if not html:
        print("Erro ao baixar a página.")
        print("Error downloading page.")
        return

    data = parse_table(html)
    if not data:
        print("Nenhum dado encontrado na tabela.")
        print("No data found in table.")
        return


    write_to_excel(data, OUTPUT_FILE)

    # Prints bilíngues
    # Bilingual prints
    print(f"Dados salvos em {OUTPUT_FILE}")                         # Português.
    print(f"Data save in {date_obj.strftime('%Y-%m-%d')}")          # English.
    print(f"Data usada para busca: {date_str}")                  
    print(f"Date used for fetch: {date_obj}")                       
