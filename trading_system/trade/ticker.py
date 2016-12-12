import datetime
import logging
import time
from threading import Thread

from sqlalchemy import and_

from trading_system.models import Ticket, StockHistory
from . import tickets

logger = logging.getLogger(__name__)


def get_trade_moment(session, ticket, from_time=None, to_time=None):
    criterion = [StockHistory.stock_id == ticket.stock_id]
    if ticket.buy:
        criterion.append(StockHistory.price <= ticket.price)
    else:
        criterion.append(StockHistory.price >= ticket.price)
    if from_time:
        criterion.append(StockHistory.time >= from_time)
    if to_time:
        criterion.append(StockHistory.time < to_time)

    trade = (session
             .query(StockHistory)
             .order_by(StockHistory.time)
             .filter(and_(*criterion))
             .first())

    return trade.time if trade else None


def _get_expired_tickets(session, current_time):
    # NOT WORKS -> tickets = (session.query(Ticket).filter(and_(Ticket.opened, (Ticket.open_time + Ticket.duration) < current_time)))
    tickets = [ticket for ticket in session.query(Ticket).filter(Ticket.opened)
               if (ticket.open_time + ticket.duration) < current_time]
    return tickets


def process_tickets(session, last_process_time, current_time):
    for ticket in _get_expired_tickets(session, current_time):
        tickets.close_ticket(session, ticket.id, False)

    for ticket in session.query(Ticket).filter_by(opened=True):
        trade_time = get_trade_moment(session, ticket,
                                      from_time=last_process_time or ticket.open_time,
                                      to_time=current_time)
        if trade_time:
            tickets.close_ticket(session, ticket.id, success=True)

    return current_time


class Ticker(object):
    TICKER_PERIOD = 5.

    def __init__(self, session):
        self._session = session

        self._thread = Thread(target=self._loop)
        self._active = False

    def run(self):
        if not self._active:
            self._active = True
            self._thread.start()

    def stop(self):
        if self._active:
            self._active = False

    def _loop(self):
        last_process_time = None
        while self._active:
            try:
                last_process_time = process_tickets(self._session,
                                                    last_process_time,
                                                    datetime.datetime.utcnow())
            except Exception as e:
                logger.exception(e)

            time.sleep(Ticker.TICKER_PERIOD)
