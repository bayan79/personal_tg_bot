from dataclasses import dataclass, field
from typing import Type, Dict, Union


@dataclass(frozen=True)
class Error(BaseException):
    code: Union[int, str]
    message: str
    exception: BaseException = None

    codes: Dict[Union[int, str], str] = field(default_factory=dict,
                                              init=False,
                                              repr=False,
                                              compare=False)


class ErrorFactory:
    base_error: Type[Error] = Error

    @classmethod
    def get_error(cls,
                  code: Union[int, str] = None,
                  message: str = None,
                  exception: BaseException = None) -> Error:
        for error_type in cls.base_error.__subclasses__():
            if code in error_type.codes:
                return error_type(code, message or error_type.codes[code], exception)
        return cls.base_error(code, message, exception)
