import hashlib
import datetime
from uuid import uuid4

from trading_system import models as mx


def encrypt_password(password):
    """
    :type password: unicode
    :rtype: unicode
    """
    result = hashlib.sha256(password.encode('utf-8')).digest()
    return result


def generate_token(session, user):
    token = str(uuid4())
    while session.query(mx.Token).filter(mx.Token.token == token).count():
        token = str(uuid4())

    token_record = mx.Token(
        user_id=user.id,
        token=token,
    )
    session.add(token_record)
    session.flush()

    return token


def register(session, username, password):
    user = mx.User(
        username=username,
        password=encrypt_password(password),
    )
    session.add(user)
    session.flush()

    token = generate_token(session, user)

    return token


def login(session, username, password):
    user = session.query(mx.User).filter(
        mx.User.username == username,
        mx.User.password == encrypt_password(password),
    ).first()

    if not user:
        return None

    token = generate_token(session, user)

    return token


def log_out(session, token):
    session.query(mx.Token).filter(mx.Token.token == token).delete(synchronize_session='fetch')


def get_by_token(session, token):
    result = (
        session.query(mx.User)
        .join(mx.Token, mx.Token.user_id == mx.User.id)
        .filter(
            mx.Token.token == token,
        )
        .first()
    )

    return result
