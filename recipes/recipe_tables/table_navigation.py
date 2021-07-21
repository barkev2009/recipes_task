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


def sort_recipes(sort_by: str, desc=True, offset=0, limit=100):
    sort_query = ''
    if sort_by == 'date':
        sort_query = Recipe.create_date.desc() if desc else Recipe.create_date
    elif sort_by == 'likes':
        sort_query = Recipe.likes.desc() if desc else Recipe.likes
    elif sort_by == 'name':
        sort_query = Recipe.recipe_name.desc() if desc else Recipe.recipe_name
    return session.query(Recipe, sql.func.array_agg(Tag.tag_name)).join(Tag).group_by(Recipe.id).order_by(sort_query) \
        .filter(Recipe.status == 'active').limit(limit).offset(offset * limit).all()


def filter_recipes(object: str, filter_item: str, offset=0, limit=100):
    if 'name' in object.lower():
        return session.query(Recipe).filter(Recipe.status == 'active') \
            .filter(sql.or_(Recipe.recipe_name.ilike(f'%{filter_item}'),
                            Recipe.recipe_name.ilike(f'{filter_item}%'))) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'tag' in object.lower():
        return session.query(Recipe, Tag.tag_name).filter(Recipe.status == 'active').join(Tag) \
            .filter(Tag.tag_name == filter_item) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'food_type' in object.lower():
        return session.query(Recipe).filter(Recipe.status == 'active') \
            .filter(Recipe.food_type == filter_item) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'author' in object.lower():
        return session.query(Recipe).filter(Recipe.status == 'active').join(User) \
            .filter(User.nickname == filter_item) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'photo' in object.lower():
        return session.query(Recipe, sql.func.count(Photo.photo_url)).filter(Recipe.status == 'active').join(Photo) \
            .filter(Photo.photo_url is not None).group_by(Recipe.id) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()


engine = sql.create_engine('postgresql+psycopg2://postgres:1111@localhost/recipes_db_v1')
session = Session(bind=engine)

if __name__ == '__main__':
    # print(*(item.__dict__['nickname'] for item in get_all_users()), sep='\n')
    print(*(item.__dict__['recipe_name'] for item in get_active_recipes(offset=3)), sep='\n')