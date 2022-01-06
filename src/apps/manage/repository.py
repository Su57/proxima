from typing import Optional, Sequence, Dict, List, Final

from sqlalchemy import insert, or_, delete, update
from sqlalchemy import select, func
from sqlalchemy.engine import Result

from src.apps.manage.models import User, Role, Authority, UserRoleRel, RoleAuthRel
from src.core.repository import Repository


class UserRepository(Repository[User]):

    entity_class = Final[User]

    def add_user(self, user: User, roles: Sequence[int] = None) -> None:
        """
        添加用户
        :param user: 待添加实体
        :param roles: 角色id列表
        :return:
        """
        with self.session_context as session:
            session.add(user)
            session.flush()
            if roles is not None and len(roles) > 0:
                entities = [{"user_id": user.id, "role_id": role_id} for role_id in roles]
                session.execute(insert(UserRoleRel), entities)
            # 保存用户
            session.commit()

    def update_user(self, ident: int, data: Dict, roles: Sequence[int] = None) -> None:
        """
        更新用户
        :param ident: 待更新用户id
        :param data: 需要变更的内容
        :param roles: 角色id列表
        :return:
        """
        with self.session_context as session:
            # 先解除原有角色绑定
            session.execute(delete(UserRoleRel).where(UserRoleRel.user_id == ident))
            # 再新增绑定
            if roles is not None and len(roles) > 0:
                entities = [{"user_id": ident, "role_id": role_id} for role_id in roles]
                session.execute(insert(UserRoleRel), entities)
            # 最后更新用户
            session.execute(update(User).where(User.id == ident).values(**data))
            # 提交事务
            session.commit()

    def delete_user(self, ident: int) -> None:
        """
        删除用户
        :param ident: 待删除用户id
        :return:
        """
        with self.session_context as session:
            # 先解除所有角色关联
            session.execute(delete(UserRoleRel).where(UserRoleRel.user_id == ident))
            # 再删除用户
            session.execute(delete(User).where(User.id == ident))
            session.commit()

    def get_user_by_email(self, email: str) -> Optional[User]:
        """
        根据邮箱地址获取用户信息(可能为空)
        :param email: 邮箱地址
        :return: 用户信息
        """
        with self.session_context as session:
            return session.execute(select(User).where(User.email == email)).scalar_one_or_none()

    def get_by_username_or_email(self, username: str, email: str) -> List[User]:
        """
        通过用户名或邮箱检索用户
        :param username: 用户名
        :param email: 邮箱
        :return:
        """
        with self.session_context as session:
            stmt = select(User).where(or_(User.username == username, User.email == email))
            result = session.execute(stmt)
            return result.scalars().all()


class RoleRepository(Repository[Role]):
    entity_class = Final[Role]

    def add_role(self, role: Role, authorities: Sequence[int] = None) -> None:
        """
        添加角色信息
        :param role: 角色对象
        :param authorities: 顺带保存的权限id
        :return:
        """
        with self.session_context as session:
            session.add(role)
            session.flush()
            # 保存角色的权限信息
            if authorities is not None and len(authorities) > 0:
                entities = [{"role_id": role.id, "auth_id": auth} for auth in authorities]
                session.execute(insert(RoleAuthRel), entities)
            session.commit()

    def update_role(self, ident: int, data: Dict, authorities: Sequence[int] = None) -> None:
        """
        更新角色，并顺带更新权限
        :param ident: 待更新角色id
        :param data: 更新数据
        :param authorities: 新的全新啊id
        :return:
        """
        with self.session_context as session:
            # 删除所有权限绑定并重新绑定权限
            if authorities is not None:
                session.execute(delete(RoleAuthRel).where(RoleAuthRel.role_id == ident))
                session.execute(insert(RoleAuthRel), [{"role_id": ident, "auth_id": auth} for auth in authorities])
            # 更新角色信息
            session.execute(update(Role).where(Role.id == ident).values(**data))

            session.commit()

    def delete_role(self, ident) -> None:
        with self.session_context as session:
            # 删除所有权限关联
            session.execute(delete(RoleAuthRel).where(RoleAuthRel.role_id == ident))
            # 删除所有用户关联
            session.execute(delete(UserRoleRel).where(UserRoleRel.role_id == ident))
            # 删除角色本体
            session.execute(delete(Role).where(Role.id == ident))
            session.commit()

    def get_user_count_by_role(self, role_id: int):
        """
        获取某角色对应人数
        :param role_id:
        :return:
        """
        with self.session_context as session:
            count_stmt = select(func.count(UserRoleRel.user_id)).where(UserRoleRel.role_id == role_id)
            count: int = session.execute(count_stmt).scalar()
            return count

    def get_count_by_name(self, name: str) -> int:
        """
        通过用户名和邮箱检索用户
        :param name: 用户名
        :return:
        """
        with self.session_context as session:
            count_stmt = select(func.count("*")).where(Role.name == name)
            count: int = session.execute(count_stmt).scalar()
            return count


class AuthorityRepository(Repository[Authority]):
    entity_class = Final[Authority]

    def get_authorities_by_role(self, role_id: int) -> List[int]:
        """
        通过角色id获取该角色对应的权限
        :param role_id:
        :return:
        """
        with self.session_context as session:
            stmt = select(RoleAuthRel.auth_id).where(RoleAuthRel.role_id == role_id)
            res: Result = session.execute(stmt)
            return res.scalars().all()

    def get_role_count_by_authority(self, ident) -> int:
        with self.session_context as session:
            # 检测是否有用户依赖该角色
            count_stmt = select(func.count(RoleAuthRel.role_id)).where(RoleAuthRel.auth_id == ident)
            count: int = session.execute(count_stmt).scalar()
            return count


class UserRoleRelRepository(Repository[UserRoleRel]):
    """ 用户-角色关联对象repo """
    entity_class = UserRoleRel


class RoleAuthRelRepository(Repository[RoleAuthRel]):
    """ 角色-权限关联对象repo """
    entity_class = RoleAuthRel


__all__ = [
    "UserRepository",
    "RoleRepository",
    "AuthorityRepository",
    "UserRoleRelRepository",
    "RoleAuthRelRepository"
]
