from unittest import TestCase, main
from unittest.mock import Mock, MagicMock, patch, ANY

from src.apps.common.models import File
from src.apps.common.repository import FileRepository
from src.apps.common.services.auth import AuthServiceImpl
from src.apps.common.services.auth import Redis
from src.apps.common.services.file import LocalFileService, FileStorage
from src.apps.manage.models import User
from src.apps.manage.repository import UserRepository
from src.common.constant import Constant
from src.core.db.session import SessionContext
from src.exceptions import ProximaException, InvalidAccountException


class FileRepositoryTestCase(TestCase):

    def test_save(self):
        """
        测试 repository的保存功能
         - 测试是否成功调用了session的add和commit方法
         - 测试返回值是否和被保存对象的id一致
        """
        session = Mock()
        session_context = Mock(spec=SessionContext, __enter__=Mock(), __exit__=Mock())
        session_context.__enter__.return_value = session
        repository = FileRepository(session_context=session_context)
        file = File()
        file.id = 1
        repository.save(file)
        session.add.assert_called_once_with(file)
        session.commit.assert_called_once()

        self.assertEqual(file.id, 1)


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
        self.assertRaises(InvalidAccountException, service.authenticate, email, '123456')

        # 没有该用户时抛出异常
        repository.get_user_by_email.return_value = None
        self.assertRaises(ProximaException, service.authenticate, 'not_really_exists_email', ANY)

    def test_logout(self):
        mock_redis = Mock(spec=Redis)
        service = AuthServiceImpl(redis=mock_redis, repository=Mock())
        user_id = 1
        redis_key = Constant.AUTH_REDIS_KEY + str(user_id)

        mock_redis.exists.return_value = True
        service.logout(user_id)
        mock_redis.exists.assert_called_once_with(redis_key)
        mock_redis.delete.assert_called_once_with(redis_key)
        self.assertEqual(mock_redis.exists.call_count, 1)

    def test_logout_not_exists(self):
        mock_redis = Mock(spec=Redis)
        service = AuthServiceImpl(redis=mock_redis, repository=Mock())
        user_id = 1
        redis_key = Constant.AUTH_REDIS_KEY + str(user_id)

        mock_redis.exists.return_value = False
        service.logout(user_id)
        mock_redis.exists.assert_called_once_with(redis_key)
        mock_redis.delete.assert_not_called()
        self.assertEqual(mock_redis.exists.call_count, 1)


if __name__ == '__main__':
    main()
