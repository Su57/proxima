from typing import Optional, List, Union
from pydantic import Field, EmailStr, NonNegativeInt
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from src.common.enums import Gender, Status
from src.apps.manage.models import User, Role, Authority
from src.core.config.serializer import SerializationConfig, BaseSerializationSchema, BaseValidationSchema

# 数据库模型 -> schema
UserModelSchema = sqlalchemy_to_pydantic(db_model=User, config=SerializationConfig, exclude={"password"})

RoleModelSchema = sqlalchemy_to_pydantic(db_model=Role, config=SerializationConfig)

AuthorityModelSchema = sqlalchemy_to_pydantic(db_model=Authority, config=SerializationConfig)


# 用于前端展示的schema
class UserViewSchema(BaseSerializationSchema):
    """
    用于前端展示的用户schema
    """
    id: str
    username: str
    nickname: str
    email: str
    mobile: str
    gender: int
    avatar: Optional[str]
    remark: Optional[str]


class RoleViewSchema(BaseSerializationSchema):
    id: str
    name: str
    remark: Optional[str]


class AuthorityViewSchema(BaseSerializationSchema):
    """ 展示权限Schema """
    id: str
    name: str
    parent_id: Optional[str]
    code: str
    remark: Optional[str]


class _UserValidationSchema(BaseValidationSchema):
    nickname: Optional[str] = Field(None, max_length=50, min_length=4, description="昵称")
    mobile: Optional[str] = Field("", description="用户手机号码")
    gender: Optional[Gender] = Field(Gender.unknown, description="性别 0:未知 1:男 2:女")
    remark: Optional[str] = Field(None, max_length=100, description="账号备注")
    avatar: Optional[str] = Field(None, description="头像URL")
    roles: Optional[List[int]] = Field(None, description="角色id列表")


class UserCreateSchema(_UserValidationSchema):
    """ 创建用户schema """
    email: EmailStr = Field(..., description="用户邮箱")
    username: str = Field(..., max_length=50, min_length=4, description="用户名")
    password: str = Field(..., min_length=6, max_length=20, description="密码")


class UserUpdateSchema(_UserValidationSchema):
    """ 更新用户schema """
    email: Optional[EmailStr] = Field(None, description="用户邮箱")
    username: Optional[str] = Field(None, max_length=50, min_length=4, description="用户名")
    status: Optional[int] = Field(None, description="账号状态")


class _RoleValidationSchema(BaseValidationSchema):
    status: Optional[Status] = Field(Status.enable, description="角色状态，0正常，1停用")
    authorities: Optional[List[int]] = Field(None, description="菜单权限id列表")
    remark: Optional[str] = Field(None, max_length=64, description="角色备注")


class RoleCreateSchema(_RoleValidationSchema):
    """ 创建角色schema """
    name: str = Field(..., max_length=50, description="角色名称")


class RoleUpdateSchema(_RoleValidationSchema):
    name: Optional[str] = Field(None, max_length=50, description="角色名称")


class AuthorityCreateSchema(BaseValidationSchema):
    name: str = Field(..., description="权限名称")
    parent_id: Optional[int] = Field(None, description="父权限id")
    sort: NonNegativeInt = Field(..., description="显示顺序")
    code: str = Field(..., min_length=1, max_length=32, description="权限标识")
    remark: Optional[str] = Field(None, max_length=64, description="权限备注")


class AuthorityUpdateSchema(BaseValidationSchema):
    name: Optional[str] = Field(None, description="权限名称")
    parent_id: Optional[Union[str, int]] = Field(None, description="父权限id")
    sort: Optional[NonNegativeInt] = Field(None, description="显示顺序")
    code: Optional[str] = Field(None, min_length=1, max_length=32, description="权限标识")
    remark: Optional[str] = Field(None, max_length=64, description="权限备注")


class UserRoleSchema(BaseValidationSchema):
    user_id: str
    role_id: str
    created_at: Optional[int]
    updated_at: Optional[int]


AuthorityViewSchema.update_forward_refs()
