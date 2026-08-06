# Dólar Spot B3

Coleta as cotações D+1 e D+2 do Dólar BMF Spot e mantém um histórico em
`data/dollar_spot_history.parquet`.

## Instalação

```powershell
python -m pip install -r requirements.txt
```

## Execução

```powershell
python dollar_d2_sport.py
```

## Carga histórica

Os valores anteriores são extraídos dos Boletins Diários do Mercado da B3:

```powershell
python -m dollar_spot.backfill --inicio 2025-01-01 --fim 2026-07-31
```

O comando ignora fins de semana, datas já presentes no Parquet e dias sem
boletim. Como cada PDF precisa ser baixado e interpretado, intervalos longos
podem levar alguns minutos. Os resultados são salvos a cada 20 datas; caso a
execução seja interrompida, basta repetir o comando para continuar.
Os feriados sem sessão de negociação são excluídos pelo calendário oficial da
B3; não há preenchimento artificial com a cotação do dia útil anterior.
O coletor tenta as variantes históricas dos nomes dos PDFs em português e em
inglês e os códigos de boletim `BDI_00`/`BDI_02`, pois nem todas as datas são
servidas de forma uniforme pelo Acervo.

Cada resultado também é sincronizado imediatamente em
`data/backfill_checkpoint.jsonl`. O andamento completo, incluindo boletins
ausentes e erros, fica em `logs/backfill.log`. Ao repetir o comando após fechar
o terminal, o checkpoint é recuperado antes de a coleta continuar.

Cada data de referência ocupa uma única linha. Uma nova execução para uma data
já existente atualiza essa linha, em vez de duplicá-la.

O histórico diferencia `reference_date`, que é a data da cotação divulgada pela
B3, de `collected_at_utc`, que registra o instante da coleta como timestamp UTC.

## Estrutura

```text
dollar_spot/
├── domain.py       # modelo das cotações
├── parser.py       # interpretação da resposta da B3
├── b3_client.py    # comunicação HTTP
├── bdi_client.py   # download de boletins históricos
├── bdi_parser.py   # extração de RTDOLD1 e RTDOLD2 dos PDFs
├── backfill.py     # comando de carga histórica
├── repository.py   # histórico Parquet
├── service.py      # fluxo de coleta e persistência
├── cli.py          # saída no terminal
└── config.py       # URLs e caminhos padrão
```

O arquivo `dollar_d2_sport.py` foi mantido como entrada compatível com a versão
anterior.
