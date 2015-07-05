from nose.tools import assert_equals
from unittest.mock import MagicMock

from notifirc.utils import read_nicks


def test_read_nicks():
    n = ['alex\n', 'brittany\n', 'chris\n', 'debra\n']
    file = MagicMock()
    file.readlines = MagicMock(return_value=n)
    nicks = read_nicks(file)
    assert_equals(sorted([x.rstrip() for x in n]), sorted(nicks))
