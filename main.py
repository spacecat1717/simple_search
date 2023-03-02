import asyncio

from database.create_table import CreateTable

table = CreateTable()

if __name__ == "__main__":
    asyncio.run(table.create_table())
    #TODO: add quart app here
