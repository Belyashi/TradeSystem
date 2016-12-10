import sqlalchemy as sa
from .base import Base
from .stock import Stock
from .user import User


class Ticket(Base):
    __tablename__ = 'tickets'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    stock_id = sa.Column(sa.Integer, sa.ForeignKey(Stock.id))
    count = sa.Column(sa.Integer)
    price = sa.Column(sa.Float)
    buy = sa.Column(sa.Boolean)
    opened = sa.Column(sa.Boolean, default=True)
    open_time = sa.Column(sa.DateTime)
    duration = sa.Column(sa.Interval)

    @property
    def total_price(self):
        return self.count * self.price
