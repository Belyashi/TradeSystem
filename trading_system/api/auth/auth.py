from flask.blueprints import Blueprint

from trading_system.api.utils import json_data
from trading_system.db import session


auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register')
def user_register():
    token = trading_system.trade.users.register(session)
    return json_data({'token': token})
