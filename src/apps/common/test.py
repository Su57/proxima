from unittest import TestCase, main
from unittest.mock import Mock, MagicMock, patch

from settings import settings
from src.apps.common.models import File
from src.apps.manage.models import User
from src.apps.common.repository import FileRepository
from src.apps.manage.repository import UserRepository
from src.core.db.session import SessionFactory, Session
from src.apps.common.services.auth import AuthServiceImpl
from src.exceptions import ProximaException, InvalidAccountException
from src.apps.common.services.file import LocalFileService, FileStorage


class FileRepositoryTestCase(TestCase):

    def setUp(self) -> None:
        session_factory = SessionFactory(settings.SQLALCHEMY_DATABASE_URI)
        self.repository = FileRepository(session_factory=session_factory)

    @patch.object(Session, "commit")
    @patch.object(Session, "add")
    def test_save(self, mock_add: MagicMock, mock_commit: MagicMock):
        """
        测试 repository的保存功能
         - 测试是否成功调用了session的add和commit方法
         - 测试返回值是否和被保存对象的id一致
        """
        file: File = File()
        file.id = 1
        res: int = self.repository.save(file)
        mock_add.assert_called_once_with(file)
        mock_commit.assert_called_once()
        self.assertEqual(res, 1)


class LocalFileServiceTestCase(TestCase):

    @patch.object(FileStorage, "save")
    def test_upload(self, mock_file_storage_save: MagicMock):
        """
        测试上传
         - 测试是否正确保存了文件
         - 测试是否正确调用了repository的save()方法
         - 返回值是否正确
        """
        file_storage = FileStorage(name="Test FileStorage", filename="Test Filename")
        mock_repository: Mock = Mock(spec=FileRepository)
        service = LocalFileService(repository=mock_repository)

        result = service.upload(file_storage)

        # 测试是否执行了文件系统保存
        mock_file_storage_save.assert_called_once()
        # 测试是否执行了数据库操作
        mock_repository.save.assert_called_once()
        self.assertEqual(result.filename, "Test Filename")


class AuthServiceTestCase(TestCase):

    def test_authenticate(self):
        """
        测试用户身份校验
         - 测试是否正确调用了repository和redis
         - 测试返回对象
         - 测试邮箱不存在、密码错误、账号禁用时的异常
        :return:
        """
        email = "some_email@example.cn"
        password = "pbkdf2:sha256" \
                   ":260000$ZYmljS6Ts2eedfh0$75c286ad17b37c1dd9d428280fd22cfb474575f5d30c9892915597449b8fff8b"

        # 准备mock对象
        mock_redis = Mock()
        mock_query_result = Mock()
        mock_query_result.fetchall.return_value = ["some authority"]
        repository = Mock(spec=UserRepository)

        # 准备数据
        user = User()
        user.id = 1
        user.username = "admin"
        user.email = email
        user.password = password

        # 设置mock行为
        repository.get_user_by_email.return_value = user
        repository.execute_query.return_value = mock_query_result
        service = AuthServiceImpl(mock_redis, repository)

        # 调用接口
        token = service.authenticate(email, "123456")

        # 检测断言
        repository.get_user_by_email.assert_called_once_with(email)
        repository.execute_query.assert_called_once()
        mock_redis.set.assert_called_once()
        self.assertEqual(token.token_type, "Bearer")

        # 密码不正确时会抛出异常
        self.assertRaises(ProximaException, service.authenticate, email, 'some_not_matched_password')

        # 用户不可用时会抛出异常
        user.status = 1
        self.assertRaises(InvalidAccountException, service.authenticate, email, 'some_password')

        # 没有该用户时抛出异常
        repository.get_user_by_email.return_value = None
        self.assertRaises(ProximaException, service.authenticate, 'not_really_exists_email', 'some_password')


if __name__ == '__main__':
    main()
