from pathlib import Path

from discord.ext.commands.errors import BadArgument, CommandNotFound

PREFIX = '$'

LOGGIN_FORMAT = '[%(asctime)s]:[%(levelname)s] $%(name)s @: %(message)s'

OWNER_ID = 546542419399802884
OWNER_IDS = [546542419399802884]

COGS_DIR = './Flangsbot/src/cogs'

# COGS = [
#   path.split('//')[-1][:-3] for cog in glob(COGS_DIR)
# ]

COGS = [
    path.stem for path in Path(COGS_DIR).glob('*.py')
]

IGNORE_EXCEPTIONS = (
    CommandNotFound,
    BadArgument
)