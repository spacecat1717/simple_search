import asyncio

from config.log_config import Logger as Log
from database.connection import Connection


class CreateTable:
    def __init__(self):
        self._connection = Connection()

    async def create_table(self) -> bool:
        command = (
            "CREATE TABLE IF NOT EXISTS test_table3(\
            id SERIAL,\
            rubrics TEXT,\
            text TEXT,\
            created_date VARCHAR(32)\
            )"
        )
        try:
            async with self._connection as conn:
                await conn.execute(command)
            Log.logger.info('[DB] Table was created')
            return True
        except Exception as e:
            Log.logger.error('[DB] Could not create table. reason: %r', e)
            return False
