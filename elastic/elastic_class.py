import httpx

from elasticsearch import AsyncElasticsearch

from config.log_config import Logger as Log


class ElasticManager:
    """Works with ES
    Wrote as Singleton"""
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(ElasticManager, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self):
        if (self.__initialized):
            return
        self.__initialized = True
        self._url = 'http://localhost:9200'
        self._client = httpx.AsyncClient()
        self._es = AsyncElasticsearch(hosts=self._url)

    async def test_conn(self) -> bool:
        """Tests connection to ES before the service is starting
        Calls in pre_run.py
        """
        substring = 'You Know, for Search'.encode()
        async with self._client as client:
            response = await client.get(self._url)
            if substring in response.content:
                Log.logger.info('[ES] Works')
                return True
            else:
                Log.logger.error('[ES] Something went wrong with ES. Could not connect to host')
                return False

    async def create_index(self) -> bool:
        """Creates new index with config for language analysis"""
        data = {
            "mappings": {
                "properties": {
                    "iD": {
                        "type": "integer",
                        "fields": {
                            "iD": {
                                "type": "integer"
                            }
                        }
                    },
                    "text_data": {
                        "type": "text",
                        "analyzer": "russian",
                        "search_analyzer": "russian",
                        "fields": {
                            "text_data": {
                            "type": "text"
                            }
                        }
                    }
                }
            }
        }
        try:
            async with self._client as client:
                await client.put(url=f'{self._url}/records', json=data)
                Log.logger.info('[ES] Index was created')
                return True
        except Exception as e:
            Log.logger.error('[ES] Could not create index. Reason: %r', e)
            return False

    async def add_record(self, record: dict) -> bool:
        """Add one new record in ES
        :param record is a Record.as_dict() result"""
        try:
            doc = {
                "iD": record["id"],
                "text_data": record["text"]
            }
            await self._es.create(index="records", id=record["id"], document=doc)
            Log.logger.info('[ES] Record %r was saved in index', record['id'])
            return True
        except Exception as e:
            Log.logger.error('[ES] Could not save record %r in index. Reason: %r', record["id"], e)

    async def delete_record(self, rec_id: int) -> bool:
        """Delete one new record by its index"""
        try:
            await self._es.delete(index='records', id=str(rec_id))
            Log.logger.info('[ES] Record %r was deleted', rec_id)
            return True
        except Exception as e:
            Log.logger.error('[ES] Could not delete record %r. Reason: %r', rec_id, e)
            return False

    async def _convert_data(self, data: dict) -> list:
        """Convert search result with only necessary data
        :param data: raw search result"""
        ids = []
        for d in data:
            ids.append(d['_source']['iD'])
        return ids

    async def search(self, query: str) -> list or False:
        """Do search by query
         :return converted data (final result)"""
        body = {
            "query": {"match": {"text_data": query}}
        }
        try:
            res = await self._es.search(index='records', body=body, size=20)
            Log.logger.info('[ES] Query was found')
            return await self._convert_data(res['hits']['hits'])
        except Exception as e:
            Log.logger.error('[ES] Search failed. Reason: %r', e)
            return False
