from unittest import TestCase
from unittest.mock import Mock

from src.core.db.session import SessionContext


class RepositoryTestCase(TestCase):

    def setUp(self) -> None:
        self.session = Mock()
        self.session_context = Mock(spec=SessionContext, __enter__=Mock(), __exit__=Mock())
        self.session_context.__enter__.return_value = self.session

