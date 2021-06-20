import datetime
import os

from application.abstract.api import API
from application.dataclasses.urls import URL
from application.keys import ClientKey

from .datamodels import User, BinanceResponse, Capital, Price


class Binance(API):
    """
    https://binance-docs.github.io/apidocs/spot/en/#contact-us
    """
    BASE_URL = URL("https://api.binance.com/")

    def __init__(self):
        super().__init__()
        self.key: ClientKey = ClientKey(token=os.getenv("BINANCE_API_KEY"),
                                        secret=os.getenv("BINANCE_SECRET"))
        self.headers = self.key.header()

    def get_user_balance(self) -> Capital:
        params = {
            'timestamp': int(datetime.datetime.now().timestamp() * 1000),
        }
        params['signature'] = self.key.get_signature(params)

        capital: Capital = self.get(self.BASE_URL,
                                    endpoint='sapi/v1/capital/config/getall',
                                    params=params,
                                    parse=BinanceResponse[Capital])
        return capital

    def get_price(self, coin: str) -> Price:
        price: Price = self.get(self.BASE_URL,
                                endpoint='api/v3/ticker/price',
                                params={'symbol': f"{coin}USDT"},
                                parse=BinanceResponse[Price])
        return price
