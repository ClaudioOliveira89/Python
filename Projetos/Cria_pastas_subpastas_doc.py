#Script para ler planilha, cria pasta, subpastas e cartas.

import os 
import shutil 
import pandas as pd 

#Caminho do arquivo excel.
df = pd.read_excel('.xlsx')

#Endreço do diretório de onde será o criado as pastas.
base_dir = ' '

#Aqui será lido os campos da planilha, onde vai cria pastas e subpastas.
for fundo in df['RAZÃO SOCIAL'].unique():
    for subpasta in ['ATAS', 'CONTRATOS e REGULAMENTOS', 'CARTAS', 'INVESTIDA','NFS','RATING']:
        fundo_dir = os.path.join(base_dir, fundo, subpasta)
os.makedirs(fundo_dir, exist_ok=True)

#fará o mapeamento do auditor do fundo verificado as colunas e comparando com o campo fundo.
mapeamento_auditor_fundo = {}
for index, row in df.iterrows():
    auditor = row['AUDITORIA 2024']
    fundo = row['RAZÃO SOCIAL']
    if auditor not in 
    mapeamento_auditor_fundo:
    mapeamento_auditor_fundo[auditor] = []
    mapeamento_auditor_fundo[auditor].append(fundo)

    #Diretório base onde as cartas serão coletadas
    auditor_dir = r''


    #Loop onde as cartas serão copiadas para as pastas.
    for audirtor in 
    mapeamento_auditor_fundo:
    caminho_auditor = 
    os.path.join(auditor_dir, auditor)
    for arquivo in
    os.path.join(auditor_dir):
    if arquivo.endswith('.docx'):
        for fundo in 
        mapeamento_auditor_fundo[auditor]:
    
    #Aqui vai a base_dir onde vai copiar e salvar as cartas.
    destino = os.path.join(base_dir, fundo, 'CARTAS', arquivo)

    #Aqui verifica se o diretório de destino exite, se não cria.
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    shutil.copy(os.path.join(caminho_auditor, arquivo), destino)
    print(f"Copiado {arquivo} para {destino}")
#os valores podem ser modificados para criar qualquer pastas e cartas, de acordo com a sua necessidade. 

#fim