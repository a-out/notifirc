import redis
from functools import partial

from notifirc.filters import contains
from notifirc.message_store import RedisMessageStore
from notifirc.processor import process_messages


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