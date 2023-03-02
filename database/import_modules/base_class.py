from database.connection import Connection


class ImportManager:
    """This is the base class to create child import classes (open/close principle)"""
    def __init__(self):
        self._connection = Connection()

    async def import_from_file(self, filepath: str):
        pass
