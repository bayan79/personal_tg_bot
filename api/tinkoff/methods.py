import os
from cachetools import cached, TTLCache

from api.tinkoff.datamodels import Stocks, User, OrderBook, Price, Balance, TinkoffResponse
from application.abstract.api import API
from application.dataclasses.urls import URL
from application.keys.bearer import Bearer


class Tinkoff(API):
    """
    https://tinkoffcreditsystems.github.io/invest-openapi/swagger-ui/
    """
    BASE_URL = URL("https://api-invest.tinkoff.ru/openapi/")
    BASE_SANDBOX_URL = URL("https://api-invest.tinkoff.ru/openapi/sandbox/")

    def __init__(self):
        super().__init__()
        self.key: Bearer = Bearer(token=os.getenv("TINKOFF_API_TOKEN"))
        self.headers = self.key.header()

    def get_user_accounts(self, need_stocks=True, need_balance=True) -> User:
        user: User = self.get(self.BASE_URL, endpoint='user/accounts',
                              parse=TinkoffResponse[User])
        if need_balance or need_stocks:
            for account in user.accounts:
                if need_stocks:
                    account.stocks = self.get_stocks(account.brokerAccountId)
                if need_balance:
                    account.balance = self.get_balance(account.brokerAccountId)
        return user

    def get_stocks(self, account_id) -> Stocks:
        params = {'brokerAccountId': account_id}
        stocks: Stocks = self.get(self.BASE_URL, 'portfolio', params=params,
                                  parse=TinkoffResponse[Stocks])
        stocks.positions = [stock for stock in stocks.positions if stock.instrumentType == 'Stock']
        for stock in stocks.positions:
            orderbook = self.get_orderbook(stock.figi)
            stock.lastPrice = Price(
                currency=stock.averagePositionPrice.currency,
                value=orderbook.lastPrice,
            )
        return stocks

    @cached(cache=TTLCache(maxsize=128, ttl=600))
    def get_orderbook(self, figi: str) -> OrderBook:
        orderbook = self.get(self.BASE_URL, 'market/orderbook', params={
            'figi': figi,
            'depth': 1,
        }, parse=TinkoffResponse[OrderBook])
        return orderbook

    def get_balance(self, account_id: str) -> Balance:
        currencies = self.get(self.BASE_URL, 'portfolio/currencies', params={
            'brokerAccountId': account_id,
        }, parse=TinkoffResponse[Balance])
        return currencies
