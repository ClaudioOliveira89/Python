import re
import requests

url = 'https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsPage/exchangeRate?language=pt-br'
page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30).text
m = re.search(r'src="([^"]*main[^"]*\.js)"', page)
print('main js', m.group(1) if m else 'not found')
if m:
    bundle_url = 'https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsPage/' + m.group(1)
    data = requests.get(bundle_url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=30).text
    print('bundle len', len(data))

    for token in ['getIndicators', 'getIndicatorsService', 'exchangeRates', 'TAXAS DE CÂMBIO', 'TAXAS DE CAMBIO', 'financialIndicators', 'api', 'http', 'https']:
        lower_token = token.lower()
        if lower_token in data.lower():
            idx = data.lower().find(lower_token)
            print('TOKEN', token)
            print(data[idx-800:idx+2000])
            print('---')
