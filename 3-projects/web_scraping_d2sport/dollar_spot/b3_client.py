import base64
import json

import requests

from .config import B3_PROXY_URL


class B3FinancialIndicatorsClient:
    def __init__(self, timeout: int = 30, session=None):
        self.timeout = timeout
        self.session = session or requests.Session()

    def fetch(self) -> tuple[str, bytes, str]:
        payload = {"language": "pt-br"}
        encoded = base64.b64encode(
            json.dumps(payload).encode("utf-8")
        ).decode("ascii")
        url = B3_PROXY_URL.format(encoded_payload=encoded)

        response = self.session.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/126 Safari/537.36"
                ),
                "Accept-Language": "pt-BR,pt;q=0.9",
                "Accept": "application/json",
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.text, response.content, url
