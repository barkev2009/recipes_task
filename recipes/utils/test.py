import psycopg2
from recipes.utils.utils import PostgreSQLStarter

conn, cursor = PostgreSQLStarter().get_connection_and_cursor()
cursor.execute('SELECT version();')
print(cursor.fetchone())