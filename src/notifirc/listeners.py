import asyncio
from pprint import pprint
import logging
from datetime import datetime

from . unpack import unpack_command
from . utils import encode_msg


TIMEOUT = 300
logger = logging.getLogger(__name__)


def _send(writer, msg):
    data = msg + "\r\n"
    writer.write(data.encode())


def _irc_initialize(writer, config, nickserv=True):
    _send(writer, "USER {} 8 * :{}".format(config['nick'], config['nick']))
    _send(writer, "NICK " + config['nick'])
    if nickserv:
        _send(writer,
              "NICKSERV identify {} {}".format(
                config['creds'][0], config['creds'][1]))


def _join(writer, config):
    _send(writer, "JOIN " + config['channel'])


def _handle_message(writer, config, pub, msg_id, command, params):
    if command == 'PRIVMSG':
        logger.info("[{}] {} -> {}".format(
            config['channel'], params['nick'], params['message']
        ))
        pub.publish(encode_msg(
            config['channel'], msg_id, params['nick'], params['message']
        ))
    elif command == 'PING':
        _send(writer, "PONG " + params['message'])
        logger.info("[{}] PONG {}".format(config['channel'], params['message']))
    elif command == 'JOIN' and params['nick'] == config['nick']:
        logger.info("JOINED " + config['channel'])


@asyncio.coroutine
def irc_listen(loop, pub, config, ssl=True):
    msg_id = 0
    reader, writer = yield from asyncio.open_connection(
        config['host'], config['port'], loop=loop, ssl=ssl)

    _irc_initialize(writer, config)
    _join(writer, config)

    while True:
        try:
            fut = reader.read(4096)
            # wait up to TIMEOUT seconds to read new msg from socket
            data = yield from asyncio.wait_for(fut, timeout=TIMEOUT)
        except asyncio.TimeoutError:
            logger.info("[{}] TIMEOUT".format(config['channel']))
            break

        try:
            command, params = unpack_command(data.decode())
            _handle_message(writer, config, pub, msg_id, command, params)
        except ValueError:
            # message can't be parsed. just ignore it, a la Postel's Law
            pass
        msg_id += 1

    logger.info("[{}] COMPLETED".format(config['channel']))
    writer.close()
