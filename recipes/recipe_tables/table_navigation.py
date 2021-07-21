import sqlalchemy as sql
from sqlalchemy.orm import Session
from recipes.recipe_tables.create_tables import User, Recipe, Photo, Tag, Step


def get_all_users():
    return session.query(User).order_by(User.id).all()


def get_user_profile(username):
    return session.query(User, sql.func.count(User.id)).join(Recipe). \
        filter(User.nickname == username, User.status == 'active').group_by(User.id).all()


def get_first_ten_by_recipes():
    return session.query(User, sql.func.count(User.id)) \
        .join(Recipe).order_by(sql.func.count(User.id).desc()) \
        .filter(User.status == 'active').group_by(User.id).limit(10).all()


def get_active_recipes(offset=0, limit=100):
    return session.query(Recipe).filter(Recipe.status == 'active') \
        .order_by(Recipe.id).limit(limit).offset(offset * limit).all()


engine = sql.create_engine('postgresql+psycopg2://postgres:1111@localhost/recipes_db_v1')
session = Session(bind=engine)

if __name__ == '__main__':
    # print(*(item.__dict__['nickname'] for item in get_all_users()), sep='\n')
    print(*(item.__dict__['recipe_name'] for item in get_active_recipes(offset=3)), sep='\n')