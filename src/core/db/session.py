from typing import Final, Optional

from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session


class SessionFactory:
    """ Session工厂 """

    def __init__(self, dsn: str) -> None:
        self._engine: Final[Engine] = create_engine(dsn, future=True, echo=True)
        self._scoped_session: Final[scoped_session] = scoped_session(
            sessionmaker(
                class_=Session,
                autoflush=False,
                autocommit=False,
                bind=self._engine,
                expire_on_commit=False
            )
        )

    def get_session(self) -> Session:
        """ 根据engine获取session """
        return self._scoped_session()


class SessionContext:

    """ sql session 上下文管理器 """

    def __init__(self, factory: SessionFactory):
        self.session: Optional[Session] = None
        self.factory: Final[SessionFactory] = factory

    def __enter__(self) -> Session:
        """ 创建数据库会话 """
        self.session = self.factory.get_session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """ 关闭session，并对发生错误的情况下进行事务回滚 """
        if self.session is not None:
            if exc_type is not None:
                self.session.rollback()
            self.session.close()
