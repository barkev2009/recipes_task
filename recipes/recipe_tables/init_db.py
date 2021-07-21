from recipes.utils.utils import PostgreSQLStarter
from recipes.config.config import config


def init_db():
    conn, cursor = PostgreSQLStarter(database_exists=False).get_connection_and_cursor()
    cursor.execute(f'create database {config["postgres"]["database"]}')
    conn.commit()


if __name__ == '__main__':
    init_db()
