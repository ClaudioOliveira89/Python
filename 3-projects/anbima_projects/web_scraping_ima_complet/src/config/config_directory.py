from datetime import datetime 
from pathlib import Path 

BASE_DIR = Path(__file__).resolve().parent.parent 
DATE_REFERENTIAL = datetime.today().strftime("%d%m%Y") 

DOWNLOAD_PATH_IMA = Path(r"downloads")