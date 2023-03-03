import asyncio
from datetime import datetime

from config.log_config import Logger as Log
from database.connection import Connection
from database.records.record import Record


class RecordManager:
    """Manage Record instances + works with Record's own methods"""
    def __init__(self):
        self._connection = Connection()

    async def _create_instance(self, rubrics: str, text: str, rec_id=None,
                               created_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")) -> Record:
        """Creates only an instance of Record class, without saving in DB"""
        return Record(record_id=rec_id, rubrics=rubrics, text=text, created_date=created_date)

    async def new_record(self, rubrics: str, text: str) -> Record or False:
        """Creates new record"""
        record = await self._create_instance(rubrics, text)
        if await record.save_record():
            Log.logger.info('[DB] Record %r was created', record.id)
            return record
        else:
            Log.logger.error('[DB] Could not create record, check logs')
            return False

    async def _get_record_by_id(self, record_id: int) -> Record or False:
        """Gets one record from DB by its id"""
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
        """Deletes record"""
        record = await self._get_record_by_id(record_id)
        if await record.delete_record():
            return True
        return False

    async def get_records_by_search(self, ids: list) -> list[dict]:
        """Gets records by search result
        :param ids: list of records ids received from ES (calls in search Blueprint)
        """
        command = (
            "SELECT * FROM test_table3 WHERE id IN {} ORDER BY created_date LIMIT 20"
        )
        async with self._connection as conn:
            sql = command.format(tuple(ids))
            res = await conn.fetch(sql)
        result = []
        for r in res:
            record = await self._create_instance(rec_id=r[0], rubrics=r[1], text=r[2], created_date=r[3])
            result.append(await record.as_dict())
        Log.logger.info('[DB] Records by search query were got')
        return result
