class Publisher(object):
    def publish(self, msg):
        raise NotImplementedError()


class RedisPublisher(Publisher):
    def __init__(self, rdis):
        self.rdis = rdis

    def publish(self, msg):
        self.rdis.publish(
            'notifirc-messages',
            msg
        )