from unittest.mock import MagicMock
from nose.tools import assert_equal

from notifirc.message_store import MessageStore
from notifirc.processor import _context


def test_context():
    expected = [3, 4, 5, 6, 7, 8, 9, 10]
    assert_equal(_context(5, 2, 5), expected)