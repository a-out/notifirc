from nose.tools import assert_equals

from notifirc.utils import parse_irc_msg


def test_can_parse_ping_message():
    msg = 'PING :orwell.freenode.net'
    parsed = parse_irc_msg(msg)
    assert_equals(parsed['type'], 'PING')
    assert_equals(parsed['data'], 'orwell.freenode.net')


def test_can_parse_ident_confirmation_message():
    msg = ':NickServ!NickServ@services. NOTICE nick :You are now identified for nick.'
    parsed = parse_irc_msg(msg)
    assert_equals(parsed['type'], 'NOTICE_IDENTIFIED')


def test_can_parse_long_privmsg():
    msg_info = ':username!abcdefgh@gateway/web/freenode/ip.255.255.255.255 PRIVMSG #channel '
    msg_text = ':Down, down, down. Would the fall never come to an end? “I wonder how many miles I’ve fallen by this time?” She took down a jar from one of the shelves as she passed. she said aloud. “I must be getting somewhere near the centre of the earth. Let me see: that would be four thousand miles down, I think—” (for, you see, Alice had learnt several things of this sort in her lessons in the schoolroom, and though this was not a very good opportunity for showing off her knowledge, as there was no one to listen to her, still it was good practice to say it over) “—yes, that’s about the right distance—but then I wonder what Latitude or Longitude I’ve got to?”\r\n'
    parsed = parse_irc_msg(msg_info + msg_text)
    assert_equals(parsed['data'][0], 'username')
    assert_equals(parsed['data'][1], msg_text.lstrip(':').rstrip('\r\n'))
