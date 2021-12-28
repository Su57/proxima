from abc import abstractmethod
from typing import List, Optional

from src.apps.manage.models import User
from src.apps.manage.repository import UserRepository
from src.apps.manage.schemas import UserCreateSchema, UserUpdateSchema, UserViewSchema
from src.core.service import IService, ServiceImpl
from src.core.web.schemas import Page
from src.exceptions import ProximaException
from src.utils import SecurityUtil


class UserService(IService):
    """ 用户相关业务逻辑 """

    @abstractmethod
    def get_user_list(self, current: Optional[int] = 1, size: Optional[int] = 10) -> Page[UserViewSchema]:
        """
        获取用户列表(可分页)

        :param current: 页码 默认1
        :param size: 每页数量 默认10
        :return: 分页数据
        """
        raise NotImplemented

    @abstractmethod
    def add_user(self, schema: UserCreateSchema) -> None:
        """
        新增用户

        :param schema: 新增时的数据
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def update_user(self, ident: int, schema: UserUpdateSchema) -> None:
        """
        更新用户

        :param ident: 待更新对象的id
        :param schema:  更新的数据
        :return: 更新后的对象
        """
        raise NotImplemented

    @abstractmethod
    def delete_user(self, ident: int) -> None:
        """
        根据id删除用户

        :param ident: 用户id
        :return:
        """
        raise NotImplemented


class UserServiceImpl(ServiceImpl[UserRepository, User], UserService):

    def get_user_list(self, current: Optional[int] = 1, size: Optional[int] = 10) -> Page[UserViewSchema]:
        """
        获取用户列表(可分页)

        :param current: 页码
        :param size: 每页数量
        :return: 分页数据
        """
        _res: Page[User] = self.repository.get_page(current, size)
        result: Page[UserViewSchema] = Page(total=_res.total, current=_res.current, size=_res.size, pages=_res.pages)
        result.records = [UserViewSchema.from_orm(obj) for obj in _res.records]
        return result

    def add_user(self, schema: UserCreateSchema) -> None:
        """
        新增用户

        :param schema: 新增时的数据
        :return:
        """
        self._check_available(schema.username, schema.email)
        user: User = User()
        user.username = schema.username
        user.nickname = schema.nickname
        user.email = schema.email
        user.mobile = schema.mobile
        user.avatar = schema.avatar
        user.password = SecurityUtil.generate_password(schema.password)
        self.repository.add_user(user, schema.roles)

    def update_user(self, ident: int, schema: UserUpdateSchema) -> None:
        """
        更新用户

        :param ident: 待更新对象的id
        :param schema:  更新的数据
        :return: 更新后的对象
        """
        self._check_available(schema.username, schema.email)
        data = schema.dict(exclude_unset=True)
        roles = data.pop("roles")
        self.repository.update_user(ident=ident, data=data, roles=roles)

    def delete_user(self, ident: int) -> None:
        """
        根据id删除用户

        :param ident: 用户id
        :return:
        """
        self.repository.delete_user(ident)

    def _check_available(self, username: str, email: str, ident: Optional[int] = -1) -> None:
        """
        检查用户名或者邮箱是否可用
        @param username: 用户名
        @param email: 邮箱
        @param ident: 用户id，新增用户检测时可不填
        @return: 用户名和邮箱是否可用
        """
        username_available = True
        email_available = True
        users: List[User] = self.repository.get_by_username_or_email(username, email)
        for user in users:
            if user.id != ident:
                if user.username == username:
                    username_available = False
                if user.email == email:
                    email_available = False
        msg: List[str] = []
        if not username_available:
            msg.append("用户名已存在")
        if not email_available:
            msg.append("邮箱已存在")
        if len(msg) > 0:
            raise ProximaException(description=",".join(msg))
