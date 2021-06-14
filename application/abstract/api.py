import logging
from typing import Type

from application.dataclasses.urls import ResponseDataclass, URL, Method
from application.keys.base import Key


class APIMeta(type):
    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.logger = logging.getLogger(cls.__name__)


class API(metaclass=APIMeta):
    headers = {}

    def __init__(self):
        self.key: Key

    def get(self, url: URL, endpoint: str, parse: Type[ResponseDataclass] = None, **kwargs):
        kwargs['headers'] = {
            **self.headers,
            **kwargs.get('headers', {})
        }
        return url.request(Method.GET, endpoint, parse=parse, **kwargs)

    def post(self, url: URL, endpoint: str, parse: Type[ResponseDataclass] = None, **kwargs):
        kwargs['headers'] = {
            **self.headers,
            **kwargs.get('headers', {})
        }
        return url.request(Method.POST, endpoint, parse=parse, **kwargs)
