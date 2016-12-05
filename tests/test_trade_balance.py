from collections import defaultdict

from models import Balance, StockBalance
import trade
from .base import BaseUserTestCase


class TestTradeBalance(BaseUserTestCase):
    def test_transfer_money(self):
        deltas = [100.23, -50.01, -90.67, 1010.]
        expected_value = 0.
        for delta in deltas:
            trade.balance.transfer_money(self.session, self.user_id, delta)
            expected_value += delta

            balance = self.session.query(Balance).one()
            self.assertEqual(balance.value, expected_value)

    def test_get_money(self):
        deltas = [100.23, -50.01, -90.67, 1010.]
        expected_value = 0.

        value = trade.balance.get_money(self.session, self.user_id)
        self.assertEqual(value, expected_value)
        for delta in deltas:
            trade.balance.transfer_money(self.session, self.user_id, delta)
            expected_value += delta

            value = trade.balance.get_money(self.session, self.user_id)
            self.assertEqual(value, expected_value)

    def test_transfer_stocks(self):
        stock_ids = [trade.stocks.create_or_get_stock(self.session, 'TEST', 'CODE{}'.format(i)).id
                     for i in range(2)]
        deltas = [(stock_ids[0], 5), (stock_ids[1], -3), (stock_ids[0], 10), (stock_ids[1], 8)]
        expected_values = defaultdict(int)
        for stock_id, delta in deltas:
            trade.balance.transfer_stocks(self.session, self.user_id, stock_id, delta)
            expected_values[stock_id] += delta

            balance = self.session.query(StockBalance).filter_by(stock_id=stock_id).one()
            self.assertEqual(balance.value, expected_values[stock_id])

    def test_get_stocks(self):
        stock_ids = [trade.stocks.create_or_get_stock(self.session, 'TEST', 'CODE{}'.format(i)).id
                     for i in range(2)]
        deltas = [(stock_ids[0], 5), (stock_ids[1], -3), (stock_ids[0], 10), (stock_ids[1], 8)]
        expected_values = defaultdict(int)

        value = trade.balance.get_stocks(self.session, self.user_id, stock_ids[0])
        self.assertEqual(value, expected_values[stock_ids[0]])
        for stock_id, delta in deltas:
            trade.balance.transfer_stocks(self.session, self.user_id, stock_id, delta)
            expected_values[stock_id] += delta

            value = trade.balance.get_stocks(self.session, self.user_id, stock_ids[0])
            self.assertEqual(value, expected_values[stock_ids[0]])