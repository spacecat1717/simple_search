"""This class created for manage Record instances (like a high_level class). It can create Record instances,
 call Record methods and do some stuff with records (including DB manipulations)"""
import asyncio
from datetime import datetime

from config.log_config import Logger as Log
from database.connection import Connection
from database.records.record import Record


class RecordManager:
    def __init__(self):
        self._connection = Connection()

    async def _create_instance(self, rubrics: str, text: str) -> Record:
        return Record(rubrics=rubrics, text=text,
                      created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    async def new_record(self, rubrics: str, text: str) -> Record or False:
        record = await self._create_instance(rubrics, text)
        if await record.save_record():
            Log.logger.info('[DB] Record %r was created', record.id)
            return record
        else:
            Log.logger.error('[DB] Could not create record, check logs')
            return False

    async def _get_record_by_id(self, record_id: int) -> Record or False:
        command = (
            "SELECT * FROM test_table3 WHERE id=$1"
        )
        async with self._connection as conn:
            res = await conn.fetch(command, record_id)
            if res:
                Log.logger.info('[DB] Record %r was found', record_id)
                return Record(record_id=res[0][0], rubrics=res[0][1], text=res[0][2], created_date=res[0][3])
            Log.logger.warning('[DB] Record %r does not exists', record_id)
            return False

    async def delete_record(self, record_id: int) -> bool:
        record = await self._get_record_by_id(record_id)
        if await record.delete_record():
            return True
        return False

    async def get_records_by_search(self, ids: list) -> list[Record]:
        pass
