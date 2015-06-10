import redis
import sys
from pprint import pprint
import pickle

def decode_message(data):
    channel = data['channel']
    m = pickle.loads(data['data'])
    return {
        'channel': channel,
        'id': m['id'],
        'nick': m['nick'],
        'msg': m['msg']
    }

if len(sys.argv) < 2:
    print("Usage: redis_listen.py channel_name")
    sys.exit(1)

CHANNEL = sys.argv[1]

rdis = redis.StrictRedis(host='localhost', 
    port=6379)

sub = rdis.pubsub(ignore_subscribe_messages=True)
sub.subscribe(CHANNEL) 

for m in sub.listen():
    msg = decode_message(m)
    pprint(msg)