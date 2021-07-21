from aiohttp import web
import recipes.aiohttp_server.views as views


def setup_routes(app: web.Application):
    app.add_routes([
        web.get('/users', views.get_all_users_handler),
        web.get('/users/{user_id}', views.get_user_profile_handler),
        web.get('/users/first_ten/', views.get_first_ten_handler),
        web.get('/recipes/{page}', views.get_active_recipes_handler),
        web.get('/recipes/{page}/sort', views.sort_recipes_handler),
        web.get('/recipes/{page}/filter', views.filter_recipes_handler),
    ])