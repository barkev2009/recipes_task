import pytest
import requests


def test_get_all_users():
    response = requests.get('http://127.0.0.1:8000/users', headers={'user': 'admin'})
    assert response.status_code == 200