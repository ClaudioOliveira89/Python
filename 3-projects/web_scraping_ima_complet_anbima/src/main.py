from datetime import datetime 
from config.config_directory import DATE_REFERENTIAL 
from services import ima_complet 

if __name__ == "__main__": 
    usar_data_manual = True 
    data_manual = "20250818" 
    if usar_data_manual: 

        date_ima = datetime.strptime(data_manual, "%Y%m%d").strftime("%d%m%Y") 
    else: 
        date_ima = datetime.today().strftime("%d%m%Y")

        ima_complet.downloader_ima_complet(date_ima)

print("Data IMA: ", date_ima)