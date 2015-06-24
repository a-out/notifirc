from notifirc.utils import decode_msg


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
        msg_data = self.rdis.get(msg_key)
        return decode_msg(msg_data)

    def get_messages(self, channel, msg_ids):
        pipe = self.rdis.pipeline()

        for msg_id in msg_ids:
            msg_key = self._key_name(channel, msg_id)
            pipe.get(msg_key)
        return [decode_msg(data) for data in pipe.execute()]

    def save_message(self, channel, msg_id, data):
        msg_key = self._key_name(channel, msg_id)
        self.rdis.set(msg_key, data)
