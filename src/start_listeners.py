import redis

from notifirc.listeners import IrcListener
from notifirc.publisher import RedisPublisher


# file_listener = FileListener(
#     'ubuntu',
#     RedisPublisher(
#         redis.StrictRedis(host='localhost', port=6379)
#     ),
#     '../data/ubuntu_5_01_15.txt')
# file_listener.listen()

IrcListener(
    'wowiezowie',
    open('../data/password.txt').read().strip().split(' '),
    'irc.freenode.net',
    'django',
    RedisPublisher(redis.StrictRedis(host='localhost', port=6379))
).listen()
