import redis
import asyncio

from notifirc.listeners import irc_listen
from notifirc.publisher import RedisPublisher
from notifirc.utils import read_configs


configs = read_configs(
    open('../data/channels.txt'),
    open('../data/nicks.txt'),
    open('../data/creds.txt'))
pub = RedisPublisher(redis.StrictRedis(host='localhost', port=6379))
loop = asyncio.get_event_loop()

tasks = [irc_listen(loop, pub, config, ssl=False) for config in configs]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
