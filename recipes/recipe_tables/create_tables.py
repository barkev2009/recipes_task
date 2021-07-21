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


class User(Base):
    __tablename__ = 'users'
    id = sql.Column(sql.Integer(), primary_key=True)
    nickname = sql.Column(sql.Text(), nullable=False, unique=True)
    status = sql.Column(sql.Enum(EnumStatus), nullable=False)


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


def add_sample_users():
    for i in range(50):
        status = rd.choice(['active', 'blocked'])
        u = User(nickname=f'user_{i + 1}', status=status)
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


engine = sql.create_engine('postgresql+psycopg2://postgres:1111@localhost/recipes_db_v1')
session = Session(bind=engine)


if __name__ == '__main__':
    pass
    # create_tables_orm(engine)
    # add_sample_users()
    # add_sample_recipes()
    # add_sample_photos()
    # add_sample_tags()
    # print([item.__dict__['photo_url'] for item in session.query(Photo).order_by(Photo.id).all()])