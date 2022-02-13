from typing import Any, Optional

from .backend.base import Database
from .backend.base.base import UnsupportedDatabase

from .backend.types import DATABASE_TYPES

class DatabaseManager:
    @staticmethod
    def connect(database: Any) -> Optional[Database]:
        
        if type(database) not in DATABASE_TYPES:
            raise UnsupportedDatabase(
                f'Database of type {type(database)} is not supported by the database manager.'
            )

        return DATABASE_TYPES[type(database)]['class'](database)