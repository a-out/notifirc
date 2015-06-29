from unittest.mock import MagicMock
from functools import partial

from notifirc.processor import process_messages
from notifirc.message_store import MessageStore
from notifirc.subscriber import Subscriber
from notifirc.utils import encode_msg, decode_msg
from notifirc.filters import create_filter
from notifirc.match_writer import MatchWriter


FILTS = [
    create_filter(0, 'contains', 'hi')
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

    process_messages(msg_store, sub, FILTS, m_writer)

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
        {'data': encode_msg('mychannel', 1, 'rth', 'one')},
        {'data': encode_msg('mychannel', 2, 'rth', 'two')},
        {'data': encode_msg('mychannel', 3, 'rth', 'three')},
        {'data': encode_msg('mychannel', 4, 'rth', 'four')},
        {'data': encode_msg('mychannel', 5, 'rth', 'five')}
    ])
    m_writer = MatchWriter()

    process_messages(msg_store, sub, FILTS, m_writer)

    msg_store.get_message.assert_called_with('mychannel', 0)


def test_process_messages_detects_match():
    matching_msg = encode_msg('mychannel', 0, 'rth', 'hi everyone!')
    msgs = [
        {'data': matching_msg},
        {'data': encode_msg('mychannel', 1, 'rth', 'one')},
        {'data': encode_msg('mychannel', 2, 'rth', 'two')},
        {'data': encode_msg('mychannel', 3, 'rth', 'three')},
        {'data': encode_msg('mychannel', 4, 'rth', 'four')},
        {'data': encode_msg('mychannel', 5, 'rth', 'five')}
    ]

    def get_msg(channel, msg_id):
        if msg_id == 0:
            return decode_msg(matching_msg)

    def get_messages(channel, ids):
        if ids == [0, 1, 2, 3, 4]:
            return msgs
        else:
            return []

    msg_store = MessageStore()
    msg_store.save_message = MagicMock()
    msg_store.get_message = MagicMock(side_effect=get_msg)
    msg_store.get_messages = MagicMock(side_effect=get_messages)
    sub = Subscriber()
    sub.listen = MagicMock(return_value=msgs)
    m_writer = MatchWriter()
    m_writer.save = MagicMock()

    process_messages(msg_store, sub, FILTS, m_writer)
    m_writer.save.assert_called_with('mychannel', [0], msgs)
