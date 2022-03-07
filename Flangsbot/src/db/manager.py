from typing import Any, Optional

from .backend.base import Database
from .backend.base.base import UnsupportedDatabase

from .backend.types import DATABASE_TYPES


class DataBaseManager:
    @staticmethod
    def db_type(database_connection: Any) -> Optional[Database]:
        if type(database_connection) not in DATABASE_TYPES:
            raise UnsupportedDatabase(
                f'Database of type {type(database_connection)} is not supported by the database manager.'
            )
        return DATABASE_TYPES[type(database_connection)]['class'](database_connection)
