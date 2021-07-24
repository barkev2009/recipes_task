import psycopg2
from recipes.utils.utils import PostgreSQLStarter
import requests
from dotenv import dotenv_values

# print(*str(requests.get('http://127.0.0.1:8000/api/v1/users', headers={'user': 'user_1'}).content).split('\\n'), sep='\n')
print(dotenv_values()['PASSWORD'])