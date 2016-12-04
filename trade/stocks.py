from sqlalchemy.orm.exc import NoResultFound

from models import Stock


def get_by_tag(session, tag):
    market, code = tag.upper().split('-')
    stock = session.query(Stock).filter_by(market=market, code=code).one()
    return stock


def create_or_get_stock(session, market, code, name=None):
    try:
        stock = session.query(Stock).filter_by(market=market, code=code).one()
    except NoResultFound:
        stock = Stock(market=market,
                      code=code,
                      name=name)
        session.add(stock)
        session.flush()
    return stock


def create_stocks(session, stocks):
    for item in stocks:
        create_or_get_stock(session, **item)
