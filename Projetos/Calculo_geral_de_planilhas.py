import os
import pandas as pd

# Pasta contendo os arquivos Excel
pasta = 'C:/Users/claud/Documents/Excel/'

# Lista para armazenar os caminhos dos arquivos Excel na pasta
caminhos = []

# Iterar sobre os arquivos na pasta
for arquivo in os.listdir(pasta):
    # Verificar se o arquivo é um arquivo Excel
    if arquivo.endswith('.xlsx'):
        caminhos.append(os.path.join(pasta, arquivo))

# Listas para armazenar os resultados finais
totais_desconto = []
totais_sales = []
totais_resultado = []
totais_saldo = []

# Iterar sobre cada arquivo na lista de caminhos
for caminho in caminhos:
    # Leitura da planilha
    df = pd.read_excel(caminho)

    # Identificando os nomes exatos das colunas
    discounts_col = 'Discounts'  # Nome exato da coluna 'Discounts' sem espaços
    sales_col = 'Sales'         # Nome exato da coluna 'Sales' sem espaços

    # Garantindo que todos os valores em 'Discounts' sejam negativos
    df[discounts_col] = df[discounts_col].apply(lambda x: -abs(x))

    # Realizando a subtração dos valores de 'Discounts' em relação aos valores de 'Sales'
    df['Resultado'] = df[sales_col] - df[discounts_col]

    # Calculando os totais
    total_sales = df[sales_col].sum()
    total_discounts = df[discounts_col].sum()
    total_resultado = df['Resultado'].sum()
    saldo_total = total_sales + total_discounts

    # Adicionando os totais às listas
    totais_desconto.append(total_discounts)
    totais_sales.append(total_sales)
    totais_resultado.append(total_resultado)
    totais_saldo.append(saldo_total)

# Criando um DataFrame com os totais finais
df_totais = pd.DataFrame({
    'Categoria': ['Total Desconto', 'Total Sales', 'Resultado', 'Saldo'],
    'Valor': [sum(totais_desconto), sum(totais_sales), sum(totais_resultado), sum(totais_saldo)]
})

# Salvando o DataFrame dos totais em uma nova planilha
df_totais.to_excel('C:/Users/claud/Documents/Excel/Totais_Finais.xlsx', index=False)