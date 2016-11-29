import datetime
import time

from sqlalchemy.orm.exc import NoResultFound

from db import engine, session
from models import Base, Stock, StockHistory

import finamru_api


def save_history(market, code, history):
    try:
        stock = session.query(Stock).filter_by(market=market, code=code).one()
    except NoResultFound:
        stock = Stock(market=market,
                      code=code,
                      name='{}.{}'.format(market, code))
        session.add(stock)
        session.flush()

    data = history[['time', 'volume', 'price']].copy()
    data['stock_id'] = stock.id
    session.bulk_insert_mappings(
        StockHistory,
        data.T.to_dict().values()
    )


def main():
    Base.metadata.create_all(engine)

    market = 'NASDAQ'
    code = 'AAPL'

    history = finamru_api.load_history(
        market=market,
        code=code,
        from_date=datetime.date(2016, 11, 20),
        to_date=datetime.date(2016, 11, 21))

    print('loaded')
    t0 = time.time()
    save_history(market, code, history)
    t1 = time.time()
    print('saved')
    session.commit()
    print('finished in {:2f} seconds'.format(t1 - t0))


if __name__ == '__main__':
    main()
