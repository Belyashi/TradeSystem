import logging

from sqlalchemy.orm.exc import NoResultFound

from db import engine, session
from models import Base, Stock
from history import update_stocks_history


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


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s')

    Base.metadata.create_all(engine)

    create_or_get_stock(
        market='NASDAQ',
        code='AAPL',
        name='USD - Apple Inc')
    create_or_get_stock(
        market='NASDAQ',
        code='GOOG',
        name='USD - Alphabet Inc')
    create_or_get_stock(
        market='NASDAQ',
        code='MSFT',
        name='USD - Microsoft Corporation')

    update_stocks_history()


if __name__ == '__main__':
    main()
