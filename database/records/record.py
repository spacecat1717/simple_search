import asyncio

from config.log_config import Logger as Log
from database.connection import Connection
from elastic.elastic_class import ElasticManager


class Record:
    """Every record is an instance of Record class"""
    def __init__(self, rubrics: str, text: str, created_date: str, record_id=None) -> None:
        self._connection = Connection()
        self._es = ElasticManager()
        self.rubrics = rubrics
        self.text = text
        self.created_date = created_date
        self.id = record_id

    def __dict__(self) -> dict:
        """Overload __dict__ method for correct showing attrs data"""
        return {'id': self.id, 'rubrics': self.rubrics, 'text': self.text, 'created_date': self.created_date}

    async def as_dict(self) -> dict:
        return self.__dict__()

    async def save_record(self) -> bool:
        """Saves record in DB and ES
        I added this method because I thought, it might be helpful if this service will grow up or
         will be the base for a some big project
         """
        command = (
            "INSERT INTO test_table3(rubrics, text, created_date) VALUES ($1, $2, $3) RETURNING id"
        )
        try:
            async with self._connection as conn:
                res = await conn.fetch(command, self.rubrics, self.text, self.created_date)
            self.id = res[0][0]
            Log.logger.info('[DB] Record  %r was saved', self.id)
            await self._es.add_record(self.__dict__())
            Log.logger.info('[DB] Record %r was saved in ES', self.id)
            return True
        except Exception as e:
            Log.logger.error('[DB] Could not create record. Reason: %r', e)
            return False

    async def delete_record(self) -> bool:
        """Delete record from DB and ES"""
        command = (
            "DELETE FROM test_table3 WHERE id = $1"
        )
        if await self._es.delete_record(self.id):
            Log.logger.error('[DB] Could not delete record %r. Something went wrong with ES', self.id)
            try:
                async with self._connection as conn:
                    await conn.execute(command, self.id)
                Log.logger.info('[DB] Record %r was deleted from DB', self.id)
                return True
            except Exception as e:
                Log.logger.error('[DB] Record %r was not delete from DB, only from ES. Reason: %r', self.id, e)
                return True
        Log.logger.error('[DB] Could not delete record %r. Reason: %r', self.id, e)
        return False

