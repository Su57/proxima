import os
import pathlib
from abc import abstractmethod
from datetime import date

from werkzeug.datastructures import FileStorage
from pydantic_sqlalchemy import sqlalchemy_to_pydantic
from settings import settings
from src.apps.common.models import File
from src.apps.common.repository import FileRepository
from src.apps.common.schemas import FileViewSchema
from src.core.service import IService, ServiceImpl
from src.utils import StringUtil


class FileService(IService):
    """ 文件服务(上传、下载、移除) """

    @abstractmethod
    def upload(self, file_storage: FileStorage) -> FileViewSchema:
        """
        上传文件 - 适用于简单上传到本地文件系统
        :param file_storage: 文件对象
        :return: 文件URL
        """
        raise NotImplemented


class LocalFileService(ServiceImpl[FileRepository, File], FileService):

    def upload(self, file_storage: FileStorage) -> FileViewSchema:
        key: str = self._create_key_by_filename(file_storage.filename)
        path = pathlib.Path(settings.BASE_DIR, settings.UPLOAD_DIR, key)

        # 目录不存在时需要创建
        if not path.parent.exists():
            os.makedirs(path.parent)

        try:
            file_storage.save(path)
            file: File = File()
            file.key = key
            file.filename = file_storage.filename
            file.size = file_storage.content_length
            file.content_type = file_storage.content_type
            file_id = self.repository.save(file)
            return FileViewSchema(
                id=file_id,
                size=file_storage.content_length,
                filename=file_storage.filename,
                url=settings.UPLOAD_DIR + key
            )
        finally:
            file_storage.close()

    @staticmethod
    def _create_key_by_filename(filename: str) -> str:
        path = pathlib.Path(filename)
        # 解析文件后缀名, 获取文件本地存储路径
        suffix = "".join(path.suffixes)
        return date.today().strftime("%Y/%m/%d") + "/" + StringUtil.get_unique_key() + suffix
