import io
import pathlib
from unittest import TestCase, main
from unittest.mock import Mock, patch

from redis import StrictRedis
from werkzeug.datastructures import FileStorage

from container import Container
from settings import settings
from src.apps.common.repository import FileRepository
from src.apps.common.services import LocalFileService
from test.api_test.base import AppContextMixin


class CommonApiTestCase(AppContextMixin, TestCase):
    """
    测试通用接口(上传、下载、身份认证)
    """

    @patch('src.core.web.request.load_user')
    @patch.object(FileRepository, 'save')
    @patch.object(FileStorage, "save")
    def test_single_upload(self, mock_save: Mock, mock_repository_save: Mock, mock_load_user: Mock):
        """
        测试上传接口 - 单文件上传
        :param mock_save: 模拟的文件保存接口 - 避免每次测试时新增文件
        :param mock_repository_save: 模拟的数据库保存接口 - 避免测试时向数据库插入数据
        :param mock_load_user: 模拟的用户加载函数，保证认证流通
        :return:
        """
        mock_repository_save.return_value = 1
        data = {'file': ("fake-text-stream.txt", io.BytesIO(b"some initial text data"))}

        response = self.client.post('/file/upload', files=data)

        mock_save.assert_called_once()
        mock_repository_save.assert_called_once()
        mock_load_user.assert_called_once()

        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['filename'], "fake-text-stream.txt")
        self.assertEqual(data[0]['id'], 1)

    @patch('src.core.web.request.load_user')
    @patch.object(FileRepository, 'save')
    @patch.object(FileStorage, "save")
    def test_multi_upload(self, mock_save: Mock, mock_repository_save: Mock, mock_load_user: Mock):
        """
        测试上传接口 - 多文件上传
        :param mock_save: 模拟的文件保存接口 - 避免每次测试时新增文件
        :param mock_repository_save: 模拟的数据库保存接口 - 避免测试时向数据库插入数据
        :param mock_load_user: 模拟的用户加载函数，保证认证流通
        :return:
        """
        mock_repository_save.return_value = 1
        data = {
            'file_1': ("fake-text-stream_1.txt", io.BytesIO(b"some initial text data")),
            'file_2': ("fake-text-stream_2.txt", io.BytesIO(b"some initial text data")),
        }

        response = self.client.post('/file/upload', files=data)

        mock_save.assert_called()
        mock_repository_save.assert_called()
        mock_load_user.assert_called_once()

        self.assertEqual(response.status_code, 200)
        data = response.json()['data']
        self.assertEqual(len(data), 2)

        self.assertEqual(data[0]['filename'], "fake-text-stream_1.txt")
        self.assertEqual(data[1]['filename'], "fake-text-stream_2.txt")

    @patch('src.core.web.request.load_user')
    @patch("src.apps.common.routers.file.send_file")
    def test_download(self, mock_send_file: Mock, mock_load_user):
        """
        测试文件下载
        :param mock_send_file: 模拟的文件传输方法
        :param mock_load_user: 模拟的用户加载方法
        :return:
        """
        file_id = 1
        mock_file_service = Mock(spec=LocalFileService)
        mock_file_service.get_by_id.return_value = Mock(
            key="fake-filepath",
            filename="fake-filename.txt",
            content_type="fake-content-type"
        )
        mock_send_file.return_value = ""  # 防止出现返回结果是MagicMock导致的错误
        with self.container.file_service.override(mock_file_service):
            self.client.get("/file/download/{}".format(file_id))
            mock_file_service.get_by_id.assert_called_once_with(file_id)
            mock_load_user.assert_called_once()
            mock_send_file.assert_called_once_with(
                pathlib.Path(settings.BASE_DIR, settings.UPLOAD_DIR, "fake-filepath"),
                as_attachment=True,
                attachment_filename="fake-filename.txt",
                mimetype="fake-content-type"
            )

    @patch('src.core.web.request.load_user')
    def test_delete(self, mock_load_user: Mock):
        """
        测试文件删除
        :param mock_load_user: 模拟的用户加载方法
        :return:
        """
        mock_file_service = Mock(spec=LocalFileService)
        with self.container.file_service.override(mock_file_service):
            response = self.client.delete("/file/delete/1")
            mock_load_user.assert_called_once()
            mock_file_service.delete.assert_called_once_with(1)

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["code"], 0)

    def test_authenticate(self):
        """
        测试登录接口
        :return:
        """
        payload = {
            "email": "admin@123.cn",
            "password": "123456"
        }
        mock_redis = Mock(spec=StrictRedis)
        container: Container = getattr(self.app, "container")
        self.assertIsNotNone(container)
        with container.redis.override(mock_redis):
            # 模拟正确请求
            response = self.client.post('/login', json=payload)
            self.assertEqual(response.status_code, 200)
            mock_redis.set.assert_called_once()
            self.assertEqual(response.json()["data"]['token_type'], "Bearer")

            # 模拟错误请求
            payload["password"] = "some_fake_password"
            response = self.client.post("/login", json=payload)
            self.assertEqual(response.json()["code"], 1)
            self.assertIsNone(response.json()["data"])


if __name__ == '__main__':
    main()
