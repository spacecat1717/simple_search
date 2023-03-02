import asyncio

from config.log_config import Logger as Log
from database.export_modules.base_class import ExportManager
from elastic.elastic_class import ElasticManager


class ExportToElasticsearch(ExportManager):

    def __init__(self):
        super().__init__()
        self._es = ElasticManager()

    async def export_to(self):
        command = (
            "SELECT id, text  FROM test_table3"
        )
        async with self._connection as conn:
            records = await conn.fetch(command)
        for rec in records[1::]:
            await self._es.add_record({'id': rec[0],
                                      'text': rec[1]
                                      })

