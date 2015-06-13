from nose.tools import assert_true, assert_false
from unittest.mock import MagicMock
from functools import partial

from notifirc.processor import process_messages
from notifirc.message_store import MessageStore
from notifirc.subscriber import Subscriber
from notifirc.utils import encode_msg
from notifirc.filters import contains
from notifirc.match_writer import MatchWriter


filts = [
    {'id': 0, 'func': partial(contains, phrase='hi')}
]

def test_process_messages_saves_each_message():
    msg_store = MessageStore()
    msg_store.save_message = MagicMock()
    msg_store.get_message = MagicMock(return_value=None)
    sub = Subscriber()
    sub.listen = MagicMock(return_value=[
        {'data': encode_msg('mychannel', 0, 'rth', 'zero')}
    ])
    m_writer = MatchWriter()

    process_messages(msg_store, sub, filts, m_writer)

    msg_store.save_message.assert_called_with(
        'mychannel', 
        0, 
        encode_msg('mychannel', 0, 'rth', 'zero'))

def test_process_messages_checks_fifth_latest_message_for_matches():
    msg_store = MessageStore()
    msg_store.save_message = MagicMock()
    msg_store.get_message = MagicMock(return_value=None)
    sub = Subscriber()
    sub.listen = MagicMock(return_value=[
        {'data': encode_msg('mychannel', 0, 'rth', 'zero')},
        {'data': encode_msg('mychannel', 1, 'rth', 'zero')},
        {'data': encode_msg('mychannel', 2, 'rth', 'zero')},
        {'data': encode_msg('mychannel', 3, 'rth', 'zero')},
        {'data': encode_msg('mychannel', 4, 'rth', 'zero')},
        {'data': encode_msg('mychannel', 5, 'rth', 'zero')}
    ])
    m_writer = MatchWriter()

    process_messages(msg_store, sub, filts, m_writer)

    msg_store.get_message.assert_called_with('mychannel', 0)