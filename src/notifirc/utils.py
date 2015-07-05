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
