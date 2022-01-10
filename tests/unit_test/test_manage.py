from unittest import main
from unittest.mock import ANY

from src.apps.manage.models import *
from src.apps.manage.repository import *
from tests.unit_test.base import RepositoryTestCase


class UserRepositoryTestCase(RepositoryTestCase):
    """
    用户repository相关单元测试
    """

    def setUp(self) -> None:
        super().setUp()
        self.repository = UserRepository(session_context=self.session_context)

    def test_add_user_without_roles(self):
        user = User()
        user.id = 1
        result = self.repository.add_user(user, roles=None)
        self.session.add.assert_called_once_with(user)
        self.session.flush.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.execute.assert_not_called()
        self.assertEqual(result, 1)

    def test_add_user_with_roles(self):
        user = User()
        user.id = 1
        result = self.repository.add_user(user, roles=[1, 2, 3])
        self.session.add.assert_called_once_with(user)
        self.session.flush.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.execute.assert_called_once()
        self.assertEqual(result, 1)

    def test_update_user_with_roles(self):
        ident = 1
        roles = [1, 2, 3]
        data = {"username": "some_username"}
        self.repository.update_user(ident, data, roles)
        self.assertEqual(self.session.execute.call_count, 3)
        self.session.commit.assert_called_once()

    def test_update_user_without_roles(self):
        ident = 1
        data = {"username": "some_username"}
        self.repository.update_user(ident, data, None)
        self.assertEqual(self.session.execute.call_count, 2)
        self.session.commit.assert_called_once()

    def test_delete_user(self):
        self.repository.delete_user(1)
        self.assertEqual(self.session.execute.call_count, 2)
        self.session.commit.assert_called_once()

    def test_get_user_by_email(self):
        self.repository.get_user_by_email(ANY)
        self.session.execute.assert_called_once()

    def test_get_by_username_or_email(self):
        self.repository.get_by_username_or_email(ANY, ANY)
        self.session.execute.assert_called_once()


class RoleRepositoryTestCase(RepositoryTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.repository = RoleRepository(session_context=self.session_context)

    def test_add_role_without_authorities(self):
        role = Role()
        role.id = 1
        result = self.repository.add_role(role, authorities=None)
        self.session.add.assert_called_once_with(role)
        self.session.flush.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.execute.assert_not_called()
        self.assertEqual(result, 1)

    def test_add_role_with_authorities(self):
        role = Role()
        role.id = 1
        result = self.repository.add_role(role, authorities=[1, 2, 3])
        self.session.add.assert_called_once_with(role)
        self.session.flush.assert_called_once()
        self.session.commit.assert_called_once()
        self.session.execute.assert_called_once()
        self.assertEqual(result, 1)

    def test_update_role_without_authorities(self):
        ident = 1
        data = {"name": ANY}
        self.repository.update_role(ident, data, None)
        self.session.execute.assert_called_once()
        self.session.commit.assert_called_once()

    def test_update_user_with_roles(self):
        ident = 1
        roles = [1, 2, 3]
        data = {"name": ANY}
        self.repository.update_role(ident, data, roles)
        self.assertEqual(self.session.execute.call_count, 3)
        self.session.commit.assert_called_once()

    def test_delete_role(self):
        self.repository.delete_role(1)
        self.assertEqual(self.session.execute.call_count, 3)
        self.session.commit.assert_called_once()

    def test_get_user_count_by_role(self):
        self.repository.get_user_count_by_role(1)
        self.session.execute.assert_called_once()

    def test_get_count_by_name(self):
        self.repository.get_count_by_name(ANY)
        self.session.execute.assert_called_once()


if __name__ == '__main__':
    main()
