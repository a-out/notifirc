import redis
from filters import contains
from functools import partial
from pprint import pprint
from utils import decode_msg
from message_store import RedisMessageStore

CONTEXT_AFTER = 5

def _context(x, before, after):
    return list(range(x - before, x + after))

def check_matches(msg, filters):
    matched_filters = []
    for f in filters:
        if f['func'](msg):
            print(msg)
            matched_filters.append(f['id'])
    return matched_filters

def get_context(msg_store, channel, msg_id, m_after=5, m_before=2):
    msg_ids = _context(msg_id, m_before, m_after)
    import ipdb; ipdb.set_trace()
    return msg_store.get_messages(channel, msg_ids)

def process_messages(msg_store, sub, filters):
    last_msg = 0
    for m in sub.listen():
        msg_data = m['data']
        msg = decode_msg(msg_data)
        last_msg = msg['id']

        msg_store.save_message(msg['channel'], msg['id'], msg_data)

        # check msg from the past, so we have some
        # context for our matches
        msg_to_check = msg_store.get_message(msg['channel'], last_msg - 5)
        import ipdb; ipdb.set_trace()

        if msg_to_check:
            matches = check_matches(msg['msg'], filters)
            if len(matches) > 0:
                pprint(get_context(msg_store, msg_to_check['channel'], msg_to_check['id']))
                


if __name__ == '__main__':
    rdis = redis.StrictRedis(host='localhost', 
        port=6379)
    sub = rdis.pubsub(ignore_subscribe_messages=True)
    sub.subscribe('notifirc-messages')

    m_store = RedisMessageStore(
        redis.StrictRedis(host='localhost', 
        port=6379))

    filts = [
        {'id': 0, 'func': partial(contains, phrase='hi')}
    ]

    process_messages(m_store, sub, filts)