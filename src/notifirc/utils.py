import pickle
import re
from random import shuffle

from pprint import pprint


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

    if len(split) < 2:
        print("irregular string: " + s)
        return {'type': '', 'data': s}

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
    elif split[0] == 'ERROR':
        if 'Connection timed out' in s:
            m_type = 'ERROR_TIMEOUT'
    else:
        if 'End of /NAMES list' in s:
            m_type = 'JOINED_CHANNEL'

    return {'type': m_type, 'data': m_data}


def read_nicks(nick_file):
    nicks = [l.rstrip() for l in nick_file.readlines()]
    shuffle(nicks)
    return nicks

def read_configs(config_file, nicks_file, creds_file):
    nicks = read_nicks(nicks_file)
    channels = [
        l.rstrip().split(' ') for l in
        config_file.readlines()]
    creds = creds_file.read().rstrip().split(' ')

    return [
        {
            'host': host,
            'port': port,
            'channel': channel,
            'nick': nicks.pop(),
            'creds': creds
        }
        for (host, port, channel) in channels
    ]
