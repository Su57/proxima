from abc import ABC, abstractmethod
from typing import List, Optional, Union, Generic, Dict, Sequence, TypeVar, Final

from pydantic import BaseModel

from src.core.web.schemas import Page
from src.core.repository import Repository
from src.core.db.model import DeclarativeModel

M = TypeVar("M", bound=Repository)
T = TypeVar("T", bound=DeclarativeModel)
DataSchema = TypeVar("DataSchema", bound=BaseModel)


class IService(ABC):
    """
    增删改查接口类
    """

    @abstractmethod
    def save(self, entity: Union[T, DataSchema]) -> None:
        """
        新增数据
        :param entity: 新增时提交的数据
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def get_by_id(self, ident: int) -> Optional[T]:
        """
        根据主键获取数据库对象
        :param ident: 主键值
        :return: orm映射对象
        """
        raise NotImplemented

    @abstractmethod
    def get_by_ids(self, idents: Sequence[int]) -> List[T]:
        """
        根据主键获取数据库对象
        :param idents: 主键序列
        :return: orm映射对象列表
        """
        raise NotImplemented

    @abstractmethod
    def get_by_map(self, params: Dict[str, int] = None) -> List[T]:
        """
        根据主键获取数据库对象
        :param params: 查询条件，应用于SQL WHERE语句
        :return: orm映射对象列表
        """
        raise NotImplemented

    @abstractmethod
    def get_page(self, current: Optional[int] = 1, size: Optional[int] = 10) -> Page[T]:
        """
        获取分页数据
        :param current: 目标页
        :param size: 每页数据条数
        :return: 分页结果
        """
        raise NotImplemented

    @abstractmethod
    def update(self, ident: int, schema: DataSchema) -> None:
        """
        更新对象
        :param ident: 待更新对象主键值
        :param schema: 更新时提交的数据
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def delete(self, ident: int) -> None:
        """
        根据主键删除对象
        :param ident: 主键值
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def batch_insert(self, mappings: Sequence[DataSchema]) -> None:
        """
        批量保存
        :param mappings: 待保存的对象
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def batch_update(self, mappings: Sequence[DataSchema]) -> None:
        """
        批量更新
        :param mappings: 待更新列表。每个元素都必须包含id键，为了让sqlalchemy可以更具id进行属性更新
        :return:
        """
        raise NotImplemented

    @abstractmethod
    def batch_delete(self, idents: Sequence[int]) -> None:
        """
        批量删除
        :param idents: 待删除对象主键序列
        :return:
        """
        raise NotImplemented


class ServiceImpl(Generic[M, T], ABC):

    def __init__(self, repository: M):
        self.repository: Final[M] = repository

    def save(self, entity: Union[T, DataSchema]) -> None:
        """

        :param entity: 新增时提交的数据
        :return:
        """
        return self.repository.save(entity)

    def get_by_id(self, ident: int) -> Optional[T]:
        """
        根据主键获取数据库对象
        
        :param ident: 主键值
        :return: orm映射对象
        """
        return self.repository.get_by_id(ident)

    def get_by_ids(self, ident_list: Sequence[int]) -> List[T]:
        """
        根据主键获取数据库对象
        
        :param ident_list: 主键序列
        :return: orm映射对象列表
        """
        return self.repository.get_by_ids(ident_list)

    def get_by_map(self, params: Dict[str, int] = None) -> List[T]:
        """
        根据主键获取数据库对象
        
        :param params: 查询条件，应用于SQL WHERE语句
        :return: orm映射对象的集合
        """
        return self.repository.get_by_map(params)

    def get_page(self, current: Optional[int] = 1, size: Optional[int] = 10) -> Page[T]:
        """
        获取分页数据
        
        :param current: 目标页
        :param size: 每页数据条数
        :return: 分页结果
        """
        return self.repository.get_page(current=current, size=size)

    def update(self, ident: int, schema: DataSchema) -> None:
        """
        更新对象 不要使用SQLAlchemy ORM更新策略(查询对象 -> 修改对象字段 -> 提交变更)
        可以直接采取数据库UPDATE操作。可能失败，需要重试

        :param ident: 待更新对象主键值
        :param schema: 更新时提交的数据
        :return:
        """
        self.repository.update(ident, schema)

    def delete(self, ident: int) -> None:
        """
        根据主键删除对象
        :param ident: 主键值
        :return:
        """
        self.repository.delete(ident)

    def batch_insert(self, mappings: Sequence[DataSchema]) -> None:
        """
        批量保存
        :param mappings: 待保存的对象
        :return:
        """
        self.repository.batch_insert(mappings)

    def batch_update(self, mappings: Sequence[DataSchema]) -> None:
        """
        批量更新
        :param mappings: 待更新列表。每个元素都必须包含id键，为了让sqlalchemy可以更具id进行属性更新
        :return:
        """
        self.repository.batch_update(mappings)

    def batch_delete(self, idents: Sequence[int]) -> None:
        """
        批量删除
        :param idents: 待删除对象主键序列
        :return: 删除条目数
        """
        self.repository.batch_delete(idents)


__all__ = ["IService", "ServiceImpl"]
