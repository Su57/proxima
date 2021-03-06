from datetime import timedelta
from typing import Dict, Optional

import orjson
from redis import Redis
from werkzeug.local import LocalProxy
from flask import has_request_context, request
from dependency_injector.wiring import Provide, inject

from logger import logger
from settings import settings
from container import Container
from src.utils import SecurityUtil
from src.common.constant import Constant
from src.core.web.schemas import CurrentUser, TokenPayload
from src.exceptions import UnAuthorizedException, TokenExpiredException


@inject
def load_user(redis: Redis = Provide[Container.redis]) -> Optional[CurrentUser]:
    """
    根据token解析出的redis键，加载对应的redis用户数据，并设置为request.user。
    若request.user已经有对应的值，则直接返回值即可

    :param redis: redis客户端
    :return: CurrentUser 对象
    """
    if has_request_context():
        # 先判断是否已经加载到request中，否则可能会多次进行token解析和redis查询
        user = getattr(request, "user", None)
        if user is not None and isinstance(user, CurrentUser):
            return user
        # 从header中获取token
        token: str = request.headers.get("Authorization", None)
        # token存在时，进入token校验程序 -> 要么解析出用户，要么抛出特定异常
        if token is not None and len(token) > 0:
            token = token.replace(Constant.TOKEN_SCHEMA, "").strip()
            payload: Dict = SecurityUtil.parse_token(token=token)
            token_data = TokenPayload(sub=payload["sub"])
            redis_key: str = Constant.AUTH_REDIS_KEY + token_data.sub
            redis_value: str = redis.get(redis_key)
            if not redis_value:
                raise TokenExpiredException
            try:
                info: Dict = orjson.loads(redis_value)
                request.user = CurrentUser(**info)
                # 刷新有效期
                redis.expire(redis_key, time=timedelta(minutes=settings.TOKEN_EXPIRED_MINUTES))
                return request.user
            except Exception as exc:
                logger.error("从redis加载用户失败， 失败信息: " + str(exc))
                raise UnAuthorizedException


current_user: "CurrentUser" = LocalProxy(load_user)  # type: ignore
