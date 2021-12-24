from typing import Optional, List, Tuple, Dict, Any

import orjson
from werkzeug.exceptions import HTTPException

from src.common.enums import ResCode
from src.core.web.response import Response


class ProximaException(HTTPException):

    code: int = 400
    error_code: int = ResCode.ERROR

    def __init__(self, description=None, error_code: int = None, code: int = None, data=None, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if description:
            self.description = description
        if error_code:
            self.error_code = error_code    
        if code:
            self.code = code
        self.data = data

    def get_headers(self, environ: Optional[Dict[str, Any]] = None, scope: Optional[dict] = None) -> List[Tuple[str, str]]:
        """ 让异常对应的结果为JSON字符串而非默认的H5页面 """
        return [("Content-Type", "application/json")]

    def get_body(self, environ: Optional[Dict[str, Any]] = None, scope: Optional[dict] = None):
        """ 获取结果的具体内容 """
        response = Response.error(msg=self.description, data=self.data, code=self.error_code)
        return orjson.dumps(response)


class UnAuthorizedException(ProximaException):

    code: int = 401
    error_code: int = ResCode.ERROR
    description: str = "身份验证失败"


class InvalidAccountException(ProximaException):
    code: int = 401
    error_code: int = ResCode.ERROR
    description: str = "用户不可用"


class TokenExpiredException(ProximaException):

    code: int = 401
    error_code: int = ResCode.ERROR
    description: str = "登录信息已过期"


class AccessDeniedException(ProximaException):

    code: int = 403
    error_code: int = ResCode.ERROR
    description: str = "拒绝访问"


class NotFoundException(ProximaException):
    code: int = 401
    error_code: int = ResCode.ERROR
    description = "查询对象不存在"
