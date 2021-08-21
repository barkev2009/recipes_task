import sqlalchemy as sql
from sqlalchemy.orm import Session
import numpy as np
from numpy_groupies import aggregate
from datetime import datetime
import datetime as dt
from library.library_tables.create_tables import Book, Student
from library.config.config import config
from tabulate import tabulate


def calculate_fowls():
    query = np.array(session.query(Student.date_taken, Student.date_returned, Student.trial_period,
                                   Student.first_name, Student.last_name).order_by(Student.first_name).all())
    reading_period = (query[:, 1] - query[:, 0]).astype('timedelta64[D]')
    trial_period = np.array([item.value for item in query[:, 2]])
    days_fowled = (reading_period - trial_period).astype('int')
    days_fowled = np.where(days_fowled < 0, 0, days_fowled)
    full_names = query[:, -2] + ' ' + query[:, -1]
    table = np.dstack([days_fowled, full_names]).reshape(days_fowled.shape[0], 2)

    group_names = np.unique(full_names)
    overall_days = []
    for name in group_names:
        overall_days.append(np.sum(np.where((table[:, 1] == name), table[:, 0], 0)))
    table = np.dstack([np.array(overall_days), group_names]).reshape(group_names.shape[0], 2)

    print(tabulate(
        table,
        headers=['Days of not return', 'Full name']
    ))


def test_query():
    query = session.query()
    test = session.query(Student.trial_period).all()
    print(query)


engine = sql.create_engine('{dialect}+{driver}://{user}:{password}@{host}:{port}/{database}'.format(
    **config['postgres']))
session = Session(bind=engine)

if __name__ == '__main__':
    pass
    calculate_fowls()
    # test_query()