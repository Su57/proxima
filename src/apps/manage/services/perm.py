from abc import abstractmethod
from typing import List, MutableSequence, Dict, Any

from src.apps.manage.models import Authority
from src.apps.manage.repository import AuthorityRepository
from src.core.service import IService, ServiceImpl
from src.core.web.schemas import TreeSchema
from src.exceptions import ProximaException
from src.utils import TreeUtil


class AuthorityService(IService):

    @abstractmethod
    def build_authority_tree(self, authorities: MutableSequence[Authority]) -> List[Dict[str, Any]]:
        """
        根据列表构建树结构
        :param authorities:
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def get_authorities_by_role(self, ident: int) -> List[int]:
        """
        获取某角色所有的权限id
        :param ident: 角色id
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def delete_authority(self, ident: int) -> None:
        """
        删除权限
        @param ident:
        @return:
        """
        raise NotImplemented


class AuthorityServiceImpl(ServiceImpl[AuthorityRepository, Authority], AuthorityService):

    def build_authority_tree(self, authorities: List[Authority]) -> List[Dict[str, str]]:
        return TreeUtil.build_tree([TreeSchema.from_orm(authority) for authority in authorities])

    def get_authorities_by_role(self, ident: int) -> List[int]:
        return self.repository.get_authorities_by_role(ident)

    def delete_authority(self, ident: int) -> None:
        # 检测是否有用户依赖该角色
        count: int = self.repository.get_role_count_by_authority(ident)
        if count > 0:
            raise ProximaException(description="角色删除失败, 有用户依赖于该角色")
        # 删除权限本体
        self.repository.delete(ident)
