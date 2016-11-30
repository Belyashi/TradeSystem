from sqlalchemy.orm.exc import NoResultFound

from db import session
from models import Stock


def get_tag(stock):
    return '{}-{}'.format(stock.market, stock.code).lower()


def get_by_tag(tag):
    market, code = tag.upper().split('-')
    stock = session.query(Stock).filter_by(market=market, code=code).one()
    return stock


def create_or_get_stock(market, code, name=None):
    try:
        stock = session.query(Stock).filter_by(market=market, code=code).one()
    except NoResultFound:
        stock = Stock(market=market,
                      code=code,
                      name=name)
        session.add(stock)
        session.flush()
    return stock
