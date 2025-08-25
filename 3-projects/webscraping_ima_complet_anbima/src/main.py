from datetime import datetime 
from config.config_directory import DATE_REFERENTIAL 
from pipeline import ima_complet


if __name__ == "__main__": 
    use_date_manual = True 
    data_manual = "20250822" 

    if use_date_manual: 
        date_ima = datetime.strptime(data_manual, "%Y%m%d").strftime("%d%m%Y") 
    else: 
        date_ima = datetime.today().strftime("%d%m%Y")

    ima_complet.downloader_ima_complet(date_ima)
    xls_path = f"report/IMA_{date_ima}.xls"
 

    print("Data IMA: ", date_ima)
