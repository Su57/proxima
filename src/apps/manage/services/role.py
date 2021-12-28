from abc import abstractmethod

from src.apps.manage.models import Role
from src.apps.manage.repository import RoleRepository
from src.apps.manage.schemas import RoleCreateSchema, RoleUpdateSchema
from src.core.service import IService, ServiceImpl
from src.exceptions import ProximaException


class RoleService(IService):

    @abstractmethod
    def add_role(self, schema: RoleCreateSchema) -> None:
        """
        新增角色

        :param schema: 新增时的数据
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def update_role(self, ident: int, schema: RoleUpdateSchema) -> None:
        """
        更新用户

        :param ident: 待更新对象的id
        :param schema:  更新的数据
        :return: 更新后的角色
        """
        raise NotImplemented

    @abstractmethod
    def delete_role(self, ident: int) -> None:
        """
        删除角色

        :param ident: 角色id
        :return:
        """
        raise NotImplemented


class RoleServiceImpl(ServiceImpl[RoleRepository, Role], RoleService):

    def add_role(self, schema: RoleCreateSchema) -> None:
        count: int = self.repository.get_count_by_name(schema.name)
        if count > 0:
            raise ProximaException(description="角色名已存在")
        role: Role = Role()
        role.name = schema.name
        if schema.remark:
            role.remark = schema.remark
        if schema.status:
            role.status = schema.status
        self.repository.add_role(role, schema.authorities)

    def update_role(self, ident: int, schema: RoleUpdateSchema) -> None:
        count: int = self.repository.get_count_by_name(schema.name)
        if count > 0:
            raise ProximaException(description="角色名已存在")
        data = schema.dict(exclude_unset=True)
        authorities = data.pop("authorities", None)
        self.repository.update_role(ident, data, authorities)

    def delete_role(self, ident: int) -> None:
        count: int = self.repository.get_user_count_by_role(ident)
        if count > 0:
            raise ProximaException(description="角色删除失败, 有用户依赖于该角色")
        # 删除角色何其所有关联权限
        self.repository.delete_role(ident)
