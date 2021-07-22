from aiohttp import web
import recipes.recipe_tables.table_navigation as sql
from tabulate import tabulate
from recipes.config.config import *
import recipes.utils.utils as utils
import json


@utils.user_validation_wrapper
async def get_all_users_handler(request: web.Request):
    return web.Response(
        text=tabulate(
            utils.prepare_for_tab(
                sql.get_all_users(),
                ('id', 'nickname', 'status', 'online')
            ),
            headers=USERS_AND_QUANTITY_HEADERS[:-1],
            tablefmt='grid'
        ),
        status=200
    )


@utils.user_validation_wrapper
async def get_user_profile_handler(request: web.Request):
    url = request.url
    username = str(url).split('/')[-1]
    return web.Response(
        text=tabulate(
            utils.prepare_for_tab(
                sql.get_user_profile(username),
                ((0, 'id'), (0, 'nickname'), (0, 'status'), (0, 'online'), 1)
            ),
            headers=USERS_AND_QUANTITY_HEADERS,
            tablefmt='grid'
        ),
        status=200
    )


@utils.user_validation_wrapper
async def get_first_ten_users_handler(request: web.Request):
    return web.Response(
        text=tabulate(
            utils.prepare_for_tab(
                sql.get_first_ten_by_recipes(),
                ((0, 'id'), (0, 'nickname'), (0, 'status'), (0, 'online'), 1)
            ),
            headers=USERS_AND_QUANTITY_HEADERS,
            tablefmt='grid'
        ),
        status=200
    )


@utils.user_validation_wrapper
async def get_active_recipes_handler(request: web.Request):
    data = await request.json()
    url = str(request.url)
    active_only = False if data.get('active_only') == 'false' else True
    offset = int(url.split('/')[-1])
    return web.Response(
        text=tabulate(
            utils.prepare_for_tab(
                sql.get_active_recipes(offset, active_only=active_only),
                RECIPE_KEYS
            ),
            headers=RECIPES_HEADERS,
            tablefmt='grid'
        ),
        status=200
    )


@utils.user_validation_wrapper
async def sort_recipes_handler(request: web.Request):
    data = await request.json()
    url = str(request.url)
    offset = int(url.split('/')[-2])
    active_only = False if data.get('active_only') == 'false' else True
    desc_query = False if data.get('desc') == 'false' else True
    return web.Response(
        text=tabulate(
            utils.prepare_for_tab(
                sql.sort_recipes(data['sort_by'], desc=desc_query, offset=offset, active_only=active_only),
                RECIPE_KEYS
            ),
            headers=RECIPES_HEADERS,
            tablefmt='grid'
        ),
        status=200
    )


@utils.user_validation_wrapper
async def filter_recipes_handler(request: web.Request):
    data = await request.json()
    offset = int(str(request.url).split('/')[-2])
    active_only = False if data.get('active_only') == 'false' else True
    result = sql.filter_recipes(object=data['object'], filter_item=data['item'],
                                offset=offset, active_only=active_only)
    if data['object'] not in ['photo', 'tag']:
        return web.Response(
            text=tabulate(
                utils.prepare_for_tab(
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
                utils.prepare_for_tab(
                    result,
                    RECIPE_KEYS_NOT_SINGLE
                ),
                headers=RECIPES_HEADERS,
                tablefmt='grid'
            ),
            status=200
        )


@utils.standard_validation_wrapper
async def alter_status_handler(request: web.Request):
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


@utils.user_validation_wrapper
async def add_recipe_handler(request: web.Request):
    data = await request.json()
    result = sql.add_recipe(int(data['id']),
                            data['name'],
                            data['type'],
                            data.get('descr'),
                            photo_data=data.get('photo_data'),
                            steps=data.get('steps'),
                            tags=data.get('tags'))
    if result['message'] == 'success':
        return web.Response(text=json.dumps(result, indent=4), status=200)
    else:
        return web.Response(text=json.dumps(result, indent=4), status=418)


@utils.user_validation_wrapper
async def get_recipe_handler(request: web.Request):
    url = str(request.url)
    recipe_id = int(url.split('/')[-1])
    main_block, tag_block, step_block = sql.get_recipe(recipe_id)
    to_tabulate = utils.prepare_for_tab(
        main_block,
        ((0, 'id'), (2, 'id'), (2, 'nickname'), (2, 'status'), (0, 'recipe_name'), (0, 'recipe_description'),
         (1, 'list'), (0, 'likes'), (0, 'create_date'), (0, 'food_type'), (0, 'status'))
    )
    to_tabulate[0].insert(-4, '\n'.join(tag_block))
    to_tabulate[0].append('\n'.join(step_block))
    return web.Response(
        text=tabulate(
            to_tabulate,
            headers=('Recipe ID', 'User ID', 'User Nickname', 'User Status', 'Recipe Name',
                     'Recipe Description', 'Recipe Photos', 'Recipe Tags', 'Likes', 'Creation Date',
                     'Food Type', 'Recipe Status', 'Steps'),
            # tablefmt='grid'
        ),
        status=200
    )


@utils.standard_validation_wrapper
async def register_user_handler(request: web.Request):
    data = await request.json()
    result = sql.register_new_user(data['new_nickname'])
    if result['message'] == 'success':
        return web.Response(text=json.dumps(result, indent=4), status=200)
    else:
        return web.Response(text=json.dumps(result, indent=4), status=418)


@utils.user_validation_block_only_wrapper
async def change_online_status_handler(request: web.Request):
    options = {'online': 'true', 'offline': 'false'}
    status = options[str(request.url).split('/')[-1]]
    result = sql.change_online_status(request.headers.get('user'), status)
    if result['message'] == 'success':
        return web.Response(text=json.dumps(result, indent=4), status=200)
    else:
        return web.Response(text=json.dumps(result, indent=4), status=418)
