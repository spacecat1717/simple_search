"""This script do some job before the service is running"""

import asyncio

from config.config import PATH_TO_CSV
from config.log_config import Logger as Log
from database.create_table import CreateTable
from database.import_modules.import_from_csv import ImportFromCsv
from database.export_modules.export_to_elastic import ExportToElasticsearch
from elastic.elastic_class import ElasticManager


async def prepare_to_run():
    create_table = CreateTable()
    import_data = ImportFromCsv()
    export_to_es = ExportToElasticsearch()
    es = ElasticManager()
    #creates DB table
    await create_table.create_table()
    await asyncio.sleep(0.5)
    #imports data from csv
    await import_data.import_from_file(PATH_TO_CSV)
    await asyncio.sleep(0.5)
    #exports data from DB to ES
    await export_to_es.export_to()
    await asyncio.sleep(0.5)
    #tests connection to ES
    if not await es.test_conn():
        raise("There is no connection to ES! Please, check logs!")
    else:
        await es.create_index()

if __name__ == "__main__":
    asyncio.run(prepare_to_run())
