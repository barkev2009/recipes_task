from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from recipes.config.config import config
from aiohttp import web
import recipes.recipe_tables.table_navigation as sql
import json


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
        :return:
        """
        return self.connection, self.cursor


def prepare_for_tab(data, values):
    """
    Prepares data for printing with the help of 'tabulate' function
    :param data:
    :param values:
    :return:
    """
    output_list = []
    if type(values[0]) is tuple or type(values[0]) is list:
        for item in data:
            to_append = []
            for value in values:
                if type(value) is tuple or type(value) is list:
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


def standard_validation_wrapper(func):
    """
    Decorator for standard Internal Error response
    :param func:
    :return:
    """
    async def wrapper(request: web.Request):
        try:
            return await func(request)
        except Exception as e:
            return web.Response(text=json.dumps({'message': 'failure', 'result': str(e)}), status=500)

    return wrapper


def user_validation_wrapper(func):
    """
    Decorator for validating the user (check if he is online and not blocked)
    :param func:
    :return:
    """
    async def wrapper(request: web.Request):
        try:
            if sql.check_for_ability(request.headers.get('user')):
                return await func(request)
            else:
                return web.Response(
                    text=json.dumps({'message': 'failed to authenticate'}, indent=4),
                    status=401
                )
        except Exception as e:
            return web.Response(text=json.dumps({'message': 'failure', 'result': str(e)}), status=500)

    return wrapper


def user_validation_block_only_wrapper(func):
    """
    Decorator for validating the user (check if he is online)
    :param func:
    :return:
    """
    async def wrapper(request: web.Request):
        try:
            if sql.check_for_ability(request.headers.get('user'), active_only=True):
                return await func(request)
            else:
                return web.Response(
                    text=json.dumps({'message': 'failed to authenticate, blocked user'}, indent=4),
                    status=401
                )
        except Exception as e:
            return web.Response(text=json.dumps({'message': 'failure', 'result': str(e)}), status=500)

    return wrapper
