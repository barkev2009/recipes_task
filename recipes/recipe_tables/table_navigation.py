import sqlalchemy as sql
from sqlalchemy.orm import Session
from datetime import datetime
from recipes.recipe_tables.create_tables import User, Recipe, Photo, Tag, Step


def check_for_ability(user_name, block_only=False):
    if user_name is None:
        return False
    elif user_name == 'admin':
        return True
    else:
        check = session.query(User.status, User.online).filter(User.nickname == user_name).one()
        if any((
                all((block_only, str(check['status']).split('.')[-1] == 'active')),
                all((str(check['status']).split('.')[-1] == 'active', str(check['online']).split('.')[-1] == 'true'))
        )):
            return True
        return False


def get_all_users():
    return session.query(User).order_by(User.id).all()


def get_user_profile(username):
    return session.query(User, sql.func.count(User.id)).join(Recipe). \
        filter(User.nickname == username, User.status == 'active').group_by(User.id).all()


def get_first_ten_by_recipes():
    return session.query(User, sql.func.count(User.id)) \
        .join(Recipe).order_by(sql.func.count(User.id).desc()) \
        .filter(User.status == 'active').group_by(User.id).limit(10).all()


def get_active_recipes(offset=0, limit=100, active_only=True):
    active_query = Recipe.status == 'active' if active_only else sql.or_(Recipe.status == 'active',
                                                                         Recipe.status == 'blocked')
    return session.query(Recipe, sql.func.array_agg(Tag.tag_name)).filter(active_query) \
        .join(Tag).group_by(Recipe.id).order_by(Recipe.id).limit(limit).offset(offset * limit).all()


def sort_recipes(sort_by: str, desc=True, offset=0, limit=100, active_only=True):
    sort_query = ''
    active_query = Recipe.status == 'active' if active_only else sql.or_(Recipe.status == 'active',
                                                                         Recipe.status == 'blocked')
    if sort_by == 'date':
        sort_query = Recipe.create_date.desc() if desc else Recipe.create_date
    elif sort_by == 'likes':
        sort_query = Recipe.likes.desc() if desc else Recipe.likes
    elif sort_by == 'name':
        sort_query = Recipe.recipe_name.desc() if desc else Recipe.recipe_name
    return session.query(Recipe, sql.func.array_agg(Tag.tag_name)).join(Tag).group_by(Recipe.id).order_by(sort_query) \
        .filter(active_query).limit(limit).offset(offset * limit).all()


def filter_recipes(object: str, filter_item: str, offset=0, limit=100, active_only=True):
    active_query = Recipe.status == 'active' if active_only else sql.or_(Recipe.status == 'active',
                                                                         Recipe.status == 'blocked')
    if 'name' in object.lower():
        return session.query(Recipe).filter(active_query) \
            .filter(sql.or_(Recipe.recipe_name.ilike(f'%{filter_item}'),
                            Recipe.recipe_name.ilike(f'{filter_item}%'))) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'tag' in object.lower():
        return session.query(Recipe, Tag.tag_name).filter(active_query).join(Tag) \
            .filter(Tag.tag_name == filter_item) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'food_type' in object.lower():
        return session.query(Recipe).filter(active_query) \
            .filter(Recipe.food_type == filter_item) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'user' in object.lower():
        return session.query(Recipe).filter(active_query).join(User) \
            .filter(User.nickname == filter_item) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()
    elif 'photo' in object.lower():
        return session.query(Recipe, sql.func.count(Photo.photo_url)).filter(active_query).join(Photo) \
            .filter(Photo.photo_url is not None).group_by(Recipe.id) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()


def alter_status(object: str, object_id: int, status: str):
    try:
        options = {'user': User, 'recipe': Recipe}
        to_alter = session.query(options[object.lower()]).get(object_id)
        to_alter.status = status
        session.add(to_alter)
        session.commit()
        return {'message': 'success', 'result': f'status of {object} | {object_id} set to {status}'}
    except Exception as e:
        return {'message': 'failure', 'result': f'failed to proceed due to error: {e}'}


def add_recipe(user_id, recipe_name, food_type, recipe_description=None,
               photo_data=None, tags=None, steps=None):
    try:
        new_recipe = Recipe(
            user_id=user_id,
            create_date=datetime.now(),
            recipe_name=recipe_name,
            recipe_description=recipe_description,
            food_type=food_type,
            status='active'
        )
        session.add(new_recipe)
        session.commit()
        recipe_id = session.query(Recipe.id).all()[-1][0]
        if photo_data is None:
            photo_data = {'no_names': 'no_urls'}
        if tags is None:
            tags = ['no_tags']
        if steps is None:
            steps = ['no_steps']
        for k, v in photo_data.items():
            session.add(Photo(recipe_id=recipe_id, photo_name=k, photo_url=v))
            session.commit()
        for i, step in enumerate(steps):
            session.add(Step(recipe_id=recipe_id, step_number=i + 1, step_description=step))
            session.commit()
        for tag in tags:
            session.add(Tag(recipe_id=recipe_id, tag_name=tag))
            session.commit()
        return {'message': 'success', 'result': f'new recipe added'}
    except Exception as e:
        return {'message': 'failure', 'result': f'failed to proceed due to error: {e}'}


def get_recipe(recipe_id):
    tag_names = (item.__dict__['tag_name'] for item in session.query(Tag).filter(Tag.recipe_id == recipe_id).all())
    steps = (item.__dict__['step_description'] for item in
             session.query(Step).filter(Step.recipe_id == recipe_id).all())
    return session.query(Recipe,
                         sql.func.array_agg(Photo.photo_url),
                         User).join(User, Photo).group_by(User.id, Recipe.id) \
               .filter(Recipe.id == recipe_id).all(), tag_names, steps


engine = sql.create_engine('postgresql+psycopg2://postgres:1111@localhost/recipes_db_v1')
session = Session(bind=engine)

if __name__ == '__main__':
    # print(*(item.__dict__['nickname'] for item in get_all_users()), sep='\n')
    print(*(item.__dict__['recipe_name'] for item in get_active_recipes(offset=3)), sep='\n')
