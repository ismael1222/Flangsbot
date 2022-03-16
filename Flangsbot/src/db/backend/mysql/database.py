from typing import Any, List, Union, Dict

from ..base import Database

import aiomysql

async def create_mysql(
    host: str, port: int, user: str, password: str, dbname: str
) -> aiomysql.pool.Pool:

    return await aiomysql.create_pool(
        host=host, port=port, user=user, password=password, db=dbname, autocommit=True
    )

class MySqlDatabase(Database):
    def __str__(self):
        return f'{self.__class__.__name__}'

    def __init__(self, database):
        super().__init__(database)
        self.place_holder = SQL_TYPE[type(database)]['placeholder']
        self.cursor_context = SQL_TYPE[type(database)]['cursorcontext']
        self.commit_needed = SQL_TYPE[type(database)]['commit']
        self.quote = SQL_TYPE[type(database)]['quotes']
        self.pool = SQL_TYPE[type(database)]['pool']
    
    def with_commit(func):
        async def inner(self, *args, **kargs):
            response = await func(self, *args, **kargs)
            if self.commit_needed:
                await self.commit()

            return response

        return inner

    def with_cursor(func):
        async def inner(self, *args, **kargs):
            database = await self.database.acquire() if self.pool else self.database

            if self.cursor_context:
                async with database.cursor() as cursor:
                    response = await func(self, cursor, *args, **kargs)
            else:
                cursor = await database.cursor()
                response = await func(self, cursor, *args, **kargs)
                await cursor.close()

            if self.pool:
                await self.database.release(database)

            return response

        return inner


    async def commit(self):
        if not self.pool:
            await self.database.commit()


    async def close(self):
        await self.database.close()


    async def insertifnotexists(self, table_name, data, checks):
        response = await self.select(table_name, [], checks, True)

        if not response:
            return await self.insert(table_name, data)


    @with_cursor
    @with_commit
    async def insert(self, cursor, table_name, data):
        query = f"INSERT INTO {table_name} ({', '.join(data.keys())}) VALUES ({', '.join([self.place_holder] * len(data.values()))})"
        await cursor.execute(query, list(data.values()))


    @with_cursor
    @with_commit
    async def create_table(self, cursor, table_name, columns=None, not_exists=False):
        query = f'CREATE TABLE {"IF NOT EXISTS" if not_exists else ""} {self.quote}{table_name}{self.quote} ('
        columns = [] if columns is None else columns

        for column in columns:
            query += f"\n{self.quote}{column}{self.quote} {columns[column]},"

        query = query[:-1]

        query += "\n);"
        await cursor.execute(query)


    @with_cursor
    @with_commit
    async def update(self, cursor, table_name, data, checks):
        query = f"UPDATE {table_name} SET "

        if data:
            for key in data:
                query += f"{key} = {self.place_holder}, "
            query = query[:-2]

        if checks:
            query += " WHERE "
            for check in checks:
                query += f"{check} = {self.place_holder} AND "

            query = query[:-4]

        await cursor.execute(query, list(data.values()) + list(checks.values()))


    async def updateorinsert(self, table_name, data, checks, insert_data):
        response = await self.select(table_name, [], checks, True)

        if len(response) == 1:
            return await self.update(table_name, data, checks)

        return await self.insert(table_name, insert_data)


    @with_cursor
    @with_commit
    async def delete(self, cursor, table_name, checks=None):
        checks = {} if checks is None else checks

        query = f"DELETE FROM {table_name} "

        if checks:
            query += "WHERE "
            for check in checks:
                query += f"{check} = {self.place_holder} AND "

            query = query[:-4]

        await cursor.execute(query, list(checks.values()))


    @with_cursor
    async def select(self, cursor, table_name, keys, checks=None, fetchall=False):
        checks = {} if checks is None else checks

        keys = "*" if not keys else keys
        query = f"SELECT {','.join(keys)} FROM {table_name} "

        if checks:
            query += "WHERE "
            for check in checks:
                query += f"{check} = {self.place_holder} AND "

            query = query[:-4]

        await cursor.execute(query, list(checks.values()))
        columns = [x[0] for x in cursor.description]

        result = await cursor.fetchall() if fetchall else await cursor.fetchone()
        if not result:
            return result

        return (
            [dict(zip(columns, x)) for x in result]
            if fetchall
            else dict(zip(columns, result))
        )


    @with_cursor
    @with_commit
    async def execute(
        self, 
        cursor, 
        sql_query: str, 
        values: List[Any] = None, 
        fetchall: bool = True
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        await cursor.execute(sql_query, values if values is not None else [])

        result = await cursor.fetchall() if fetchall else await cursor.fetchone()
        columns = [x[0] for x in cursor.description]
        if not result:
            return result

        return (
            [dict(zip(columns, x)) for x in result]
            if fetchall
            else dict(zip(columns, result))
        )


SQL_TYPE: Dict[Any, Dict[str, Any]] = {

    aiomysql.pool.Pool: {
        "class": MySqlDatabase,
        "placeholder": "%s",
        "cursorcontext": True,
        "commit": True,
        "quotes": '`',
        "pool": True        
    }
}