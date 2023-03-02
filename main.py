import asyncio
import logging

from quart import Quart
from quart_cors import cors

from blueprints.search import do_search

logging.basicConfig(level=logging.DEBUG)

app = Quart(__name__, static_url_path='/')
app = cors(app, allow_origin='*')
app.register_blueprint(do_search, url_prefix='/search')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
