from typing import Optional, TypeVar, Generic

from pydantic.generics import GenericModel

from src.common.enums import ResCode

T = TypeVar('T')


class Response(GenericModel, Generic[T]):

    """ 通用返回体结构 """

    # 返回码, 0-代表操作成功， 其他参照`src.common.enums.ResCode`
    code: Optional[int] = 0
    # 说明，包含了发生错误时的错误信息
    msg: Optional[str] = ""
    # 具体的数据
    data: Optional[T] = None

    @staticmethod
    def ok(*, data: Optional[T] = None, msg: Optional[str] = None):
        response = Response(msg=msg, data=data)
        return response.dict()

    @staticmethod
    def error(*, msg: str, data: Optional[T] = None, code: Optional[int] = ResCode.ERROR) -> dict:
        response = Response(code=code, msg=msg, data=data)
        return response.dict()
