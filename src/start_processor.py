import redis
from functools import partial
import psycopg2

from notifirc.subscriber import RedisSubscriber
from notifirc.filters import contains
from notifirc.message_store import RedisMessageStore
from notifirc.processor import process_messages
from notifirc.match_writer import PostgresMatchWriter

sub = RedisSubscriber(redis.StrictRedis(host='localhost', port=6379))
m_store = RedisMessageStore(redis.StrictRedis(host='localhost', port=6379))
filts = [
    {'id': 1, 'func': partial(contains, phrase='hi')}
]

db_conn = psycopg2.connect("dbname=notifirc user=richard")
m_writer = PostgresMatchWriter(db_conn)

process_messages(m_store, sub, filts, m_writer)

db_conn.close()
