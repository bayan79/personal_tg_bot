from decimal import Decimal
from typing import List, TypeVar, Generic

from pydantic import BaseModel
from pydantic.generics import GenericModel

from application.dataclasses.urls import ResponseDataclass
from application.enums.currency import Currency
from api.jsdelivr.methods import JSDelivr


TinkoffResponseType = TypeVar('TinkoffResponseType')

CURRENCY_API = JSDelivr()


# =========== Stocks ===========

class Price(BaseModel):
    currency: Currency
    value: Decimal

    @property
    def rub(self):
        return self.as_cur(Currency.RUB)

    @property
    def usd(self):
        return self.as_cur(Currency.USD)

    def as_cur(self, currency: Currency):
        return self.value * CURRENCY_API.get_pair(self.currency.value, currency.value)


class Stock(BaseModel):
    averagePositionPrice: Price
    balance: int
    expectedYield: Price
    figi: str
    instrumentType: str
    isin: str = None
    lots: Decimal
    name: str
    ticker: str

    lastPrice: Price = None


class Stocks(BaseModel):
    positions: List[Stock]

    @property
    def sum(self):
        return sum(stock.lastPrice.usd * stock.balance for stock in self.positions)


# ========= Balance ===========

class CurrencyBalance(BaseModel):
    currency: Currency
    balance: Decimal
    blocked: Decimal = None

    @property
    def price(self) -> Price:
        return Price(currency=self.currency, value=self.balance)


class Balance(BaseModel):
    currencies: List[CurrencyBalance]

    @property
    def sum(self):
        return sum(c.price.usd for c in self.currencies)


# ============ Orderbook =========

class OrderResponse(BaseModel):
    price: float
    quantity: int


class OrderBook(BaseModel):
    figi: str
    depth: int
    bids: List[OrderResponse]
    asks: List[OrderResponse]
    tradeStatus: str
    minPriceIncrement: float = None
    faceValue: float = None
    lastPrice: float = None
    closePrice: float = None
    limitUp: float = None
    limitDown: float = None


# ============= Account ============

class Account(BaseModel):
    brokerAccountType: str
    brokerAccountId: str

    balance: Balance = None
    stocks: Stocks = None

    def __str__(self):
        return f"{self.brokerAccountType}[{self.brokerAccountId}]"


class User(BaseModel):
    accounts: List[Account]


# ========= Responses =========

class TinkoffResponse(ResponseDataclass, GenericModel, Generic[TinkoffResponseType]):
    payload: TinkoffResponseType

    def items(self) -> TinkoffResponseType:
        return self.payload
