from uuid import uuid4

from db import session
from models import User


def register():
    token = str(uuid4())
    while session.query(User).filter(User.token == token).count():
        token = str(uuid4())

    user = User(token=token)
    session.add(user)

    return token


def get_by_token(token):
    return session.query(User).filter(User.token == token).first()
