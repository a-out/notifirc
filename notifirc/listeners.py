from time import sleep
import re
import pickle


class Listener(object):
    """
        Abstract class that defines an object that listens for 
        messages, checks for matches and pushes on to an external queue.
    """

    def listen(self):
        raise NotImplementedError()

    def check_matches(self, msg):
        raise NotImplementedError()

    def send(self, channel, msg_id, nick, msg):
        self.rdis.publish(
            self.channel,
            pickle.dumps({
                'id': msg_id,
                'channel': self.channel,
                'nick': nick,
                'msg': msg
            }
        ))


class FileListener(Listener):
    """
        'Listen' for messages in a file. Used for integration testing.
    """

    def __init__(self, channel, rdis, filename, filters):
        self.channel = channel
        self.rdis = rdis
        self.filename = filename
        self.file = open(filename, 'r')
        self.msg_id = 0

    def listen(self):
        for line in self.file:
            time, nick, msg = re.match(r'(\[.*\]) <(.*)> (.*)', line).groups()
            self.send(self.channel, self.msg_id, nick, msg)
            self.msg_id += 1
            sleep(0.1)