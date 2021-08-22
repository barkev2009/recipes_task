import sqlalchemy as sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from src.config.config import config
import random as rd
from datetime import datetime
import datetime as dt

Base = declarative_base()


class Book(Base):
    __tablename__ = 'books'
    id = sql.Column(sql.Integer(), primary_key=True)
    book_name = sql.Column(sql.Text(), nullable=False)
    book_instance = sql.Column(sql.Text(), nullable=False)
    author = sql.Column(sql.Text(), nullable=False)
    publish_name = sql.Column(sql.Text(), nullable=False)
    publish_year = sql.Column(sql.Integer(), nullable=False)


class Student(Base):
    __tablename__ = 'students'
    id = sql.Column(sql.Integer(), primary_key=True)
    first_name = sql.Column(sql.Text(), nullable=False)
    last_name = sql.Column(sql.Text(), nullable=False)
    book_taken_id = sql.Column(sql.Integer(), sql.ForeignKey('books.id'), nullable=False)
    trial_period = sql.Column(sql.Integer(), nullable=False)
    date_taken = sql.Column(sql.DateTime(), default=datetime.now(), nullable=False)
    date_returned = sql.Column(sql.DateTime(), default=datetime.now(), nullable=False)


def create_tables_orm(engine):
    Base.metadata.create_all(engine)


def drop_and_create_all():
    for func in [
            Base.metadata.drop_all,
            create_tables_orm]:
        func(engine)
        print(f'{func.__name__} - successful')
    for func in (add_sample_books, add_sample_students):
        func()
        print(f'{func.__name__} - successful')


def add_sample_books():
    books_authors = (
        ('Harry Potter 1', 'J.K. Rowling'),
        ('Harry Potter 2', 'J.K. Rowling'),
        ('Harry Potter 3', 'J.K. Rowling'),
        ('Harry Potter 4', 'J.K. Rowling'),
        ('Harry Potter 5', 'J.K. Rowling'),
        ('Martin Eden', 'Jack London'),
        ('Cabbages and Kings', 'O. Henry'),
        ('Chocolat', 'Joanne Harris'),
        ('The Chronicles of Narnia', 'C. S. Lewis'),
        ('The Lord of the Rings', 'J. R. R. Tolkien'),
        ('Dracula', 'Bram Stoker')
    )
    for i in range(500):
        book_author = rd.choice(books_authors)
        book = Book(
            book_name=book_author[0] if i < 450 else 'Dracula',
            book_instance=rd.randrange(10000),
            author=book_author[1] if i < 450 else 'Bram Stoker',
            publish_name='Bloomberg',
            publish_year=2012 if book_author[0] != 'Dracula' else 2013
        )
        session.add(book)
        session.commit()


def add_sample_students():
    names = ('Anna Kapinos', 'Greg Kovshov', 'Ilya Indyk', 'Gleb Rudaev', 'Marina Glukhikh',
             'Alexandr Shevtsov', 'Lera Scherbakova', 'Olga Nosova')
    for i in range(1000):
        name = rd.choice(names)
        book_id = rd.randrange(500) + 1
        trial_period = rd.randrange(7, 31)
        return_period = rd.choice([7, 10, 20, 40]) if name != 'Greg Kovshov' else 1000
        date_taken = datetime.now() if book_id < 450 else datetime.now() - dt.timedelta(days=365)
        stud = Student(
            first_name=name.split(' ')[0],
            last_name=name.split(' ')[1],
            book_taken_id=book_id,
            trial_period=trial_period,
            date_taken=date_taken,
            date_returned=date_taken + dt.timedelta(days=return_period)
        )
        session.add(stud)
        session.commit()


engine = sql.create_engine('{dialect}+{driver}://{user}:{password}@{host}/{database}'.format(**config['postgres']))
session = Session(bind=engine)

if __name__ == '__main__':
    pass
    drop_and_create_all()
