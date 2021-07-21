from aiohttp import web
from recipes.config.config import config
from recipes.aiohttp_server.routes import setup_routes


if __name__ == '__main__':
    app = web.Application()
    setup_routes(app)
    web.run_app(app, host=config['server']['host'], port=config['server']['port'])
