from math import ceil
from typing import List, Optional, Union, Generic, Dict, Sequence, TypeVar, Any, Final

from pydantic import BaseModel
from sqlalchemy.engine.cursor import Result
from sqlalchemy.sql import update, Update, delete, Delete, insert, Insert, select, Select, func

from src.core.db.model import DeclarativeModel
from src.core.db.session import SessionContext
from src.core.web.schemas import Page

T = TypeVar("T", bound=DeclarativeModel)
DataSchema = TypeVar("DataSchema", bound=BaseModel)


class Repository(Generic[T]):
    entity_class: T

    def __init__(self, session_context: SessionContext):
        self.session_context: Final[SessionContext] = session_context

    def execute_query(self, stmt: Select) -> Result:
        with self.session_context as session:
            return session.execute(stmt)

    def save(self, entity: Union[T, DataSchema]) -> None:
        """
        新增数据

        :param entity: 新增时提交的数据
        :return:  
        """
        with self.session_context as session:
            if isinstance(entity, DeclarativeModel):
                session.add(entity)
            else:
                stmt: Insert = insert(self.entity_class).values(**entity.dict(exclude_none=True))
                session.execute(stmt)
            session.commit()

    def get_by_id(self, ident: int) -> Optional[T]:
        """
        根据主键获取数据库对象

        :param ident: 主键值
        :return: orm映射对象
        """
        with self.session_context as session:
            return session.get(self.entity_class, ident=ident)

    def get_by_ids(self, ident_list: Sequence[int]) -> List[T]:
        """
        根据主键获取数据库对象

        :param ident_list: 主键序列
        :return: orm映射对象
        """
        with self.session_context as session:
            stmt: Select = select(self.entity_class).where(self.entity_class.id.in_(ident_list))
            result: Result = session.execute(stmt)
            return result.scalars().all()

    def get_by_map(self, params: Dict[str, Any] = None) -> List[T]:
        """
        根据主键获取数据库对象

        :param params: 查询条件，应用于SQL WHERE语句
        :return: orm映射对象的集合
        """
        with self.session_context as session:
            if params is None or len(params) == 0:
                return session.execute(select(self.entity_class).distinct()).scalars().all()
            return session.execute(select(self.entity_class).distinct().filter_by(**params)).scalars().all()

    def get_page(self, current: int, size: int, params: Optional[Dict] = None) -> Page[T]:
        """
        获取分页数据 TODO 页码超出上限时的处理逻辑
        :param current: 请求的页码
        :param size: 请求的条数
        :param params: 请求的额外参数
        :return:
        """
        with self.session_context as session:

            stmt: Select = select(self.entity_class).distinct()
            if params is not None:
                stmt.filter_by(**params)
            total: int = session.execute(select(func.count("*")).select_from(stmt)).scalar()
            records: List[T] = []
            if total > 0:
                records = session.execute(stmt.slice((current - 1) * size, current * size)).scalars().all()
            page: Page = Page(current=current, size=size, total=total, pages=ceil(total / size), records=records)
            return page

    def update(self, ident: int, schema: DataSchema) -> None:
        """
        根据主键更新对象

        :param ident: 待更新对象主键值
        :param schema: 更新时提交的数据
        :return:
        """
        with self.session_context as session:
            update_data = schema.dict(exclude_unset=True)
            stmt: Update = update(self.entity_class).where(self.entity_class.id == ident).values(**update_data)
            session.execute(stmt)
            session.commit()

    def delete(self, ident: int) -> None:
        """
        根据主键删除对象
        :param ident: 主键值
        :return:
        """
        with self.session_context as session:
            stmt: Delete = delete(self.entity_class).where(self.entity_class.id == ident)
            session.execute(stmt)
            session.commit()

    def batch_insert(self, schemas: Sequence[DataSchema]) -> None:
        """
        批量保存
        :param schemas: 待保存的对象
        :return:
        """
        with self.session_context as session:
            mappings = [schema.dict(exclude_none=True) for schema in schemas]
            session.bulk_insert_mappings(self.entity_class, mappings=mappings)

    def batch_update(self, schemas: Sequence[DataSchema]) -> None:
        """
        批量更新
        :param schemas: 待更新列表。每个元素都必须包含id键，为了让sqlalchemy可以更具id进行属性更新
        :return:
        """
        with self.session_context as session:
            mappings = [schema.dict(exclude_unset=True) for schema in schemas]
            session.bulk_update_mappings(self.entity_class, mappings=mappings)
            session.commit()

    def batch_delete(self, idents: Sequence[int]) -> None:
        """
        批量删除
        :param idents: 待删除对象主键序列
        :return:
        """
        with self.session_context as session:
            stmt: Delete = delete(self.entity_class).where(self.entity_class.id.in_(idents))
            session.execute(stmt)
            session.commit()
