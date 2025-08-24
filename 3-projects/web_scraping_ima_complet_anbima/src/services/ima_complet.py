import requests
from config.config_directory import DOWNLOAD_PATH_IMA
from utils.save_files import save_file_contents

def downloader_ima_complet(date_ddmmyyyy: str):
    url = "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.xls"
    file_path = DOWNLOAD_PATH_IMA / f"IMA_Completo_{date_ddmmyyyy}.xls"

    try:
        resp = requests.get(url, verify=False)
        resp.raise_for_status()  

        save_file_contents(file_path, resp.content)
        print(f"[OK] Complete IMA downloaded:{file_path}")
        print(f"[OK] IMA Completo baixado: {file_path}")

    except requests.HTTPError as http_err:
        print(f"[ERROR] Unable to download IMA ({resp.status_code}): {http_err}")
        print(f"[ERROR] Não foi possível baixar IMA ({resp.status_code}): {http_err}")
    
    except Exception as err:
        print(f"[ERROR] An error occurred while downloading IMA: {err}")
        print(f"[ERROR] Ocorreu um erro ao baixar IMA: {err}")
