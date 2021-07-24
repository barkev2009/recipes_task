import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
import random as rd
import enum
from datetime import datetime

Base = declarative_base()


class EnumStatus(enum.Enum):
    active, blocked = 'active', 'blocked'


class EnumFoodType(enum.Enum):
    salad, first_course, main_course = 'salad', 'first_course', 'main_course'
    soup, dessert, drink = 'soup', 'dessert', 'drink'


class EnumOnline(enum.Enum):
    true, false = 'true', 'false'


class User(Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer(), primary_key=True)
    nickname = sql.Column(sql.Text(), nullable=False, unique=True)
    status = sql.Column(sql.Enum(EnumStatus), nullable=False)
    online = sql.Column(sql.Enum(EnumOnline), nullable=False)


class Recipe(Base):
    __tablename__ = 'recipes'
    id = sql.Column(sql.Integer(), primary_key=True)
    user_id = sql.Column(sql.Integer(), sql.ForeignKey('users.id'), nullable=False)
    create_date = sql.Column(sql.DateTime(), default=datetime.now(), nullable=False)
    recipe_name = sql.Column(sql.String(50), nullable=False)
    recipe_description = sql.Column(sql.Text(), default='No text added')
    food_type = sql.Column(sql.Enum(EnumFoodType), nullable=False)
    likes = sql.Column(sql.Integer(), default=0)
    status = sql.Column(sql.Enum(EnumStatus), nullable=False)


class Photo(Base):
    __tablename__ = 'photos'
    id = sql.Column(sql.Integer(), primary_key=True)
    recipe_id = sql.Column(sql.Integer(), sql.ForeignKey('recipes.id'), nullable=False)
    photo_name = sql.Column(sql.String(100))
    photo_url = sql.Column(sql.Text(), nullable=False)


class Step(Base):
    __tablename__ = 'steps'
    id = sql.Column(sql.Integer(), primary_key=True)
    recipe_id = sql.Column(sql.Integer(), sql.ForeignKey('recipes.id'), nullable=False)
    step_number = sql.Column(sql.Integer(), nullable=False)
    step_description = sql.Column(sql.Text())


class Tag(Base):
    __tablename__ = 'tags'
    id = sql.Column(sql.Integer(), primary_key=True)
    recipe_id = sql.Column(sql.Integer(), sql.ForeignKey('recipes.id'), nullable=False)
    tag_name = sql.Column(sql.String(50), nullable=False)


def create_tables_orm(engine):
    Base.metadata.create_all(engine)


def drop_and_create_all():
    for func in [
            # Base.metadata.drop_all,
            create_tables_orm]:
        func(engine)
        print(f'{func.__name__} - successful')
    for func in (add_sample_users, add_sample_recipes, add_sample_tags, add_sample_photos, add_sample_steps):
        func()
        print(f'{func.__name__} - successful')


def add_sample_users():
    options = {0: 'active', 1: 'blocked'}
    for i in range(50):
        status = options[i] if i == 0 or i == 1 else rd.choice(['active', 'blocked'])
        if status == 'blocked':
            online = 'false'
        else:
            online = rd.choice(['true', 'false'])
        u = User(nickname=f'user_{i + 1}', status=status, online=online)
        session.add(u)
        session.commit()


def add_sample_recipes():
    for i in range(500):
        status = rd.choice(['active', 'blocked'])
        food_type = rd.choice(['salad', 'first_course', 'main_course', 'soup', 'dessert', 'drink'])
        r = Recipe(
            user_id=rd.randint(1, 50),
            recipe_name=f'recipe_name_{i + 1}',
            food_type=food_type,
            likes=rd.randint(0, 100),
            status=status
        )
        session.add(r)
        session.commit()


def add_sample_tags():
    for i in range(2000):
        t = Tag(
            recipe_id=rd.randint(1, 500),
            tag_name=f'tagname_{rd.randint(1, 20)}'
        )
        session.add(t)
        session.commit()


def add_sample_photos():
    for i in range(2000):
        p = Photo(
            recipe_id=rd.randint(1, 500),
            photo_name=f'photoname_{i + 1}',
            photo_url=f'photo_url_{i + 1}'
        )
        session.add(p)
        session.commit()


def add_sample_steps():
    for i in range(500):
        for k in range(rd.randint(1, 7)):
            step = Step(
                recipe_id=i + 1,
                step_number=k,
                step_description=f'descr_step_{k}_recipe_{i}'
            )
            session.add(step)
            session.commit()


engine = sql.create_engine('postgresql+psycopg2://postgres:1111@localhost/recipes_db_v1')
session = Session(bind=engine)

if __name__ == '__main__':
    pass
    drop_and_create_all()
    # create_tables_orm(engine)
    # add_sample_users()
    # add_sample_recipes()
    # add_sample_photos()
    # add_sample_tags()
    # print([item.__dict__['photo_url'] for item in session.query(Photo).order_by(Photo.id).all()])
