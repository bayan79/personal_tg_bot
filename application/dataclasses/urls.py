import enum
import logging
from dataclasses import dataclass
from typing import Type, Union

import pydantic
import requests
from pydantic import BaseModel


class ResponseDataclass(BaseModel):
    def items(self):
        return self


class Method(enum.Enum):
    GET = enum.auto()
    POST = enum.auto()


@dataclass
class URL:
    base: str

    __logger = logging.getLogger('default.Request')

    def __set_name__(self, owner, name):
        self.__logger = logging.getLogger(owner.__name__)

    def request(self,
                method: Method,
                endpoint: str,
                parse: Type[ResponseDataclass] = None,
                **kwargs) -> Union[requests.Response, ResponseDataclass]:
        method_func = {
            Method.GET: requests.get,
            Method.POST: requests.post,
        }[method]
        result = method_func(self.base + endpoint, **kwargs)

        if result.status_code != 200:
            self.__logger.error(f"Error {result.status_code}: {result.content}")
            raise requests.exceptions.RequestException(result.status_code)

        if parse:
            try:
                return parse.parse_obj(result.json()).items()
            except pydantic.error_wrappers.ValidationError as e:
                self.__logger.error(e.args)
                raise
        return result


if __name__ == '__main__':
    from datetime import datetime, timedelta
    from typing import Any

    class WorldClockAPIResponse(ResponseDataclass):
        currentDateTime: datetime
        utcOffset: timedelta
        isDayLightSavingsTime: bool
        dayOfTheWeek: str
        timeZoneName: str
        currentFileTime: int
        ordinalDate: str
        serviceResponse: Any

    BASE_URL = URL('http://worldclockapi.com/api/')
    resp = BASE_URL.request(Method.GET, endpoint='json/utc/now', parse=WorldClockAPIResponse)
    print(resp)
