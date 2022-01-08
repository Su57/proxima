from functools import wraps
from typing import Callable

from src.core.web.request import current_user
from src.core.web.schemas import CurrentUser
from src.exceptions import AccessDeniedException, UnAuthorizedException


def login_required(func: Callable):
    """ 登录校验 """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user or not isinstance(current_user, CurrentUser):
            raise UnAuthorizedException
        return func(*args, **kwargs)

    return wrapper


def permission_required(key: str) -> Callable:
    """ 权限校验 """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # 检查是否登录
            if not current_user or not isinstance(current_user, CurrentUser):
                raise UnAuthorizedException
            # 检查权限
            if key not in current_user.authorities and not current_user.is_super:
                raise AccessDeniedException
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper


def role_required(key: str) -> Callable:
    """ 角色校验 """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # 检查是否登录
            if not current_user or not isinstance(current_user, CurrentUser):
                raise UnAuthorizedException
            # 检查角色
            if key not in current_user.authorities and not current_user.is_super:
                raise AccessDeniedException
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper


def role_or_permission_required(*, role: str = None, perm: str = None) -> Callable:
    """ 角色校验 """

    def wrapper(func):
        @wraps(func)
        def inner_wrapper(*args, **kwargs):
            # 检查是否登录
            if not current_user or not isinstance(current_user, CurrentUser):
                raise UnAuthorizedException
            # 检查角色/权限
            if role is None:
                if (perm is None or perm not in current_user.authorities) and not current_user.is_super:
                    raise AccessDeniedException
            if perm is None:
                if (role is None or role not in current_user.authorities) and not current_user.is_super:
                    raise AccessDeniedException
            return func(*args, **kwargs)

        return inner_wrapper

    return wrapper
