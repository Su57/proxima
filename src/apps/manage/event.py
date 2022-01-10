from typing import Final

from sqlalchemy import insert

from src.apps.manage.models import UserRoleRel
from src.core.db.session import SessionContext
from src.core.event import Event, EventListener


class UserSaveListener(EventListener):

    def __init__(self, session_context: SessionContext):
        self.session_context: Final[SessionContext] = session_context

    def __call__(self, user_id: int, **extra):
        """ 针对新增用户执行的操作 """
        # 保存用户的角色
        roles = extra.pop("roles")
        with self.session_context as session:
            print("保存角色信息")
            session.execute(insert(UserRoleRel), [{"user_id": user_id, "role_id": role_id} for role_id in roles])
            session.commit()


class UserSaveEvent(Event):
    ...


class UserUpdateEvent(Event):
    ...


class UserDeleteEvent(Event):
    ...
