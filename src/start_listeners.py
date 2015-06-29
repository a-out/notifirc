import redis
from random import choice
import threading

from notifirc.listeners import IrcListener
from notifirc.publisher import RedisPublisher
from notifirc.utils import read_nicks

NICKS = read_nicks(open('../data/nicks.txt'))
PASSWORD = open('../data/password.txt').read().strip().split(' ')

def start(hostname, channel):
    IrcListener(
        choice(NICKS),
        PASSWORD,
        hostname,
        channel,
        RedisPublisher(redis.StrictRedis(host='localhost', port=6379))
    ).listen()

channels = [l.split(' ') for l in open('../data/channels.txt').readlines()]

threads = []
for c in channels:
    t = threading.Thread(target=start, args=(c[0], c[1]))
    threads.append(t)
    t.start()
