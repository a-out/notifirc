from notifirc.message import Message


class MessageStore(object):

    def _key_name(self, channel, msg_id):
        return "notifirc_{}_{}".format(channel, msg_id)

    def get_message(self, channel, msg_id):
        raise NotImplementedError()

    def get_messages(self, channel, msg_ids):
        raise NotImplementedError()

    def save_message(self, channel, msg_id, data):
        raise NotImplementedError()


class RedisMessageStore(MessageStore):

    def __init__(self, rdis):
        self.rdis = rdis

    def get_message(self, channel, msg_id):
        msg_key = self._key_name(channel, msg_id)
        mdict = self.rdis.hgetall(msg_key)
        return Message.from_dict(mdict)

    def get_messages(self, channel, msg_ids):
        pipe = self.rdis.pipeline()

        for msg_id in msg_ids:
            msg_key = self._key_name(channel, msg_id)
            pipe.hgetall(msg_key)
        return [Message.from_dict(d) for d in pipe.execute()]

    def save_message(self, msg):
        msg_key = self._key_name(msg.channel, msg.msg_id)
        self.rdis.hmset(msg_key, msg.to_dict())
