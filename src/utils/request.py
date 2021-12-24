from flask import request, has_request_context

from logger import logger
from src.exceptions import ProximaException


class RequestUtil:

    @staticmethod
    def parse_int_arg(name, default: int = None) -> int:
        """
        从请求参数中解析出对应变量名的整数值。可以指定默认值。失败时抛出自定义异常。

        :param name: 待获取的参数名
        :param default: 默认值(取不到参数或参数值为空时使用)
        :return: 解析出的整数值或默认值或者None
        """
        if has_request_context():
            val: str = request.args.get(name, None)
            if not val:
                return default
            try:
                return int(val)
            except ValueError:
                logger.error(f"查询参数 {name} 类型错误。请使用整数类型值")
                ProximaException(description=f"查询参数 {name} 类型错误。请使用整数类型值")
