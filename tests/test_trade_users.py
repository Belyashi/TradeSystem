from trading_system.models import User
from .base import BaseTestCase


class TestTradeUsers(BaseTestCase):
    def test_register(self):
        token = trading_system.trade.users.register(self.session)
        self.session.commit()

        user = self.session.query(User).one()
        self.assertEqual(user.token, token)

    def test_get_by_token(self):
        token = trading_system.trade.users.register(self.session)
        user = trading_system.trade.users.get_by_token(self.session, token)
        self.assertEqual(user.token, token)

