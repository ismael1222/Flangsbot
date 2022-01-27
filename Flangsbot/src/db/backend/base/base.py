import logging

from aiomysql import Cursor, Connection, connect
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logging.getLogger(__name__)

class BaseDatabaseSchema:

    """
    This class and its subclasses are responsible for emitting schema-changing
    statements to the databases - model creation/removal/alteration, field
    renaming, index fiddling, and so on.
    """

    # Overrideable SQL templates
    sql_create_table = "CREATE TABLE %(table)s (%(definition)s)"
    sql_rename_table = "ALTER TABLE %(old_table)s RENAME TO %(new_table)s"
    sql_retablespace_table = "ALTER TABLE %(table)s SET TABLESPACE %(new_tablespace)s"
    sql_delete_table = "DROP TABLE %(table)s CASCADE"

    sql_create_column = "ALTER TABLE %(table)s ADD COLUMN %(column)s %(definition)s"
    sql_alter_column = "ALTER TABLE %(table)s %(changes)s"
    sql_alter_column_type = "ALTER COLUMN %(column)s TYPE %(type)s"
    sql_alter_column_null = "ALTER COLUMN %(column)s DROP NOT NULL"
    sql_alter_column_not_null = "ALTER COLUMN %(column)s SET NOT NULL"
    sql_alter_column_default = "ALTER COLUMN %(column)s SET DEFAULT %(default)s"
    sql_alter_column_no_default = "ALTER COLUMN %(column)s DROP DEFAULT"
    sql_alter_column_no_default_null = sql_alter_column_no_default
    sql_alter_column_collate = "ALTER COLUMN %(column)s TYPE %(type)s%(collation)s"
    sql_delete_column = "ALTER TABLE %(table)s DROP COLUMN %(column)s CASCADE"
    sql_rename_column = "ALTER TABLE %(table)s RENAME COLUMN %(old_column)s TO %(new_column)s"
    sql_update_with_default = "UPDATE %(table)s SET %(column)s = %(default)s WHERE %(column)s IS NULL"

    sql_unique_constraint = "UNIQUE (%(columns)s)%(deferrable)s"
    sql_check_constraint = "CHECK (%(check)s)"
    sql_delete_constraint = "ALTER TABLE %(table)s DROP CONSTRAINT %(name)s"
    sql_constraint = "CONSTRAINT %(name)s %(constraint)s"

    sql_create_check = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s CHECK (%(check)s)"
    sql_delete_check = sql_delete_constraint

    sql_create_unique = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s UNIQUE (%(columns)s)%(deferrable)s"
    sql_delete_unique = sql_delete_constraint

    sql_create_fk = (
        "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s FOREIGN KEY (%(column)s) "
        "REFERENCES %(to_table)s (%(to_column)s)%(deferrable)s"
    )
    sql_create_inline_fk = None
    sql_create_column_inline_fk = None
    sql_delete_fk = sql_delete_constraint

    sql_create_index = "CREATE INDEX %(name)s ON %(table)s (%(columns)s)%(include)s%(extra)s%(condition)s"
    sql_create_unique_index = "CREATE UNIQUE INDEX %(name)s ON %(table)s (%(columns)s)%(include)s%(condition)s"
    sql_delete_index = "DROP INDEX %(name)s"

    sql_create_pk = "ALTER TABLE %(table)s ADD CONSTRAINT %(name)s PRIMARY KEY (%(columns)s)"
    sql_delete_pk = sql_delete_constraint

    sql_delete_procedure = 'DROP PROCEDURE %(procedure)s'

    def __init__(self, conn):
        self.db = None
        self.cnx: Connection 
        self.cur: Cursor

    def __enter__(self): ...

    def __exit__(self, exc_type, exc_val, exc_traceback): ...
    
    async def __close__(self): ...

    def with_commit(func):
        async def inner(self, *args, **kwargs):
            resp = await func(self, *args, **kwargs)
            if self.commit_needed:
                await self.commit()
            return resp
        return inner

    def with_cursor(func):
        async def inner(self, *args, **kwargs):
            database = await self.database.acquire() if self.pool else self.database
            if self.cursor_context:
                async with database.cursor() as cursor:
                    resp = await func(self, cursor, *args, **kwargs)
            else:
                cursor = await database.cursor()
                resp = await func(self, cursor, *args, **kwargs)
                await cursor.close()
            if self.pool:
                self.database.release(database)
            return resp
        return inner

    async def build(self) -> None: ...

    async def execute(self, sql, params: tuple = None): ...

    async def multiexe(self, sql, valueset):...

    async def commit(self) -> None: ...

    async def createTable(self, table: str, *values): ...

    async def record(self, sql, *values):
        self.cur.execute(sql, tuple(values))
        return self.cur.fetchall()
    
    async def records(self, sql, *values):
        self.cur.execute(sql, tuple(values))
        return self.cur.fetchall()

    async def createField(self, sql, *values):
        self.cur.execute(sql, tuple(values))
        if (fetch := self.cur.fetchone()) is not None:
            return fetch[0]

    async def createColumn(self, sql, *values):
        self.cur.execute(sql, tuple(values))
        return [item[0] for item in self.cur.fetchall()]

    def createAutosave(self, sched: AsyncIOScheduler, *, interval: int = None): ...

    def deleteAutosaver(self, sched: AsyncIOScheduler): ...

    async def remove_procedure(self, procedure_name, param_types: tuple = None): ...

