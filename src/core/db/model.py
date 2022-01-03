from sqlalchemy import Column, BigInteger
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class DeclarativeModel:
    """ 全局ORM基类 """
    id = Column("id", BigInteger, autoincrement=True, primary_key=True, comment="主键")
