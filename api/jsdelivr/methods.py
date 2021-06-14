from decimal import Decimal
from functools import lru_cache

import requests
import os


class JSDelivr:
    """
    Spec: https://github.com/fawazahmed0/currency-api#readme
    """
    BASE_URL = "https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/"

    def __init__(self):
        self.headers = {'Authorization': f'Bearer {os.getenv("TINKOFF_API_TOKEN")}'}

    @lru_cache(maxsize=100)
    def request(self, method, endpoint, data: dict = None, params: dict = None, headers: dict = None):
        args = dict(
            url=JSDelivr.BASE_URL + endpoint,
            data=data,
            params=params,
            headers={**(headers or {}), **self.headers},
        )
        if method == 'GET':
            result = requests.get(**args)
        elif method == 'POST':
            result = requests.post(**args)
        else:
            raise NotImplementedError(f'Wrong method: {method}')

        if result.status_code != 200:
            raise requests.exceptions.RequestException()

        return result.json()

    def get_currencies(self):
        return self.request('GET', 'currencies.json')

    def get_pair(self, base_cur_code: str, value_cur_code: str) -> Decimal:
        base, tar = base_cur_code.lower(), value_cur_code.lower()
        if base == tar:
            return Decimal(1)
        value = self.request('GET', f'currencies/{base}/{tar}.json')
        return Decimal(value[tar])
