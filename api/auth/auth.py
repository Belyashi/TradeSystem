from flask.blueprints import Blueprint

import trade
from db import session
from utils import json_data


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register')
def user_register():
    token = trade.users.register(session)
    return json_data({'token': token})
