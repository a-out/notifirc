import redis
from functools import partial
import threading

from notifirc.listeners import FileListener
from notifirc.message_store import RedisMessageStore
from notifirc.filters import contains
from notifirc.processor import process_messages


def start_processor():
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


t = threading.Thread(target=start_processor)
t.daemon = True

t.start()

file_listener = FileListener(
    'ubuntu',
    redis.StrictRedis(host='localhost', port=6379),
    '../data/ubuntu_5_01_15.txt')
file_listener.listen()

t.join()