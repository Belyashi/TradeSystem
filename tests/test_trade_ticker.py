import datetime

import pandas as pd
import numpy as np

import trade
from .base import BaseUserTestCase


def _create_history(session, prices, start_time=None, stock_code=None):
    stock = trade.stocks.create_or_get_stock(
        session,
        market='MARKET',
        code=stock_code or 'CODE'
    )

    start_time = start_time or datetime.datetime(2016, 12, 5)

    count = len(prices)
    history = pd.DataFrame({
        'time': start_time + np.arange(count) * datetime.timedelta(seconds=5),
        'volume': 100,
        'price': prices
    })
    trade.stock_history.save_history(
        session,
        stock.id,
        history
    )
    return history, stock.id


def _get_trade_moment(session, user_id, stock_id, price, buy, from_time=None):
    ticket = trade.tickets.open_ticket(
        session,
        user_id,
        stock_id,
        100,
        price,
        buy,
        datetime.timedelta(days=10)
    )

    trade_time = trade.ticker.get_trade_moment(
        session,
        ticket,
        from_time
    )
    return trade_time


def date_from_str(s):
    return datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


class TestTradeTicker(BaseUserTestCase):
    def test_get_trade_moment_buy_less(self):
        prices = np.concatenate([
            np.arange(100., 50., -1.),
            np.arange(50., 100., 1.)
        ])
        history, trade_time = self._test_get_trade_moment(
            prices,
            69.95,
            True
        )
        self.assertEqual(trade_time, date_from_str('2016-12-05 00:02:35'))

    def test_get_trade_moment_buy_equal(self):
        history, trade_time = self._test_get_trade_moment(
            np.arange(100., 50., -1.),
            85.,
            True
        )
        self.assertEqual(trade_time, date_from_str('2016-12-05 00:01:15'))

    def test_get_trade_moment_sell_more(self):
        prices = np.concatenate([
            np.arange(50., 100., 1.),
            np.arange(100., 50., -1.)
        ])
        history, trade_time = self._test_get_trade_moment(
            prices,
            70.01,
            False
        )
        self.assertEqual(trade_time, date_from_str('2016-12-05 00:01:45'))

    def test_get_trade_moment_sell_equal(self):
        history, trade_time = self._test_get_trade_moment(
            np.arange(50., 100., 1.),
            61.,
            False
        )
        self.assertEqual(trade_time, date_from_str('2016-12-05 00:00:55'))

    def test_get_trade_moment_stocks_filter(self):
        prices = np.arange(100., 50., -1.)
        _create_history(
            self.session,
            prices,
            start_time=datetime.datetime(2016, 11, 1),
            stock_code='ANOTHER_STOCK'
        )
        history, trade_time = self._test_get_trade_moment(
            prices,
            85.,
            True
        )
        self.assertEqual(trade_time, date_from_str('2016-12-05 00:01:15'))

    def test_get_trade_moment_from_time_filter(self):
        prices = np.concatenate([
            np.arange(50., 100., 1.),
            np.arange(50., 100., 1.)
        ])
        history, trade_time = self._test_get_trade_moment(
            prices,
            70.01,
            False,
            from_time=date_from_str('2016-12-05 00:04:15')
        )
        self.assertEqual(trade_time, date_from_str('2016-12-05 00:05:55'))

    def _test_get_trade_moment(self, prices, ticket_price, ticket_buy, from_time=None):
        history, stock_id = _create_history(
            self.session,
            prices
        )

        trade_time = _get_trade_moment(
            self.session,
            self.user_id,
            stock_id,
            ticket_price,
            ticket_buy,
            from_time
        )

        return history, trade_time

    def test_process_ticket_close_expired(self):
        stock = trade.stocks.create_or_get_stock(
            self.session,
            market='MARKET',
            code='CODE'
        )

        ticket = trade.tickets.open_ticket(
            self.session,
            self.user_id,
            stock.id,
            100, 55.5, True,
            datetime.timedelta(minutes=5)
        )
        ticket.open_time = date_from_str('2016-12-05 00:00:00')

        trade.ticker.process_tickets(
            self.session,
            None,
            date_from_str('2016-12-05 00:04:55')
        )

        self.assertTrue(ticket.opened)

        trade.ticker.process_tickets(
            self.session,
            None,
            date_from_str('2016-12-05 00:05:10')
        )

        self.assertFalse(ticket.opened)

    def test_process_ticket_close_succeed(self):
        pass