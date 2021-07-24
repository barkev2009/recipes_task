import psycopg2
from recipes.utils.utils import PostgreSQLStarter
import requests

print(*str(requests.get('http://127.0.0.1:8000/api/v1/users', headers={'user': 'user_1'}).content).split('\\n'), sep='\n')