from sqlalchemy.orm.exc import NoResultFound

from trading_system.models import Balance, StockBalance


def get_money(session, user_id):
    try:
        balance = session.query(Balance).filter_by(user_id=user_id).one()
        return balance.value
    except NoResultFound:
        return 0.


def get_stocks(session, user_id, stock_id):
    try:
        balance = session.query(StockBalance).filter_by(user_id=user_id, stock_id=stock_id).one()
        return balance.value
    except NoResultFound:
        return 0


def transfer_money(session, user_id, delta):
    try:
        balance = session.query(Balance).filter_by(user_id=user_id).one()
        balance.value += delta
    except NoResultFound:
        balance = Balance(user_id=user_id, value=delta)
        session.add(balance)


def transfer_stocks(session, user_id, stock_id, delta):
    try:
        balance = session.query(StockBalance).filter_by(user_id=user_id, stock_id=stock_id).one()
        balance.value += delta
    except NoResultFound:
        balance = StockBalance(user_id=user_id, stock_id=stock_id, value=delta)
        session.add(balance)
