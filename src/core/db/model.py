from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class DeclarativeModel:
    """ 全局ORM基类 """
