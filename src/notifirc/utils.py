import pickle


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
