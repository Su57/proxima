import io
from unittest import TestCase, main
from unittest.mock import Mock, patch

from werkzeug.datastructures import FileStorage

from src.apps.common.repository import FileRepository
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
        mock_load_user.return_value = Mock(id=1, is_super=True)
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
        mock_load_user.return_value = Mock(id=1, is_super=True)
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


if __name__ == '__main__':
    main()
