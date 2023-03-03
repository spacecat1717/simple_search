from quart import request, Blueprint

from database.records.record_manager import RecordManager

delete_record = Blueprint('delete', __name__)


@delete_record.get('/')
async def delete_rec() -> tuple:
    """Blueprint for delete request"""
    rec_id = request.args.get('rec_id')
    db = RecordManager()
    if await db.delete_record(int(rec_id)):
        return {'status': 'ok'}, 200
    return {'status': 'error'}, 500
