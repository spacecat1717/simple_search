import asyncio

from database.create_table import CreateTable
from database.export_data.export_from_file import FileExporter

exporter = FileExporter()
table = CreateTable()

if __name__ == "__main__":
    asyncio.run(table.create_table())
    asyncio.run(exporter.export_from_csv())
    #TODO: add quart app here
