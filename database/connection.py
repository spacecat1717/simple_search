import asyncpg

from config.config import DB_USER, DB_NAME, DB_PASS, DB_HOST


class Connection:
    """DB connection as Singleton"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Connection, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):

        if (self.__initialized):
            return
        self.__initialized = True
        self._db_name = DB_NAME
        self._db_user = DB_USER
        self._db_password = DB_PASS
        self._db_host = DB_HOST
        self._conn = None

    async def _get_conn(self):
        return self._conn

    conn = property(_get_conn)

    async def __aenter__(self):
        self._conn = await asyncpg.connect(database=self._db_name, user=self._db_user, password=self._db_password,
                                           host=self._db_host)
        return self._conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._conn.close()
