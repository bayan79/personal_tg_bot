import enum
import logging
from dataclasses import dataclass
from typing import Type, Union

import pydantic
import requests
from pydantic import BaseModel

from application.errors import ErrorFactory


class ErrorResponse(BaseModel):
    __error_factory__: Type[ErrorFactory] = ErrorFactory

    code: str
    message: str

    @property
    def exception(self):
        return self.__error_factory__.get_error(code=self.code, message=self.message)


class ResponseDataclass(BaseModel):
    __error_response__: Type[ErrorResponse] = ErrorResponse

    def items(self):
        return self

    @classmethod
    def extract_error(cls, response: requests.Response) -> BaseException:
        try:
            return cls.__error_response__.parse_obj(response.json()).exception
        except:
            return cls.__error_response__.__error_factory__.get_error(
                code=response.status_code,
                message=response.text
            )


class Method(enum.Enum):
    GET = enum.auto()
    POST = enum.auto()

    @property
    def request(self):
        return {
            Method.GET: requests.get,
            Method.POST: requests.post,
        }.get(self)


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
        result = method.request(self.base + endpoint, **kwargs)
        if result.status_code != 200:
            raise self.get_error(result, response_model=parse)

        if parse:
            try:
                return parse.parse_obj(result.json()).items()
            except pydantic.error_wrappers.ValidationError as e:
                raise
            except Exception as e:
                raise self.get_error(result, response_model=parse)
        return result

    def get_error(self,
                  response: requests.Response,
                  response_model: Type[ResponseDataclass] = None):
        self.__logger.error(f"Error {response.status_code}: {response.content[:100]}")

        if not response_model:
            return ErrorFactory.get_error(response.status_code, response.text)
        error = response_model.extract_error(response)
        return error


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

    BASE_URL = URL('https://worldclockapi.com/api/')
    resp = BASE_URL.request(Method.GET, endpoint='json/utc/now', parse=WorldClockAPIResponse)
    print(resp)
