import asyncio
import httpx

from config.log_config import Logger as Log


class ElasticManager:
    def __init__(self):
        self._url = 'http://localhost:9200'

    async def test_conn(self) -> bool:
        substring = 'You Know, for Search'.encode()
        async with httpx.AsyncClient() as client:
            response = await client.get(self._url)
            if substring in response.content:
                Log.logger.info('[ES] Works')
                return True
            else:
                Log.logger.error('[ES] Something went wrong with ES. Could not connect to host')
                return False

    async def create_index(self) -> bool:
        data = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "russian",
                        "search_analyzer": "russian",
                        "fields": {
                            "keyword": {
                            "type": "keyword",
                            "ignore_above": 256
                            }
                        }
                    },
            "content": {
                "type": "text",
                "analyzer": "russian",
                "search_analyzer": "russian",
                "fields": {
                "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                            }
                        }
                    }
                }
            }
        }
        try:
            async with httpx.AsyncClient() as client:
                await client.put(url=f'{self._url}/records', json=data)
                Log.logger.info('[ES] Index was created')
                return True
        except Exception as e:
            Log.logger.error('[ES] Could not create index. Reason: %r', e)
            return False

    async def add_record(self, record: dict) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                await client.post(url=f'{self._url}/records/{record["id"]}', json=record)
                Log.logger.info('[ES] Record %r was saved in index', record['id'])
                return True
        except Exception as e:
            Log.logger.error('[ES] Could not save record %r in index. Reason: %r', record["id"], e)

    async def delete_record(self, rec_id: int) -> bool:
        try:
            async with httpx.AsyncClient() as client:
                await client.delete(url=f'{self._url}/records/{rec_id}')
                Log.logger.info('[ES] Record %r was deleted', rec_id)
                return True
        except Exception as e:
            Log.logger.error('[ES] Could not delete record %r. Reason: %r', rec_id, e)
            return False



e = ElasticManager()
asyncio.run(e.delete_record(100))
