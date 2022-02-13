from collections import ChainMap

from .mysql.database import SQL_TYPE
from .sqlite.database import SQLITE_TYPE

DATABASE_LIST = [SQL_TYPE, SQLITE_TYPE]

DATABASE_TYPES = dict(ChainMap(*DATABASE_LIST))