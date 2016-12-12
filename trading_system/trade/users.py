from uuid import uuid4

from trading_system.models import User


def register(session):
    token = str(uuid4())
    while session.query(User).filter(User.token == token).count():
        token = str(uuid4())

    user = User(token=token)
    session.add(user)

    return token


def get_by_token(session, token):
    return session.query(User).filter(User.token == token).first()
