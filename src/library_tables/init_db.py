from src.config import config
from src.utils import PostgreSQLStarter


def init_db():
    """
    Initializes the library database
    """
    conn, cursor = PostgreSQLStarter(database_exists=False).get_connection_and_cursor()
    cursor.execute(f'create database {config["postgres"]["database"]}')
    conn.commit()
    print(f'Database {config["postgres"]["database"]} successfully created')


if __name__ == '__main__':
    init_db()
