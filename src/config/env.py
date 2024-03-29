import os

import toml
from envparse import env

env.read_envfile()

_env = toml.load('env.toml')


class Bot:
    _data = _env['Bot']

    token: str = _data['token']
    id = int(token.split(':')[0])
    skip_updates = _data.get('skip_updates', False)


class Database:
    _data = _env['Database']

    name = _data['name']
    username = _data.get('username')
    password = _data.get('password')
    host = os.environ['MONGO_HOST']
    port = int(os.environ['MONGO_PORT'])
    auth_source = _data.get('auth_source', 'admin')


class Users:
    _data = _env['Users']

    admins_ids = _data['admins_ids']


class Log:
    _data = _env['Log']

    file = _data.get('file')
    level = _data.get('level')
