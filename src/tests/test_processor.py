from unittest.mock import MagicMock

from notifirc.processor import process_messages
from notifirc.message_store import MessageStore
from notifirc.subscriber import Subscriber
from notifirc.filters import create_filter
from notifirc.match_writer import MatchWriter
from notifirc.message import Message


FILTS = [
    create_filter(0, 'contains', 'hi')
]


def test_process_messages_saves_each_message():
    msg_store = MessageStore()
    msg_store.save_message = MagicMock()
    msg_store.get_message = MagicMock(return_value=None)
    sub = Subscriber()
    msg = Message(0, 'mychannel', 'rth', 'zero')
    sub.listen = MagicMock(return_value=[
        {'data': msg.encode()}
    ])
    m_writer = MatchWriter()

    process_messages(msg_store, sub, FILTS, m_writer)

    msg_store.save_message.assert_called_with(msg)


def test_process_messages_checks_fifth_latest_message_for_matches():
    msg_store = MessageStore()
    msg_store.save_message = MagicMock()
    msg_store.get_message = MagicMock(return_value=None)
    sub = Subscriber()
    sub.listen = MagicMock(return_value=[
        {'data': Message(0, 'mychannel',  'rth', 'zero').encode()},
        {'data': Message(1, 'mychannel',  'rth', 'one').encode()},
        {'data': Message(2, 'mychannel',  'rth', 'two').encode()},
        {'data': Message(3, 'mychannel',  'rth', 'three').encode()},
        {'data': Message(4, 'mychannel',  'rth', 'four').encode()},
        {'data': Message(5, 'mychannel',  'rth', 'five').encode()}
    ])
    m_writer = MatchWriter()

    process_messages(msg_store, sub, FILTS, m_writer)

    msg_store.get_message.assert_called_with('mychannel', 0)


def test_process_messages_detects_match():
    matching_msg = Message(0, 'mychannel', 'rth', 'hi everyone!')
    msgs = [
        {'data': matching_msg.encode()},
        {'data': Message(1, 'mychannel', 'rth', 'one').encode()},
        {'data': Message(2, 'mychannel', 'rth', 'two').encode()},
        {'data': Message(3, 'mychannel', 'rth', 'three').encode()},
        {'data': Message(4, 'mychannel', 'rth', 'four').encode()},
        {'data': Message(5, 'mychannel', 'rth', 'five').encode()}
    ]

    def get_msg(channel, msg_id):
        if msg_id == 0:
            return matching_msg

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
