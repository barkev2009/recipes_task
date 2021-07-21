from aiohttp import web
from recipes.recipe_tables.table_navigation import get_all_users


async def get_all_users_handler(request: web.Request):
    try:
        return web.Response(
            text='\n'.join(
                ('{id} | {nickname} | {status}'.format(**item.__dict__) for item in get_all_users())
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)
