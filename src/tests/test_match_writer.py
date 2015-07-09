from nose.tools import assert_is_not_none

from notifirc.message import Message
from notifirc.match_writer import PostgresMatchWriter


def test_serialize_works_on_message_objects():
    msg_store = PostgresMatchWriter(None)
    msgs = [
        Message(0,  '#myChanel', 'Me', 'this is a message'),
        Message(1,  '#myChanel', 'Me', 'this is a message'),
        Message(2,  '#myChanel', 'Me', 'this is a message'),
        None
    ]
    serialized = msg_store._serialize(msgs)
    assert_is_not_none(serialized)
