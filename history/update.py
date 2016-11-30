import datetime
import logging
import time

import pytz

from db import session
from history import finamru_api
from models import Stock
from settings import HISTORY_DAYS_BEFORE, HISTORY_LOAD_BATCH
from .history import get_history_range, save_history


def _get_update_date_range(stock_id, first_date, last_date):
    api_tz = pytz.timezone(finamru_api.TIMEZONE)

    min_time, max_time = get_history_range(stock_id)
    min_date = api_tz.fromutc(min_time).date() if min_time else None
    max_date = api_tz.fromutc(max_time).date() if max_time else None

    max_batch_delta = datetime.timedelta(days=HISTORY_LOAD_BATCH - 1) if HISTORY_LOAD_BATCH else None
    if max_date and last_date >= min_date:
        if max_date < last_date:
            from_date = max_date + datetime.timedelta(days=1)
            to_date = min(last_date, from_date + max_batch_delta) if HISTORY_LOAD_BATCH else last_date
        elif first_date < min_date:
            to_date = min_date - datetime.timedelta(days=1)
            from_date = max(first_date, to_date - max_batch_delta) if HISTORY_LOAD_BATCH else first_date
        else:
            from_date, to_date = None, None
    else:
        to_date = last_date
        from_date = max(first_date, to_date - max_batch_delta) if HISTORY_LOAD_BATCH else first_date

    return from_date, to_date


def _update_stock_history(market, code):
    stock = session.query(Stock).filter_by(market=market, code=code).one()

    last_date = datetime.datetime.now().date() - datetime.timedelta(days=1)
    first_date = last_date - datetime.timedelta(days=HISTORY_DAYS_BEFORE - 1)
    while first_date <= last_date:
        from_date, to_date = _get_update_date_range(stock.id, first_date, last_date)
        if not from_date:
            break

        t0 = time.time()

        try:
            history = finamru_api.load_history(
                market=market,
                code=code,
                from_date=from_date,
                to_date=to_date)
        except finamru_api.FinamRuException as e:
            logging.error('{}.{} not updated: {}'.format(market, code, str(e)))
            return
        except Exception as e:
            logging.exception(e)
            return

        save_history(stock.id, history)
        session.commit()

        t1 = time.time()

        logging.info('{}.{} updated from {} to {} ({:2f} seconds)'
                     .format(market, code, from_date, to_date, t1 - t0))

        last_date = from_date - datetime.timedelta(days=1)


def update_stocks_history():
    logging.info('updating stocks...')
    for stock in session.query(Stock):
        _update_stock_history(stock.market, stock.code)
    logging.info('updating stocks finished')