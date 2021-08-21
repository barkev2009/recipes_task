import sqlalchemy as sql
from sqlalchemy.orm import Session
from datetime import datetime
from library.library_tables.create_tables import User, Recipe, Photo, Tag, Step, EnumStatus, EnumOnline
from library.config.config import config, FOOD_TYPES


def check_for_client_error(func):
    """
    Decorator for safe function work (returns an error message instead of raising one)
    :param func:
    :return:
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return {'message': 'failure', 'result': f'failed to proceed due to error| {e}'}
    return wrapper


def check_for_ability(user_name, active_only=False):
    """
    User validation, returns True if he is admin or active and online
    (active_only checks only for active status)
    :param user_name:
    :param active_only:
    :return:
    """
    if user_name is None:
        return False
    elif user_name == 'admin':
        return True
    else:
        check = session.query(User.status, User.online).filter(User.nickname == user_name).one()
        if any((
                all((active_only, check['status'] is EnumStatus.active)),
                all((check['status'] is EnumStatus.active, check['online'] is EnumOnline.true))
        )):
            return True
        return False


def get_all_users():
    """
    Returns all users from the database
    :return:
    """
    return session.query(User).order_by(User.id).all()


def get_user_profile(username):
    """
    Returns user profile by the username/nickname (for active users only)
    :param username:
    :return:
    """
    return session.query(User, sql.func.count(User.id)).join(Recipe). \
        filter(User.nickname == username, User.status == 'active').group_by(User.id).all()


def get_first_ten_by_recipes():
    """
    Returns the first ten active users by the quantity of their library,
    sorted in descending order
    :return:
    """
    return session.query(User, sql.func.count(User.id)) \
        .join(Recipe).order_by(sql.func.count(User.id).desc()) \
        .filter(User.status == 'active').group_by(User.id).limit(10).all()


def get_active_recipes(offset=0, limit=100, active_only=True):
    """
    Returns the table of active (or all) library, includes pagination
    :param offset:
    :param limit:
    :param active_only:
    :return:
    """
    active_query = Recipe.status == 'active' if active_only else sql.or_(Recipe.status == 'active',
                                                                         Recipe.status == 'blocked')
    return session.query(Recipe, sql.func.array_agg(Tag.tag_name)).filter(active_query) \
        .join(Tag).group_by(Recipe.id).order_by(Recipe.id).limit(limit).offset(offset * limit).all()


def sort_recipes(sort_by: str, desc=True, offset=0, limit=100, active_only=True):
    """
    Returns active (or all) library, sorted by a certain item, includes pagination
    :param sort_by: object type to sort by, can be either date, likes or name
    :param desc:
    :param offset:
    :param limit:
    :param active_only:
    :return:
    """
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
    """
    Returns active (or all) library, filtered by a certain item, includes pagination
    :param object: object type to filter by, can be either recipe_name, tag, food_type, user or photo_name
    :param filter_item: value of the object
    :param offset:
    :param limit:
    :param active_only:
    :return:
    """
    active_query = Recipe.status == 'active' if active_only else sql.or_(Recipe.status == 'active',
                                                                         Recipe.status == 'blocked')
    if 'recipe_name' in object.lower():
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
    elif 'photo_name' in object.lower():
        return session.query(Recipe, sql.func.count(Photo.photo_url)).filter(active_query).join(Photo) \
            .filter(Photo.photo_url is not None).group_by(Recipe.id) \
            .order_by(Recipe.id).limit(limit).offset(offset * limit).all()


@check_for_client_error
def alter_status(object: str, object_id: int, status: str):
    """
    Changes the status (active or blocked) of either a user or a recipe
    :param object: user or recipe
    :param object_id: active or blocked
    :param status:
    :return:
    """
    options = {'user': User, 'recipe': Recipe}
    to_alter = session.query(options[object.lower()]).get(object_id)
    to_alter.status = status
    session.add(to_alter)
    session.commit()
    return {'message': 'success', 'result': f'status of {object} (ID={object_id}) set to {status}'}


@check_for_client_error
def add_recipe(user_name, recipe_name, food_type, recipe_description=None,
               photo_data=None, tags=None, steps=None):
    """
    Adds a recipe to the database (available for online users and admin)
    :param user_id:
    :param recipe_name:
    :param food_type:
    :param recipe_description:
    :param photo_data:
    :param tags:
    :param steps:
    :return:
    """
    user_id = int(session.query(User.id).filter(User.nickname == user_name).one()[0])
    if food_type not in FOOD_TYPES:
        return {'message': 'failure', 'result': f'wrong food type'}
    new_recipe = Recipe(
        user_id=user_id, create_date=datetime.now(), recipe_name=recipe_name, food_type=food_type,
        recipe_description=recipe_description, status='active'
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


def get_recipe(recipe_id):
    """
    Returns a recipe profile by its ID
    :param recipe_id:
    :return:
    """
    tag_names = (item.__dict__['tag_name'] for item in session.query(Tag).filter(Tag.recipe_id == recipe_id).all())
    steps = (item.__dict__['step_description'] for item in
             session.query(Step).filter(Step.recipe_id == recipe_id).all())
    return session.query(Recipe,
                         sql.func.array_agg(Photo.photo_url),
                         User).join(User, Photo).group_by(User.id, Recipe.id) \
               .filter(Recipe.id == recipe_id).all(), tag_names, steps


@check_for_client_error
def register_new_user(username):
    """
    Registers a new user
    :param username:
    :return:
    """
    new_user = User(
        nickname=username,
        status='active',
        online='true'
    )
    session.add(new_user)
    session.commit()
    return {'message': 'success',
            'result': f'New user {username} successfully created'}


@check_for_client_error
def change_online_status(username, status):
    """
    Lets the active user to check in or check out of his/her profile
    :param username:
    :param status:
    :return:
    """
    session.query(User).filter(User.nickname == username, User.status != 'blocked').update(
        {'online': status}, synchronize_session='fetch'
    )
    session.commit()
    if status == 'true':
        return {'message': 'success', 'result': 'You successfully checked in'}
    return {'message': 'success', 'result': 'You successfully checked out'}


@check_for_client_error
def put_like(recipe_id):
    """
    Allows the user to put a like to a certain recipe by its ID
    :param recipe_id:
    :return:
    """
    recipe = session.query(Recipe).get(recipe_id)
    recipe.likes += 1
    session.add(recipe)
    session.commit()
    return {'message': 'success', 'result': f'like given to recipe (ID={recipe_id})'}


engine = sql.create_engine('{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}'.format(
    **config['postgres']))
session = Session(bind=engine)

if __name__ == '__main__':
    pass
    # print(*(item.__dict__['nickname'] for item in get_all_users()), sep='\n')
    # print(*(item.__dict__['recipe_name'] for item in get_active_recipes(offset=3)), sep='\n')
    # print(session.query(Recipe).filter(Recipe.status == 'active').join(User).filter(User.nickname == 'user_1').all())
    put_like(1)
