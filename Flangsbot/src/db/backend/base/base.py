from abc import ABC, abstractmethod
from typing import Dict, List, Union, Optional, Any

class UnsupportedDatabase(Exception): ...
class UnstablishedDatabaseConnection(Exception): ...

class BaseDatabase(ABC):
    __slots__ = ("database",)

    def __init__(self, database):
        self.database = database

    @abstractmethod
    async def close(self): ...

    @abstractmethod
    async def insertifnotexists(
        self, 
        table_name: str, 
        data: Dict[str, Any], 
        checks: Dict[str, Any]
    ): ...

    @abstractmethod
    async def insert(
        self,
        table_name: str, 
        data: Dict[str, Any]
    ): ...

    @abstractmethod
    async def create_table(
        self,
        table_name: str,
        columns: Optional[Dict[str, str]] = None,
        exists: Optional[bool] = False,
    ): ...

    @abstractmethod
    async def update(
        self, 
        table_name: str, 
        data: Dict[str, Any], 
        checks: Dict[str, Any]
    ): ...

    @abstractmethod
    async def updateorinsert(
        self,
        table_name: str,
        data: Dict[str, Any],
        checks: Dict[str, Any],
        insert_data: Dict[str, Any],
    ): ...

    @abstractmethod
    async def delete(
        self, 
        table_name: str, 
        checks: Dict[str, Any]
    ): ...

    @abstractmethod
    async def select(
        self,
        table_name: str,
        keys: List[str],
        checks: Optional[Dict[str, Any]] = None,
        fetchall: Optional[bool] = False,
    ): ...

    @abstractmethod
    async def execute(
        self, 
        sql_query: str, 
        values: List[Any], 
        fetchall: bool = True
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]: ...
