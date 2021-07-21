from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from recipes.config.config import config


class PostgreSQLStarter:
    """
    Class to start and return connection and cursor instances from psycopg2
    depending on the existence of the database
    """

    def __init__(self, database_exists=True,
                 user=config['postgres']['user'],
                 password=config['postgres']['password'],
                 host=config['postgres']['host'],
                 port=config['postgres']['port'],
                 database=config['postgres']['database']):
        self.database_exists = database_exists
        if self.database_exists:
            self.connection = connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port,
                                      database=database)
            self.cursor = self.connection.cursor()
        else:
            self.connection = connect(user=user,
                                      password=password,
                                      host=host,
                                      port=port)
            self.connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            self.cursor = self.connection.cursor()

    def get_connection_and_cursor(self):
        return self.connection, self.cursor


def prepare_for_tab(data, values):
    output_list = []
    if 'tuple' in str(type(values[0])) or 'list' in str(type(values[0])):
        for item in data:
            to_append = []
            for value in values:
                if 'tuple' in str(type(value)) or 'list' in str(type(value)):
                    if 'list' not in value:
                        to_append.append(item[value[0]].__dict__[value[1]])
                    else:
                        to_append.append('\n'.join(item[value[0]]))
                else:
                    to_append.append(item[value])
            output_list.append(to_append)
    else:
        for item in data:
            output_list.append([item.__dict__[value] for value in values])
    return output_list
