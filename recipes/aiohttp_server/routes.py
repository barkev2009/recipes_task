from aiohttp import web
from recipes.aiohttp_server.views import get_all_users_handler


def setup_routes(app: web.Application):
    app.add_routes([
        web.get('/users', get_all_users_handler),
    ])