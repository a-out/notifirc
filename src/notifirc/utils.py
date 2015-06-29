import pickle
import re


def decode_msg(data):
    if data is None:
        return None

    m = pickle.loads(data)
    return {
        'channel': m['channel'],
        'id': m['id'],
        'nick': m['nick'],
        'msg': m['msg']
    }


def encode_msg(channel, msg_id, nick, msg):
    return pickle.dumps({
        'id': msg_id,
        'channel': channel,
        'nick': nick,
        'msg': msg
    })


def zero_min(n):
    return 0 if n < 0 else n


def parse_irc_msg(s):
    split = s.split(' ')
    m_type, m_data = '', ''

    if split[0] == 'PING':
        m_type = 'PING'
        # return hostname, without preceding colon
        m_data = split[1].split(':')[1]
    elif split[1] == 'PRIVMSG':
        m_type = 'PRIVMSG'
        msg = re.search(r'^:(.*)!.+ PRIVMSG #.+ :(.*)', s.rstrip('\r\n'))
        if msg: m_data = msg.groups()
    elif split[1] == 'NOTICE':
        if 'You are now identified' in s:
            m_type = 'NOTICE_IDENTIFIED'

    return {'type': m_type, 'data': m_data}
