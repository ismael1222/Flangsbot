from typing import Any, Dict, List, Union

from ..base import Database

from motor.motor_asyncio import AsyncIOMotorClient

class _MongoDatabase(Database):
    def __str__(self):
        return f"<{self.__class__.__name__} '{self.name}'>"
        
    def __init__(self, database):
        super().__init__(self, database)
        self.database = database

    @property
    def name(self):
        return self.database.name

    async def close(self):
        self.database.client.close()

    async def insertifnotexists(self, table_name, data, checks):
        response = await self.select(table_name, [], checks, True)

        if not response:
            return await self.insert(table_name, data)

    async def insert(self, table_name, data):
        return await self.database[table_name].insert_one(data)

    async def create_table(self, table_name, _=None, exists=False):
        # create_table has an unused positional parameter to make the methods consistent between database types.

        if exists and table_name in await self.database.list_collection_names():
            return

        return await self.database.create_collection(table_name)

    async def update(self, table_name, data, checks):
        return await self.database[table_name].update_one(checks, {"$set": data})

    async def updateorinsert(self, table_name, data, checks, insert_data):
        response = await self.select(table_name, [], checks, True)

        if len(response) == 1:
            return await self.update(table_name, data, checks)

        return await self.insert(table_name, insert_data)

    async def delete(self, table_name, checks=None):
        return await self.database[table_name].delete_one(
            {} if checks is None else checks
        )

    async def select(self, table_name, keys, checks=None, fetchall=False):
        checks = {} if checks is None else checks

        if fetchall:
            fetch = self.database[table_name].find(checks)
            result = []

            async for doc in fetch:
                current_doc = {}

                for key, value in doc.items():
                    if not keys or key in keys:
                        current_doc[key] = value

                result.append(current_doc)
        else:
            fetch = await self.database[table_name].find_one(checks)
            result = {}

            if fetch is not None:
                for key, value in fetch.items():
                    if not keys or key in keys:
                        result[key] = value
            else:
                result = None

        return result

    async def execute(
        self, sql_query: str, values: List[Any], fetchall: bool = True
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        raise NotImplementedError("NoSQL databases cannot execute sql queries.")

MONGO_TYPE: Dict[Any, Dict[str, Any]] = {
    AsyncIOMotorClient: _MongoDatabase,
}