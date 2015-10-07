import asyncio
from pprint import pprint
import logging

from . unpack import unpack_command
from . message import Message


TIMEOUT = 300
logger = logging.getLogger(__name__)


def _send(writer, msg):
    logger.info(msg)
    data = msg + "\r\n"
    writer.write(data.encode())


def _irc_initialize(writer, config):
    _send(writer, "USER {} 8 * :{}".format(config['nick'], config['nick']))
    _send(writer, "NICK " + config['nick'])
    if config['nickserv']:
        _send(writer,
              "NICKSERV identify {} {}".format(
                config['creds'][0], config['creds'][1]))
    else:
        _join(writer, config)


def _join(writer, config):
    _send(writer, "JOIN " + config['channel'])


def _handle_message(writer, config, pub, msg_id, command, params):
    if command == 'PRIVMSG':
        logger.info("[{}] {} -> {}".format(
            config['channel'], params['nick'], params['message']
        ))
        m = Message(msg_id, config['channel'], params['nick'], params['message'])
        pub.publish(m.encode())
    elif command == 'PING':
        _send(writer, "PONG " + params['message'])
        logger.info("[{}] PONG {}".format(config['channel'], params['message']))
    elif command == 'JOIN' and params['nick'] == config['nick']:
        logger.info("JOINED " + config['channel'])
    elif command == 'NOTICE' and params.get('nick') == 'NickServ':
        if 'identified' in params['message']:
            logger.info("IDENTIFIED")
            _join(writer, config)


@asyncio.coroutine
def irc_listen(loop, pub, config):
    msg_id = 0
    dump_file = open('../dump.txt', 'w')
    reader, writer = yield from asyncio.open_connection(
        config['host'], config['port'], loop=loop, ssl=config['ssl'])
    _irc_initialize(writer, config)

    while True:
        # read message
        try:
            fut = reader.read(4096)
            # wait up to TIMEOUT seconds to read new msg from socket
            data = yield from asyncio.wait_for(fut, timeout=TIMEOUT)
        except asyncio.TimeoutError:
            logger.info("[{}] TIMEOUT".format(config['channel']))
            reader, writer = yield from asyncio.open_connection(
                config['host'], config['port'], loop=loop, ssl=config['ssl'])
            _irc_initialize(writer, config)
            continue

        # parse / handle message
        try:
            dump_file.write(data.decode())
            command, params = unpack_command(data.decode())
            _handle_message(writer, config, pub, msg_id, command, params)
        except ValueError:
            # message can't be parsed. just ignore it, a la Postel's Law
            pass
        msg_id += 1

    logger.info("[{}] CONNECTION CLOSED".format(config['channel']))
    writer.close()
    dump_file.close()
