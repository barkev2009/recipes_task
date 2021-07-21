from aiohttp import web
import recipes.recipe_tables.table_navigation as sql
from tabulate import tabulate
from recipes.config.config import *
from recipes.utils.utils import prepare_for_tab


async def get_all_users_handler(request: web.Request):
    try:
        return web.Response(
            text='\n'.join(
                ('{id} | {nickname} | {status}'.format(**item.__dict__) for item in sql.get_all_users())
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def get_user_profile_handler(request: web.Request):
    try:
        username = str(request.url).split('/')[-1]
        return web.Response(
            text='\n'.join(
                ('{} | {} | {} | {}'.format(
                    item[0].__dict__['id'],
                    item[0].__dict__['nickname'],
                    item[0].__dict__['status'],
                    item[1]
                ) for item in sql.get_user_profile(username))
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def get_first_ten_handler(request: web.Request):
    try:
        return web.Response(
            text='\n'.join(
                ('{} | {} | {} | {}'.format(
                    item[0].__dict__['id'],
                    item[0].__dict__['nickname'],
                    item[0].__dict__['status'],
                    item[1]
                ) for item in sql.get_first_ten_by_recipes())
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def get_active_recipes_handler(request: web.Request):
    try:
        offset = int(str(request.url).split('/')[-1])
        return web.Response(
            text='\n'.join(
                ('{id} | {user_id} | {recipe_name} | {create_date} | {likes} | {recipe_description} | {status}'.format(
                    **item.__dict__
                ) for item in sql.get_active_recipes(offset=offset))
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def sort_recipes_handler(request: web.Request):
    try:
        data = await request.json()
        url = str(request.url)
        offset = int(url.split('/')[-2])
        desc_query = False if data.get('desc') == 'false' else True
        return web.Response(
            text=tabulate(
                prepare_for_tab(
                    sql.sort_recipes(data['sort_by'], desc=desc_query, offset=offset),
                    RECIPE_KEYS
                ),
                headers=RECIPES_HEADERS,
                tablefmt='grid'
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def filter_recipes_handler(request: web.Request):
    try:
        data = await request.json()
        offset = int(str(request.url).split('/')[-2])
        result = sql.filter_recipes(object=data['object'], filter_item=data['item'], offset=offset)
        if data['object'] not in ['photo', 'tag']:
            return web.Response(
                text=tabulate(
                    prepare_for_tab(
                        result,
                        RECIPE_KEYS_FILTER
                    ),
                    headers=RECIPES_HEADERS,
                    tablefmt='grid'
                ),
                status=200
            )
        else:
            return web.Response(
                text=tabulate(
                    prepare_for_tab(
                        result,
                        RECIPE_KEYS_NOT_SINGLE
                    ),
                    headers=RECIPES_HEADERS,
                    tablefmt='grid'
                ),
                status=200
            )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)
