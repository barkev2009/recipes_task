import sqlalchemy as sql
from sqlalchemy.orm import Session
from recipes.recipe_tables.create_tables import User, Recipe, Photo, Tag, Step


def get_all_users():
    return session.query(User).order_by(User.id).all()


engine = sql.create_engine('postgresql+psycopg2://postgres:1111@localhost/recipes_db_v1')
session = Session(bind=engine)

if __name__ == '__main__':
    print(*(item.__dict__['nickname'] for item in get_all_users()), sep='\n')