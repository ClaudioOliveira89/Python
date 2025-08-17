📊 Web Scraper DI Dólar – B3

Ferramenta para coleta automatizada das taxas DI e Dólar publicadas pela B3, com exportação para Excel. Permite extrair dados de uma data específica ou da última data disponível.
Automated tool for collecting DI and Dollar rates published by B3, with Excel export. Supports fetching a specific date or the latest available.


📂 Estrutura do Projeto / Project Structure
src/
├─ main.py                  # Ponto de entrada / Entry point
├─ pipeline/
│  └─ orchestrator.py       # Orquestra o fluxo do scraper / Orchestrates the scraping flow
├─ repo/
│  ├─ fetcher.py            # Responsável pelo download e parsing do HTML / Handles HTML fetch & parsing
│  └─ writer.py             # Responsável pela exportação para Excel / Handles Excel export
├─ config/
│  └─ config_loader.py      # Configuração de URLs e diretórios / URL & directory configuration
report/                      # Diretório para arquivos Excel gerados / Generated Excel files

🛠️ Requisitos / Requirements

Python 3.10 ou superior / Python 3.10+

Bibliotecas / Libraries: requests, beautifulsoup4, openpyxl

pip install requests beautifulsoup4 openpyxl

🚀 Uso / Usage

Por data específica / For a specific date:

from pipeline.orchestrator import run_pipeline

run_pipeline(date="2025-08-15")


Última data disponível / Latest available date:

run_pipeline()

💾 Saída / Output

Arquivos Excel são gerados no diretório report/
Excel files are generated in the report/ directory

Formato do arquivo / File format: DI_dolar_DD_MM_YYYY.xlsx

Exemplo de saída / Example output:

Dados salvos em report/DI_dolar_15_08_2025.xlsx
Data usada para busca: 15/08/2025
Date used for fetch: 2025-08-15

⚠️ Observações / Notes

Atualmente captura apenas a taxa DOL / Currently fetches only DOL rate.

Ajuste a URL no arquivo config/config_loader.py caso necessário / Adjust the URL in config/config_loader.py if needed.