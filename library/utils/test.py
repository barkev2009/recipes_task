import psycopg2
from library.utils.utils import PostgreSQLStarter
import requests
import json
from dotenv import dotenv_values

# print(*str(requests.get('http://127.0.0.1:8000/api/v1/users', headers={'user': 'user_1'}).content).split('\\n'), sep='\n')
response = requests.put('http://127.0.0.1:8000/api/v1/alter',
                        headers={'user': 'admin', 'password': '5556'},
                        json=json.dumps({'object': 'recipe',
                                         'id': 1,
                                         'status': 'blocked'}))
print(response.status_code)
