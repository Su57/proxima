from sqlalchemy import Column, BigInteger, Integer, String

from src.core.db.model import DeclarativeModel


class File(DeclarativeModel):
    __tablename__ = "file"

    size = Column("size", Integer, nullable=False, comment="文件大小")
    key = Column("key", String(150), nullable=False, comment="文件存储路径")
    filename = Column("filename", String(64), nullable=False, comment="文件名")
    content_type = Column("content_type", String(32), comment="文件类型")
    upload_time = Column("upload_time", BigInteger, comment="上传日期")


__all__ = ["File"]
