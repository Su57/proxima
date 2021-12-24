from datetime import datetime
from typing import Optional, List, Any, Set, TypeVar, Generic

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar('T')


class Page(GenericModel, Generic[T]):
    """ 分页结果 """
    # 结果总数
    total: int = 0
    # 当前页
    current: int = 1
    # 每页条目
    size: int = 10
    # 总页数
    pages: int = 0
    # 当前页数据集
    records: List[T] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class CurrentUser(BaseModel):
    """ 当前用户信息(仅必要部分) """

    id: int

    username: str

    is_super: bool = False

    # 该用户所有可用的按钮树结构
    authorities: Set[str]

    # 最后登录时间
    last_login: datetime = datetime.utcnow()


class TreeSchema(BaseModel):
    """ 具有树结构特征的schema """
    id: Any
    name: str = Field(alias="label")
    parent_id: Any
    children: Optional[List['TreeSchema']] = []
    disabled: Optional[bool] = False

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class TokenPayload(BaseModel):
    sub: Optional[Any] = None


TreeSchema.update_forward_refs()
