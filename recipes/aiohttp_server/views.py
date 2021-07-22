from aiohttp import web
import recipes.recipe_tables.table_navigation as sql
from tabulate import tabulate
from recipes.config.config import *
from recipes.utils.utils import prepare_for_tab
import json


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


async def alter_status_handler(request: web.Request):
    try:
        data = await request.json()
        if all([request.headers.get('token') == config['admin_data']['password'],
                request.headers.get('user') == 'admin']):
            result = sql.alter_status(data['object'], int(data['id']), data['status'])
            if result['message'] == 'success':
                return web.Response(text=json.dumps(result, indent=4), status=200)
            else:
                return web.Response(text=json.dumps(result, indent=4), status=418)
        else:
            return web.Response(text=json.dumps({'message': 'failure',
                                                 'result': 'not authorized to alter status'}, indent=4),
                                status=401)
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def add_recipe_handler(request: web.Request):
    try:
        data = await request.json()
        result = sql.add_recipe(int(data['id']), data['name'], data['type'], data.get('descr'))
        if result['message'] == 'success':
            return web.Response(text=json.dumps(result, indent=4), status=200)
        else:
            return web.Response(text=json.dumps(result, indent=4), status=418)
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)


async def get_recipe_handler(request: web.Request):
    try:
        url = str(request.url)
        recipe_id = int(url.split('/')[-1])
        main_block, tag_block, step_block = sql.get_recipe(recipe_id)
        to_tabulate = prepare_for_tab(
            main_block,
            ((0, 'id'), (2, 'id'), (2, 'nickname'), (2, 'status'), (0, 'recipe_name'), (0, 'recipe_description'),
             (1, 'list'), (0, 'likes'), (0, 'create_date'), (0, 'food_type'), (0, 'status'))
        )
        to_tabulate[0].insert(-4, '\n'.join(tag_block))
        to_tabulate[0].append('\n'.join(step_block))
        return web.Response(
            text=tabulate(
                to_tabulate,
                headers=('Recipe ID', 'User ID', 'User Nickname', 'User Status', 'Recipe Name', 'Recipe Description',
                         'Recipe Photos', 'Recipe Tags', 'Likes', 'Creation Date', 'Food Type', 'Recipe Status', 'Steps'),
                # tablefmt='grid'
            ),
            status=200
        )
    except Exception as e:
        return web.Response(text=f'Failed to respond to the request: {e}', status=500)
