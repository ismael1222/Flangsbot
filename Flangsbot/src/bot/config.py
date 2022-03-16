from pathlib import Path

from discord.ext.commands.errors import BadArgument, CommandNotFound

import logging

# Define a prefix of the bot
PREFIX = '$'

# Define the bot's logging format

class CustomFormatter(logging.Formatter):

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt

        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset, 
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

FMT = '[%(asctime)s] | [%(levelname)s] $%(name)s @: %(message)s'

STD_HANDLER = logging.StreamHandler()
STD_HANDLER.setLevel(logging.DEBUG)
STD_HANDLER.setFormatter(
    CustomFormatter(FMT)
)

# Define the bot's owner ids
OWNER_ID = 546542419399802884
OWNER_IDS = [546542419399802884]

# Define the bot's cogs
COGS_DIR = './Flangsbot/src/cogs'

COGS = [
    path.stem for path in Path(COGS_DIR).glob('*.py')
]

# Define the bot's ignore exceptions
IGNORE_EXCEPTIONS = (
    CommandNotFound,
    BadArgument
)