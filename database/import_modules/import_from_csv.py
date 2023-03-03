import asyncio
import aiofiles

from aiocsv import AsyncReader

from config.log_config import Logger as Log
from database.import_modules.base_class import ImportManager


class ImportFromCsv(ImportManager):
    """Inports data from csv file to DB"""

    async def import_from_file(self, filepath: str) -> bool:
        Log.logger.info('Starting to import file...')
        try:
            async with aiofiles.open(filepath, mode="r", encoding="utf-8", newline="") as f:
                async for row in AsyncReader(f):
                    async with self._connection as conn:
                        await conn.execute("INSERT INTO test_table3(text, created_date, rubrics) VALUES ($1, $2, $3)",
                                           row[0], row[1], row[2])
            Log.logger.info('[DB] Data from file was exported to DB')
            return True
        except Exception as e:
            Log.logger.error('[DB] Could not import data from csv file. Reason: %r', e)
            return False



