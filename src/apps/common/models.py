from sqlalchemy import Column, BigInteger, Integer, String

from src.core.db.model import DeclarativeModel


class File(DeclarativeModel):
    __tablename__ = "file"

    id = Column("id", BigInteger, autoincrement=True, index=True, primary_key=True, comment="主键")
    size = Column("size", Integer, nullable=False, comment="文件大小")
    key = Column("key", String(150), nullable=False, comment="文件存储路径")
    filename = Column("filename", String(64), nullable=False, comment="文件名")
    content_type = Column("content_type", String(32), comment="文件类型")
    upload_time = Column("upload_time", BigInteger, comment="上传日期")
