from decimal import Decimal
from typing import List, TypeVar, Generic

from pydantic import BaseModel, validator
from pydantic.generics import GenericModel

from api.binance.errors import BinanceErrorFactory
from application.dataclasses.urls import ResponseDataclass, ErrorResponse

BinanceResponseType = TypeVar('BinanceResponseType')


class Price(BaseModel):
    symbol: str
    price: Decimal


class Network(BaseModel):
    addressRegex: str
    coin: str
    depositDesc: str = None
    depositEnable: bool
    isDefault: bool
    memoRegex: str
    minConfirm: int
    name: str
    network: str
    resetAddressStatus: bool
    specialTips: str = None
    unLockConfirm: int
    withdrawDesc: str = None
    withdrawEnable: bool
    withdrawFee: Decimal
    withdrawIntegerMultiple: Decimal
    withdrawMax: Decimal
    withdrawMin: Decimal


class Coin(BaseModel):
    coin: str
    depositAllEnable: bool
    free: Decimal
    freeze: Decimal
    ipoable: Decimal
    ipoing: Decimal
    isLegalMoney: bool
    locked: Decimal
    name: str
    networkList: List[Network]
    storage: Decimal
    trading: bool
    withdrawAllEnable: bool
    withdrawing: Decimal


class Capital(BaseModel):
    __root__: List[Coin]

    @validator('__root__')
    def validator__root__(cls, v):
        return [i for i in v if i.free != 0]


class Balance(BaseModel):
    asset: str
    free: Decimal
    locked: Decimal


class User(BaseModel):
    accountType: str
    balances: List[Balance]
    buyerCommission: Decimal
    canDeposit: bool
    canTrade: bool
    canWithdraw: bool
    makerCommission: int
    permissions: List[str]
    sellerCommission: int
    takerCommission: int
    updateTime: int


# ========= Responses =========

class BinanceErrorResponse(ErrorResponse):
    __error_factory__ = BinanceErrorFactory

    code: int
    msg: str

    @property
    def exception(self):
        return self.__error_factory__.get_error(code=self.code, message=self.msg)


class BinanceResponse(ResponseDataclass, GenericModel, Generic[BinanceResponseType]):
    __error_response__ = BinanceErrorResponse
    __root__: BinanceResponseType

    def items(self) -> BinanceResponseType:
        return self.__root__

