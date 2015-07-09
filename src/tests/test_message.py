from nose.tools import assert_equal

from notifirc.message import Message


def test_message_constructor():
    msg = Message(0, 'mychannel', 'rth', 'message text')
    assert_equal(msg.msg_id, 0)
    assert_equal(msg.channel, 'mychannel')
    assert_equal(msg.nick, 'rth')
    assert_equal(msg.text, 'message text')


def test_message_from_dict():
    mdict = {
        'msg_id': 1,
        'channel': '#myChannel',
        'nick': 'Me',
        'text': 'This is my message'
    }

    m = Message.from_dict(mdict)
    assert_equal(m.msg_id, 1)
    assert_equal(m.channel, '#myChannel')
    assert_equal(m.nick, 'Me')
    assert_equal(m.text, 'This is my message')


def test_message_to_and_from_dict_completeness():
    m = Message(0, 'mychannel', 'rth', 'message text')

    d = m.to_dict()
    msg = Message.from_dict(d)

    assert_equal(msg.msg_id, 0)
    assert_equal(msg.channel, 'mychannel')
    assert_equal(msg.nick, 'rth')
    assert_equal(msg.text, 'message text')


def test_message_encode_and_decode_completeness():
    m = Message(0, 'mychannel', 'rth', 'message text')

    e = m.encode()
    msg = Message.decode(e)

    assert_equal(msg.msg_id, 0)
    assert_equal(msg.channel, 'mychannel')
    assert_equal(msg.nick, 'rth')
    assert_equal(msg.text, 'message text')
