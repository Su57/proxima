from abc import ABC, abstractmethod
from datetime import datetime
from datetime import timedelta
from typing import Set, Optional, Final

from redis import Redis
from sqlalchemy.engine import Result
from sqlalchemy.sql import select, distinct

from settings import settings
from src.apps.common.schemas import BearerToken
from src.apps.manage.models import User, Authority, user_role, role_auth
from src.apps.manage.repository import UserRepository
from src.common.constant import Constant
from src.core.web.schemas import CurrentUser
from src.exceptions import ProximaException, InvalidAccountException
from src.utils import StringUtil, SecurityUtil


class AuthService(ABC):

    @abstractmethod
    def authenticate(self, email: str, password: str) -> BearerToken:
        """
        登录校验
        :param email: 用户邮箱
        :param password: 密码
        :return: 签发的身份令牌
        """
        raise NotImplemented


class AuthServiceImpl(AuthService):

    def __init__(self, redis: Redis, repository: UserRepository) -> None:
        self.redis: Final[Redis] = redis
        self.repository: Final[UserRepository] = repository

    def authenticate(self, email: str, password: str) -> BearerToken:
        user: Optional[User] = self.repository.get_user_by_email(email)
        if user is None or not SecurityUtil.verify_password(password, user.password):
            raise ProximaException(description="用户名或密码错误")

        if user.status == 1:
            raise InvalidAccountException

        stmt = select(distinct(Authority.code)) \
            .select_from(Authority) \
            .join(role_auth, Authority.id == role_auth.c.auth_id) \
            .join(user_role, user_role.c.role_id == role_auth.c.role_id) \
            .join(User, User.id == user_role.c.user_id).where(User.email == email)
        result: Result = self.repository.execute_query(stmt)
        authorities: Set[str] = {res[0] for res in result.fetchall()}

        # 用户id是1的是超级用户
        is_super: bool = True if user.id == 1 else False

        current_user: CurrentUser = CurrentUser(
            id=user.id,
            last_login=datetime.utcnow(),
            username=user.username,
            authorities=authorities,
            is_super=is_super
        )
        uid: str = StringUtil.get_unique_key()
        expire: timedelta = timedelta(minutes=settings.TOKEN_EXPIRED_MINUTES)
        self.redis.set(name=Constant.AUTH_REDIS_KEY + uid, value=current_user.json(), ex=expire)
        token: str = SecurityUtil.create_token(subject=uid)
        return BearerToken(access_token=token, token_type=Constant.TOKEN_SCHEMA)
