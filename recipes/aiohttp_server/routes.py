from aiohttp import web
import recipes.aiohttp_server.views as views


def setup_routes(app: web.Application):
    app.add_routes([
        web.get('/api/v1/users', views.get_all_users_handler),
        web.get('/api/v1/users/{user_id}', views.get_user_profile_handler),
        web.get('/api/v1/users/first_ten/', views.get_first_ten_users_handler),
        web.get('/api/v1/recipes/{page}', views.get_active_recipes_handler),
        web.get('/api/v1/recipes/{page}/sort', views.sort_recipes_handler),
        web.get('/api/v1/recipes/{page}/filter', views.filter_recipes_handler),
        web.get('/api/v1/recipes/show_recipe/{recipe_id}', views.get_recipe_handler),
        web.post('/api/v1/recipes', views.add_recipe_handler),
        web.put('/api/v1/alter', views.alter_status_handler),
        web.post('/api/v1/register', views.register_user_handler),
        web.put('/api/v1/{online_status}', views.change_online_status_handler)
    ])
