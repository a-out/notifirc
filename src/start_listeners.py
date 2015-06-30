import redis
import threading
import logging

from notifirc.listeners import IrcListener
from notifirc.publisher import RedisPublisher
from notifirc.utils import read_nicks

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    level=logging.DEBUG)

nicks = read_nicks(open('../data/nicks.txt'))
CHANNELS = [
    l.rstrip().split(' ') for l in
    open('../data/channels.txt').readlines()]
PASSWORD = open('../data/password.txt').read().strip().split(' ')


def start(hostname, channel, nick):
    IrcListener(
        nick,
        PASSWORD,
        hostname,
        channel,
        RedisPublisher(redis.StrictRedis(host='localhost', port=6379))
    ).listen()


threads = []
for (host, channel) in CHANNELS:
    nick = nicks.pop()
    t = threading.Thread(target=start, args=(host, channel, nick))
    threads.append(t)
    t.start()
