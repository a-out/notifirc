import pickle


class Message(object):

    @classmethod
    def decode(cls, data):
        return pickle.loads(data)

    @classmethod
    def from_dict(cls, d):
        try:
            return cls(d['msg_id'], d['channel'], d['nick'], d['text'])
        except KeyError:
            return None

    def __init__(self, msg_id, channel, nick, text):
        self.msg_id = msg_id
        self.channel = channel
        self.nick = nick
        self.text = text

    def encode(self):
        return pickle.dumps(self)

    def to_dict(self):
        return {
            'msg_id':   self.msg_id,
            'channel':  self.channel,
            'nick':     self.nick,
            'text':     self.text
        }

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
