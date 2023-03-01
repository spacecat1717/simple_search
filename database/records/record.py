"""Every record is an instance of Record class
I created save_record and delete_record methods to have an opportunity to add and remove records in DB
I thought, it might be helpful if this service will grow up or will be the base for a some big project
"""


from config.log_config import Logger as Log
from database.connection import Connection


class Record:
    def __init__(self, rubrics: str, text: str, created_date: str, record_id=None) -> None:
        self._connection = Connection()
        self.rubrics = rubrics
        self.text = text
        self.created_date = created_date
        self.id = record_id

    async def save_record(self) -> bool:
        command = (
            "INSERT INTO test_table3(rubrics, text, created_date) VALUES ($1, $2, $3) RETURNING id"
        )
        try:
            async with self._connection as conn:
                res = await conn.fetch(command, self.rubrics, self.text, self.created_date)
            self.id = res[0][0]
            Log.logger.info('[DB] Record  %r was saved', self.id)
            return True
        except Exception as e:
            Log.logger.error('[DB] Could not create record. Reason: %r', e)
            return False

    async def delete_record(self) -> bool:
        command = (
            "DELETE FROM test_table3 WHERE id = $1"
        )
        try:
            async with self._connection as conn:
                await conn.execute(command, self.id)
            Log.logger.info('[DB] Record %r was deleted', self.id)
            return True
        except Exception as e:
            Log.logger.error('[DB] Could not delete record %r. Reason: %r', self.id, e)
            return False


