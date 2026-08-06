from datetime import datetime 
from pathlib import Path

DOWNLOAD_PATH_IMA = Path(__file__).resolve().parent.parent.parent


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DOWNLOAD_PATH_IMA = BASE_DIR / "downloads"
DATE_REFERENTIAL = datetime.today().strftime("%d%m%Y") 
URL = "https://www.anbima.com.br/informacoes/ima/arqs/ima_completo.xls"  
