from typing import Any, List, Union, Dict

from ..base import Database

import aiosqlite

class SqliteDatabase(Database):
    def __str__(self):
        return f'{self.__class__.__name__}'

    def __init__(self, database):
        super().__init__(database)
        self.place_holder = SQLITE_TYPE[type(database)]['placeholder']
        self.cursor_context = SQLITE_TYPE[type(database)]['cursorcontext']
        self.commit_needed = SQLITE_TYPE[type(database)]['commit']
        self.quotes = SQLITE_TYPE[type(database)]['quotes']
        self.pool = SQLITE_TYPE[type(database)]['pool']


SQLITE_TYPE: Dict[Any, Dict[str, Any]] = {
    
    aiosqlite.core.Connection: {
        "class": SqliteDatabase,
        "placeholder": '?',
        "cursorcontext": True,
        "commit": True,
        "quotes": '"',
        "pool": False,
    }
}