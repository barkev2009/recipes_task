from library.utils.utils import PostgreSQLStarter
from library.config.config import config


def init_db():
    conn, cursor = PostgreSQLStarter(database_exists=False).get_connection_and_cursor()
    cursor.execute(f'create database {config["postgres"]["database"]}')
    conn.commit()
    print(f'Database {config["postgres"]["database"]} successfully created')


if __name__ == '__main__':
    init_db()
