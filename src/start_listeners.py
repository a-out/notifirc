import redis

from notifirc.listeners import FileListener
from notifirc.publisher import RedisPublisher


file_listener = FileListener(
    'ubuntu',
    RedisPublisher(
        redis.StrictRedis(host='localhost', port=6379)
    ),
    '../data/ubuntu_5_01_15.txt')
file_listener.listen()
