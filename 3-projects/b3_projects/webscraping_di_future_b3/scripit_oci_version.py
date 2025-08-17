from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


def extrair_ddi_cupom_cambial():
    driver = webdriver.Chrome()

    url = "https://www2.bmf.com.br/pages/portal/bmfbovespa/lumis/lum-ajustes-do-pregao-ptBR.asp"
    driver.get(url)

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, 'tblDadosAjustes'))
    )

    tabela = driver.find_element(By.ID, 'tblDadosAjustes')
    linhas = tabela.find_elements(By.TAG_NAME, 'tr')

    dados = []
    coletar = False

    for linha in linhas:
        colunas = linha.find_elements(By.TAG_NAME, 'td')
        if not colunas:
            continue

        primeira_coluna = colunas[0].text.strip()

        if 'DCO - Cupom Cambial em OC1' in primeira_coluna:
            coletar = True

        if 'DDI - Cupom cambial' in primeira_coluna:
            break

        if coletar:
           
            if len(colunas) == 6:
                vencimento = colunas[1].text.strip()
                preco_ant = colunas[2].text.strip()
                preco_atual = colunas[3].text.strip()
                variacao = colunas[4].text.strip()
                ajuste = colunas[5].text.strip()

           
            elif len(colunas) == 5:
                vencimento = colunas[0].text.strip()
                preco_ant = colunas[1].text.strip()
                preco_atual = colunas[2].text.strip()
                variacao = colunas[3].text.strip()
                ajuste = colunas[4].text.strip()
            else:
                continue  

            dados.append({
                'Mercadoria': 'DCO - Cupom cambial em OC1',
                'Vencimento': vencimento,
                'Preço de ajuste anterior': preco_ant,
                'Preço de ajuste Atual': preco_atual,
                'Variação': variacao,
                'Valor do ajuste por contrato (R$)': ajuste,
            })

    driver.quit()
    return dados


if __name__ == '__main__':
    dados = extrair_ddi_cupom_cambial()

    if not dados:
        print("Nenhum dado foi capturado.")
    else:
        df = pd.DataFrame(dados)
        df.to_csv('ddi_cupom_cambial_oci.csv', index=False, sep=';')
        df.to_excel('ddi_cupom_cambial_oci.xlsx', index=False)
        print("✔️ Arquivos salvos como 'ddi_cupom_cambial_oci.csv' e 'ddi_cupom_cambial_oci.xlsx'")
