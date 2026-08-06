## 📊 Public Bond Rates Downloader – ANBIMA

### English Description

Web scraping is a form of data mining that enables the extraction of information from websites, converting it into structured data. In this project, I automate the collection of Brazilian public bond rates published by ANBIMA, saving the results into XLS files for further use, analysis, or the production of indexes and indicators.

📊 **Public Bond Rates Downloader – ANBIMA**

An automated tool for downloading Brazilian public bond rates published by ANBIMA. It saves the source data as an Excel file for structured analysis and financial research. The project provides implementations in both Python and PowerShell and validates the downloaded file before saving it.

---

### Portuguese Description

Web scraping é uma forma de mineração que permite a extração de dados de sites da web, convertendo-os em informação estruturada. Neste projeto, eu automatizo a coleta das Taxas de Títulos Públicos publicadas pela ANBIMA, salvando os resultados em arquivos XLS para uso posterior, análise ou produção de índices e indicadores.

📊 **Downloader de Taxas de Títulos Públicos – ANBIMA**

Ferramenta automatizada para baixar as Taxas de Títulos Públicos publicadas pela ANBIMA. Salva os dados de origem em um arquivo Excel e valida a planilha antes de armazená-la. O projeto disponibiliza implementações em Python e PowerShell, sendo ideal para análises estruturadas e pesquisas financeiras.

---

### Project Structure / Estrutura do Projeto

```text
.
├── src/
│   └── baixar_taxas_anbima.py
├── powershell/
│   └── baixar_taxas_anbima.ps1
├── downloads_anbima/        # generated files / arquivos gerados
├── .gitignore
└── README.md
```

### Requirements / Requisitos

- Python 3.9 or later; or / ou
- PowerShell 5.1 or later.
- Internet access / Acesso à internet.

No third-party packages are required. / Nenhum pacote de terceiros é necessário.

### Usage / Como usar

Python:

```bash
python src/baixar_taxas_anbima.py
python src/baixar_taxas_anbima.py --destino minha_pasta
```

PowerShell:

```powershell
./powershell/baixar_taxas_anbima.ps1
./powershell/baixar_taxas_anbima.ps1 -Destino minha_pasta
```

By default, the spreadsheet is saved in `downloads_anbima/`. This directory is ignored by Git because it contains generated data.

Por padrão, a planilha é salva em `downloads_anbima/`. Essa pasta é ignorada pelo Git por conter dados gerados.

### Data Source / Fonte dos Dados

- [ANBIMA – Taxas de Títulos Públicos](https://www.anbima.com.br/pt_br/informar/taxas-de-titulos-publicos.htm)
