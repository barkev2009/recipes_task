from aiohttp import web
import recipes.recipe_tables.table_navigation as sql


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
