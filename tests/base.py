import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

import trade
from models import Base


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def tearDown(self):
        Base.metadata.drop_all(self.engine)


class BaseUserTestCase(BaseTestCase):
    def setUp(self):
        super(BaseUserTestCase, self).setUp()

        token = trade.users.register(self.session)
        user = trade.users.get_by_token(self.session, token)
        self.user_id = user.id
