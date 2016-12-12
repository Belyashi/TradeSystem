import sqlalchemy as sa
from .base import Base
from .user import User
from .stock import Stock


class StockBalance(Base):
    __tablename__ = 'stock_balance'

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), primary_key=True)
    stock_id = sa.Column(sa.Integer, sa.ForeignKey(Stock.id), primary_key=True)
    value = sa.Column(sa.Integer)
