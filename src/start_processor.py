import redis
from functools import partial

from notifirc.subscriber import RedisSubscriber
from notifirc.filters import contains
from notifirc.message_store import RedisMessageStore
from notifirc.processor import process_messages
from notifirc.match_writer import MatchWriter

sub = RedisSubscriber(redis.StrictRedis(host='localhost', port=6379))
m_store = RedisMessageStore(redis.StrictRedis(host='localhost', port=6379))
filts = [
    {'id': 0, 'func': partial(contains, phrase='hi')}
]
m_writer = MatchWriter()

process_messages(m_store, sub, filts, m_writer)