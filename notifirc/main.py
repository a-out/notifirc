import redis
from functools import partial

import filters
from listeners import FileListener


filters = [
    { 'id': 0, 'func': partial(filters.contains, phrase="hi") },
    { 'id': 1, 'func': partial(filters.starts_with, phrase="question") }
]

rdis = redis.StrictRedis(host='localhost', 
    port=6379,
    decode_responses=True)

file_listener = FileListener('ubuntu', rdis, 'data/ubuntu_5_01_15.txt', filters)
file_listener.listen()