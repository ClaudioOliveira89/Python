import base64
import json
import requests

payload = {"language": "pt-br"}
encoded = base64.b64encode(json.dumps(payload).encode("utf-8")).decode("ascii")
url = f"https://sistemaswebb3-derivativos.b3.com.br/financialIndicatorsProxy/FinancialIndicators/GetFinancialIndicators/{encoded}"
print(url)
r = requests.get(url, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"}, timeout=30)
print(r.status_code)
print(r.text[:4000])
