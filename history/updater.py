import logging
import datetime
import time
import pytz

from sqlalchemy import func
from sqlalchemy.orm.exc import NoResultFound

from db import engine, session
from history import finamru_api
from models import Base, Stock, StockHistory


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


def get_stock_history_range(stock_id):
    query = (session.query(
        func.min(StockHistory.time).label('min_time'),
        func.max(StockHistory.time).label('max_time'))
             .filter(StockHistory.stock_id == stock_id)
             .one())
    return query.min_time, query.max_time


def save_history(stock_id, history):
    if len(history) == 0:
        return

    data = history.copy()
    data['stock_id'] = stock_id
    session.bulk_insert_mappings(
        StockHistory,
        data.T.to_dict().values()
    )


def get_update_date_range(stock_id, first_date, last_date, max_batch=None):
    api_tz = pytz.timezone(finamru_api.TIMEZONE)

    min_time, max_time = get_stock_history_range(stock_id)
    min_date = api_tz.fromutc(min_time).date() if min_time else None
    max_date = api_tz.fromutc(max_time).date() if max_time else None

    max_batch_delta = datetime.timedelta(days=max_batch - 1) if max_batch else None
    if max_date and last_date >= min_date:
        if max_date < last_date:
            from_date = max_date + datetime.timedelta(days=1)
            to_date = min(last_date, from_date + max_batch_delta) if max_batch else last_date
        elif first_date < min_date:
            to_date = min_date - datetime.timedelta(days=1)
            from_date = max(first_date, to_date - max_batch_delta) if max_batch else first_date
        else:
            from_date, to_date = None, None
    else:
        to_date = last_date
        from_date = max(first_date, to_date - max_batch_delta) if max_batch else first_date

    return from_date, to_date


def update_stock_history(market, code, days_before, max_batch=None):
    stock = session.query(Stock).filter_by(market=market, code=code).one()

    last_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    first_date = last_date - datetime.timedelta(days=days_before - 1)
    while first_date <= last_date:
        from_date, to_date = get_update_date_range(stock.id, first_date, last_date, max_batch)
        if not from_date:
            break

        t0 = time.time()

        history = finamru_api.load_history(
            market=market,
            code=code,
            from_date=from_date,
            to_date=to_date)

        save_history(stock.id, history)
        session.commit()

        t1 = time.time()

        logging.info('{}.{} updated from {} to {} ({:2f} seconds)'
                     .format(market, code, from_date, to_date, t1 - t0))

        last_date = from_date - datetime.timedelta(days=1)


def update_stocks_history(days_before=None, max_batch=None):
    logging.info('updating stocks...')
    for stock in session.query(Stock):
        update_stock_history(stock.market, stock.code, days_before, max_batch)
    logging.info('updating stocks finished')


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s')

    Base.metadata.create_all(engine)

    create_or_get_stock(
        market='NASDAQ',
        code='AAPL',
        name='USD - Apple Inc')

    update_stocks_history(days_before=10, max_batch=5)

if __name__ == '__main__':
    main()
