from flask import request, Response
from trading_system import models as mx
from trading_system.db import session


def auth_middleware():
    token = request.args.get('token')
    result = session.query(mx.Token).filter(mx.Token.token == token).count()

    if not result:
        return 'Not Authorized', 403
