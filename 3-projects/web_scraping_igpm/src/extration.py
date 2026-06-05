import time 
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://www.anbima.com.br/pt_br/informar/estatisticas/precos-e-indices/projecao-de-inflacao-gp-m.htm")
time.sleep(5)

driver.execute_script("document.querySelector('a[href=\"#home\"]').click()")
time.sleep(3)

soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

igpm_div = soup.find("div", {"id": "home"})
tables = igpm_div.find_all("table")

history_table = None
for table in tables:
    if "HISTÓRICO DOS ÚLTIMOS 12 MESES" in table.get_text():
        history_table = table
        break

if history_table:
    df_history = pd.read_html(str(history_table), decimal=",", thousands=".")[0]
    print(df_history)
    df_history.to_excel("Historico_12_meses_igpm.xlsx", index=False)
else:
    print("Table 'LAST 12 MONTHS HISTORY' not found.")
