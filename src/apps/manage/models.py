from sqlalchemy import Column, String, Integer, BigInteger, SmallInteger, ForeignKey, UniqueConstraint

from src.utils import DateUtil
from src.common.enums import Status, Gender
from src.core.db.model import DeclarativeModel


class UserRoleRel(DeclarativeModel):
    """ 用户-角色 关联表 """
    __tablename__ = "user_role_rel"
    user_id = Column("user_id", BigInteger, index=True, nullable=False, comment="用户id")
    role_id = Column("role_id", BigInteger, index=True, nullable=False, comment="角色id")

    __table_args__ = (UniqueConstraint('user_id', 'role_id', name='uq_user_role_id'),)


class RoleAuthRel(DeclarativeModel):
    """ 角色-权限 关联表 """
    __tablename__ = "role_auth_rel"
    role_id = Column("role_id", BigInteger, index=True, nullable=False, comment="角色id")
    auth_id = Column("auth_id", BigInteger, index=True, nullable=False, comment="权限id")

    __table_args__ = (UniqueConstraint('role_id', 'auth_id', name='uq_role_auth_id'),)


class User(DeclarativeModel):
    """ 系统用户表 """
    __tablename__ = "user"
    username = Column(String(50), nullable=False, comment="用户名")
    nickname = Column(String(50), nullable=False, default="", comment="昵称")
    email = Column(String(120), unique=True, nullable=False, index=True, comment="邮箱")
    mobile = Column(String(11), unique=True, nullable=False, default="", comment="手机号")
    gender = Column(SmallInteger, nullable=False, default=Gender.unknown.value, comment="性别， 0：男， 1：女")
    avatar = Column(String(64), nullable=True, comment='头像URL')
    password = Column(String(128), nullable=False, comment="密码")
    status = Column(SmallInteger, nullable=False, default=Status.enable.value, comment="用户状态，0正常 1禁用或停用")
    remark = Column(String(50), nullable=False, default="", comment="备注")
    created = Column("created", BigInteger, nullable=False, default=DateUtil.timestamp, comment="创建时间(时间戳，精确到秒)")
    updated = Column("updated", BigInteger, nullable=True, onupdate=DateUtil.timestamp, comment="更新时间(时间戳，精确到秒)")


class Role(DeclarativeModel):
    """ 系统角色 """
    __tablename__ = "role"
    name = Column(String(50), nullable=False, comment="角色名称")
    status = Column(SmallInteger, nullable=False, default=Status.enable.value, comment="角色状态，0正常，1停用")
    remark = Column(String(50), nullable=False, default="", comment="备注")
    created = Column("created", BigInteger, nullable=False, default=DateUtil.timestamp, comment="创建时间(时间戳，精确到秒)")
    updated = Column("updated", BigInteger, nullable=True, onupdate=DateUtil.timestamp, comment="更新时间(时间戳，精确到秒)")


class Authority(DeclarativeModel):
    """ 菜单 / 权限 """
    __tablename__ = "authority"

    name = Column(String(50), nullable=False, comment="名称")
    parent_id = Column(BigInteger, ForeignKey('authority.id'), index=True, comment='父权限id')
    sort = Column(Integer, default=0, nullable=False, comment="显示顺序")
    code = Column(String(100), nullable=False, comment="权限标识")
    remark = Column(String(64), nullable=True, comment="权限")
    created = Column("created", BigInteger, nullable=False, default=DateUtil.timestamp, comment="创建时间(时间戳，精确到秒)")
    updated = Column("updated", BigInteger, nullable=True, onupdate=DateUtil.timestamp, comment="更新时间(时间戳，精确到秒)")


__all__ = {
    "User",
    "Role",
    "Authority",
    "UserRoleRel",
    "RoleAuthRel"
}
