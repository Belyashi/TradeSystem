import datetime
from unittest import mock

from trading_system.models import Ticket
from .base import BaseUserTestCase


def create_ticket(session, user_id, count=None, price=None, buy=True, duration=None):
    count = 30 if count is None else count
    price = 765.31 if price is None else price
    duration = duration or datetime.timedelta(hours=3)

    stock = trading_system.trade.stocks.create_or_get_stock(
        session,
        market='MARKET',
        code='CODE'
    )

    ticket = trading_system.trade.tickets.open_ticket(
        session,
        user_id=user_id,
        stock_id=stock.id,
        count=count,
        price=price,
        buy=buy,
        duration=duration
    )

    return ticket, stock.id


class TestTradeTickets(BaseUserTestCase):
    @mock.patch('trade.balance.transfer_stocks')
    @mock.patch('trade.balance.transfer_money')
    def test_open_ticket_buy(self, transfer_money, transfer_stocks):
        ticket_count = 10
        ticket_price = 100.15
        ticket_duration = datetime.timedelta(hours=3)
        ticket, stock_id = create_ticket(
            self.session,
            self.user_id,
            ticket_count,
            ticket_price,
            True,
            ticket_duration
        )

        self.assertIsNotNone(ticket.id)
        ticket_ = self.session.query(Ticket).one()
        self.assertEqual(ticket.id, ticket_.id)
        self.assertEqual(ticket.user_id, self.user_id)
        self.assertEqual(ticket.stock_id, stock_id)
        self.assertEqual(ticket.count, ticket_count)
        self.assertEqual(ticket.price, ticket_price)
        self.assertTrue(ticket.buy)
        self.assertTrue(ticket.opened)
        self.assertEqual(ticket.duration, ticket_duration)
        self.assertEqual(ticket.total_price, ticket_count * ticket_price)

        transfer_money.assert_called_once_with(
            self.session,
            self.user_id,
            -ticket.total_price
        )

        transfer_stocks.assert_not_called()

    @mock.patch('trade.balance.transfer_stocks')
    @mock.patch('trade.balance.transfer_money')
    def test_open_ticket_sell(self, transfer_money, transfer_stocks):
        ticket, stock_id = create_ticket(
            self.session,
            self.user_id,
            buy=False,
        )

        transfer_money.assert_not_called()
        transfer_stocks.assert_called_once_with(
            self.session,
            self.user_id,
            stock_id,
            -ticket.count
        )

    def test_open_ticket_wrong_count_and_price(self):
        with self.assertRaises(ValueError):
            create_ticket(self.session, self.user_id, count=0)

        with self.assertRaises(ValueError):
            create_ticket(self.session, self.user_id, count=-10)

        with self.assertRaises(ValueError):
            create_ticket(self.session, self.user_id, price=0.)

        with self.assertRaises(ValueError):
            create_ticket(self.session, self.user_id, price=-100.55)

    @mock.patch('trade.balance.transfer_stocks')
    @mock.patch('trade.balance.transfer_money')
    def test_close_ticket_buy_success(self, transfer_money, transfer_stocks):
        ticket, _ = create_ticket(
            self.session,
            self.user_id,
            buy=True
        )
        transfer_money.reset_mock()
        transfer_stocks.reset_mock()

        trading_system.trade.tickets.close_ticket(self.session, ticket.id, success=True)

        self.assertFalse(ticket.opened)
        transfer_money.assert_not_called()
        transfer_stocks.assert_called_once_with(
            self.session,
            self.user_id,
            ticket.stock_id,
            ticket.count
        )

    @mock.patch('trade.balance.transfer_stocks')
    @mock.patch('trade.balance.transfer_money')
    def test_close_ticket_sell_success(self, transfer_money, transfer_stocks):
        ticket, _ = create_ticket(
            self.session,
            self.user_id,
            buy=False
        )
        transfer_money.reset_mock()
        transfer_stocks.reset_mock()

        trading_system.trade.tickets.close_ticket(self.session, ticket.id, success=True)

        transfer_money.assert_called_once_with(
            self.session,
            self.user_id,
            ticket.total_price
        )
        transfer_stocks.assert_not_called()

    @mock.patch('trade.balance.transfer_stocks')
    @mock.patch('trade.balance.transfer_money')
    def test_close_ticket_buy_not_success(self, transfer_money, transfer_stocks):
        ticket, _ = create_ticket(
            self.session,
            self.user_id,
            buy=True
        )
        transfer_money.reset_mock()
        transfer_stocks.reset_mock()

        trading_system.trade.tickets.close_ticket(self.session, ticket.id, success=False)

        transfer_money.assert_called_once_with(
            self.session,
            self.user_id,
            ticket.total_price
        )
        transfer_stocks.assert_not_called()

    @mock.patch('trade.balance.transfer_stocks')
    @mock.patch('trade.balance.transfer_money')
    def test_close_ticket_sell_not_success(self, transfer_money, transfer_stocks):
        ticket, _ = create_ticket(
            self.session,
            self.user_id,
            buy=False
        )
        transfer_money.reset_mock()
        transfer_stocks.reset_mock()

        trading_system.trade.tickets.close_ticket(self.session, ticket.id, success=False)

        transfer_money.assert_not_called()
        transfer_stocks.assert_called_once_with(
            self.session,
            self.user_id,
            ticket.stock_id,
            ticket.count
        )

    def test_close_not_opened_ticket(self):
        ticket, _ = create_ticket(
            self.session,
            self.user_id,
            buy=False
        )
        ticket.opened = False

        with self.assertRaises(ValueError):
            trading_system.trade.tickets.close_ticket(self.session, ticket.id, success=False)