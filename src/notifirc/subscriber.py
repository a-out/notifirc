class Subscriber(object):
    def listen(self):
        raise NotImplementedError()


class RedisSubscriber(Subscriber):
    def __init__(self, rdis):
        self.sub = rdis.pubsub(ignore_subscribe_messages=True)

    def listen(self):
        self.sub.subscribe('notifirc-messages')
        for m in self.sub.listen():
            yield m
