import os 
import shutil 
import pandas as pd 

# Caminho do arquivo excel.
df = pd.read_excel('C:/Users/claud/Documents/Excel/PL_testes.xlsx')
print(df.columns)

# Endereço do diretório de onde serão criadas as pastas.
base_dir = 'C:/Users/claud/Documents/Arquivos PDF'

# Iterando sobre os fundos na planilha
for fundo in df['RAZÃO_SOCIAL'].unique():
    # Formatando o nome do fundo e CNPJ
    nome_formatado = fundo[:20]  # Limitando a 20 caracteres
    cnpj = df[df['RAZÃO_SOCIAL'] == fundo]['CNPJ'].iloc[0]  # Pegando o CNPJ correspondente ao fundo
    
    # Removendo caracteres não numéricos do CNPJ
    cnpj = ''.join(filter(str.isdigit, str(cnpj)))

    # Formatando o CNPJ
    cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}.{cnpj[8:12]}-{cnpj[12:]}"

    # Criando as pastas e subpastas
    for subpasta in ['ATAS', 'CONTRATOS e REGULAMENTOS', 'CARTAS', 'INVESTIDA', 'NFS', 'RATING']:
        fundo_dir = os.path.join(base_dir, f"{nome_formatado} {cnpj_formatado}", subpasta)
        os.makedirs(fundo_dir, exist_ok=True)

print("Pastas criadas com sucesso!")


