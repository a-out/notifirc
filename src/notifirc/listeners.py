from time import sleep
import re
import socket

from pprint import pprint

from notifirc.utils import encode_msg, parse_irc_msg


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
        self.publisher.publish(encode_msg(channel, msg_id, nick, msg))


class FileListener(Listener):
    """
        'Listen' for messages in a file. Used for integration testing.
    """

    def __init__(self, channel, publisher, filename):
        self.channel = channel
        self.publisher = publisher
        self.file = open(filename, 'r', encoding='utf-8')
        self.msg_id = 0

    def listen(self):
        for line in self.file:
            time, nick, msg = re.match(r'(\[.*\]) <(.*)> (.*)', line).groups()
            self.send(self.channel, self.msg_id, nick, msg)
            self.msg_id += 1
            print(msg)
            sleep(0.1)


class IrcListener(Listener):
    """
        Listen for messages on a given IRC channel and save them to
        a MessageWriter.
    """

    def __init__(self, nick, creds, hostname, channel, publisher):
        self.nick = nick
        self.creds = creds
        self.hostname = hostname
        self.channel = channel
        self.publisher = publisher
        self.sock = socket.socket()
        self.msg_id = 0

    def listen(self):
        self.sock.connect((self.hostname, 6667))
        self.receive()
        self.send_irc("USER {} 8 * :{}".format(self.nick, self.nick))
        self.send_irc("NICK {}".format(self.nick))

        if 'freenode' in self.hostname:
            self.send_irc(
                "NICKSERV identify {} {}".format(self.creds[0], self.creds[1]))
            self.wait_for('NOTICE_IDENTIFIED')

        self.send_irc("JOIN #" + self.channel)

        while True:
            msg = self.receive()

            if msg['type'] == 'PING':
                self.send_irc("PONG " + msg['data'])
            elif msg['type'] == 'PRIVMSG':
                self.send(self.channel, self.msg_id, msg['data'][0], msg['data'][1])
                self.msg_id += 1

    def receive(self):
        buff = self.sock.recv(4096).decode('UTF-8')
        pprint(buff)
        return parse_irc_msg(buff)

    def wait_for(self, msg_type):
        while True:
            msg = self.receive()
            if msg['type'] == msg_type: break

    def send_irc(self, cmd):
        print("sending: " + cmd)
        self.sock.send("{}\r\n".format(cmd).encode('UTF-8'))
