import requests
from bs4 import BeautifulSoup

def fetch_page(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar a página: {e}")
        print(f"Error downloading page: {e}")
        return ""

def parse_table(html: str) -> list:
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='tb_principal1')
    data_rows = []

    if table:
        all_td = table.find_all('td')
        for i in range(0, len(all_td), 2):
            row = all_td[i:i+2]
            if len(row) == 2:
                data_rows.append([cell.get_text(strip=True) for cell in row])
    else:
        print("Tabela não encontrada...")
        print("Table not found...")
    return data_rows

