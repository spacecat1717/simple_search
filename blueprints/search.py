from quart import request, Blueprint

from database.records.record_manager import RecordManager
from elastic.elastic_class import ElasticManager

do_search = Blueprint('search', __name__)


@do_search.get('/')
async def search() -> tuple:
    """Blueprint for search request"""
    if request.args.get('q') == '':
        return {"status": "error", "type": "incorrect request"}, 400
    query = request.args.get('q')
    es = ElasticManager()
    db = RecordManager()
    record_ids = await es.search(query)
    result = await db.get_records_by_search(record_ids)
    return {"status": "ok", "data": result}, 200
