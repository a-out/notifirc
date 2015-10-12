import logging

from . import db
from . import filters
from . import listeners
from . import match_writer
from . import message_store
from . import processor
from . import publisher
from . import subscriber
from . import unpack
from . import utils

logging.basicConfig(
    format='[%(levelname)s] %(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p',
    filename='notifirc.log',
    level=logging.DEBUG)
