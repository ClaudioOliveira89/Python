import pandas as pd

# Leitura da planilha
df = pd.read_excel('C:/Users/claud/Documents/Excel/Financial_Sample.xlsx')

# Verificando as colunas disponíveis
print("Colunas disponíveis no DataFrame:", df.columns)

# Identificando os nomes exatos das colunas
discounts_col = 'Discounts'  # Nome exato da coluna 'Discounts' sem espaços
sales_col = 'Sales'         # Nome exato da coluna 'Sales' sem espaços

# Garantindo que todos os valores em 'Discounts' sejam negativos
df[discounts_col] = df[discounts_col].apply(lambda x: -abs(x))

# Realizando a subtração dos valores de 'Discounts' em relação aos valores de 'Sales'
df['Resultado'] = df[sales_col] - df[discounts_col]

# Calculando o total resultante dessa operação
total_resultado = df['Resultado'].sum()

# Calculando o saldo total (somando valores de 'Sales' e subtraindo valores de 'Discounts')
total_sales = df[sales_col].sum()
total_discounts = df[discounts_col].sum()
saldo_total = total_sales + total_discounts

df_totais = pd.DataFrame({
    'Categoria': ['Total Desconto', 'Total Sales', 'Resultado', 'Saldo'],
    'Valor': [total_discounts, total_sales, total_resultado, saldo_total]
})

# Salvando o DataFrame dos totais em uma nova planilha
df_totais.to_excel('C:/Users/claud/Documents/Excel/Totais_PL.xlsx', index=False)

print("Total resultante da subtração de 'Discounts' em 'Sales':", total_resultado)
print("Total de saldo que sobrou:", saldo_total)
