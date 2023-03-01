import asyncio
import asyncpg
import aiofiles

from aiocsv import AsyncReader

from config.config import PATH_TO_CSV
from config.log_config import Logger as Log
from database.connection import Connection


class FileExporter:
    def __init__(self):
        self._connection = Connection()

    async def export_from_csv(self) -> bool:
        Log.logger.info('Starting to export file...')
        try:
            async with aiofiles.open(PATH_TO_CSV, mode="r", encoding="utf-8", newline="") as f:
                async for row in AsyncReader(f):
                    async with self._connection as conn:
                        await conn.execute("INSERT INTO test_table3(text, created_date, rubrics) VALUES ($1, $2, $3)",
                                           row[0], row[1], row[2])
            Log.logger.info('[DB] Data from file was exported to DB')
            return True
        except Exception as e:
            Log.logger.error('[DB] Could not export data from csv file. Reason: %r', e)
            return False

