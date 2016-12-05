import trade
from models import User
from .base import BaseTestCase


class TestTradeUsers(BaseTestCase):
    def test_register(self):
        token = trade.users.register(self.session)
        self.session.commit()

        user = self.session.query(User).one()
        self.assertEqual(user.token, token)

    def test_get_by_token(self):
        token = trade.users.register(self.session)
        user = trade.users.get_by_token(self.session, token)
        self.assertEqual(user.token, token)

