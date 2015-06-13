import redis
from listeners import FileListener


rdis = redis.StrictRedis(host='localhost',
    port=6379,
    decode_responses=True)

file_listener = FileListener('ubuntu', rdis, 'data/ubuntu_5_01_15.txt')
file_listener.listen()