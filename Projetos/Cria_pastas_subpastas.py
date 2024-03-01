import os

# Começa descrevendo o caminho base
caminho_base = 'C:/Users/claud/Documents/Arquivos PDF'

# Lista de pastas principais
pastas_principais = ['Odessa', 'Kharkiv', 'Kherson', 'Kiev']

# Lista de subpastas desejadas
subpastas = ['Hostomel', 'Crimeia', 'Kupiansk', 'Kramatosk']

for pasta_principal in pastas_principais:
    caminho_principal = os.path.join(caminho_base, pasta_principal)
    
    # Verifica se a pasta principal existe e a cria se não existir
    if not os.path.exists(caminho_principal):
        os.makedirs(caminho_principal)
    
    # Cria as subpastas dentro da pasta principal
    for subpasta in subpastas:
        caminho_subpasta = os.path.join(caminho_principal, subpasta)
        os.makedirs(caminho_subpasta, exist_ok=True)
        print(f'Criada subpasta: {caminho_subpasta}')
