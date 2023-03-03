from database.connection import Connection


class ExportManager:
    """This is the base class to create child export classes """
    def __init__(self):
        self._connection = Connection()

    async def export_to(self):
        pass