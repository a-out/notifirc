from time import sleep
import re
from notifirc.utils import encode_msg


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
            'notifirc-messages',
            encode_msg(channel, msg_id, nick, msg)
        )


class FileListener(Listener):
    """
        'Listen' for messages in a file. Used for integration testing.
    """

    def __init__(self, channel, rdis, filename):
        self.channel = channel
        self.rdis = rdis
        self.file = open(filename, 'r', encoding='utf-8')
        self.msg_id = 0

    def listen(self):
        for line in self.file:
            time, nick, msg = re.match(r'(\[.*\]) <(.*)> (.*)', line).groups()
            self.send(self.channel, self.msg_id, nick, msg)
            self.msg_id += 1
            print(msg)
            sleep(0.1)