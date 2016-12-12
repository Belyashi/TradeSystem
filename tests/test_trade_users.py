from trading_system import models as mx
from .base import BaseTestCase

import trading_system


class TestTradeUsers(BaseTestCase):
    def test_register(self):
        token = trading_system.trade.users.register(self.session, 'user1', 'passw')
        self.session.commit()

        got_token = self.session.query(mx.Token).join(mx.User, mx.Token.user_id == mx.User.id).one()
        self.assertEqual(got_token.token, token)

    def test_get_by_token(self):
        token = trading_system.trade.users.register(self.session, 'user1', 'passw')

        user = trading_system.trade.users.get_by_token(self.session, token)

        got_token = (
            self.session.query(mx.Token)
            .join(mx.User, mx.User.id == mx.Token.user_id)
            .filter(mx.User.id == user.id)
            .one()
        )

        self.assertEqual(got_token.token, token)
