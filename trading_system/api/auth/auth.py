import json

from flask.blueprints import Blueprint
from flask import request

from trading_system.api.utils import json_data
from trading_system.db import session
from trading_system.trade import users


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['POST'])
def user_register():
    data = json.loads(request.data.decode('utf-8'))
    username = data.get('username')
    passw = data.get('password')

    token = users.register(session, username, passw)
    return json_data({'token': token})


@auth.route('/login', methods=['POST'])
def user_login():
    data = json.loads(request.data.decode('utf-8'))
    username = data.get('username')
    passw = data.get('password')

    token = users.login(session, username, passw)
    if not token:
        return json_data({'error': 'auth_failed'})

    return json_data({'token': token})


@auth.route('/logout', methods=['POST'])
def user_logout():
    token = request.args.get('token')
    users.log_out(session, token)
    return 'Ok'
