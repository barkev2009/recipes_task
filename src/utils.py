from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from src.config.config import config


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
        """
        Returns connection and cursor instances to the user

        :return: connection and cursor for connecting to the database
        """
        return self.connection, self.cursor
