import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Base, User
import trade


class TestTradeUser(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)

    def test_register(self):
        token = trade.users.register(self.session)
        self.session.commit()

        users = self.session.query(User).all()
        self.assertEqual(len(users), 1)

        user = users[0]
        self.assertEqual(user.token, token)

    def test_get_by_token(self):
        token = trade.users.register(self.session)
        user = trade.users.get_by_token(self.session, token)
        self.assertEqual(user.token, token)

