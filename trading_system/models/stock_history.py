import sqlalchemy as sa
from .base import Base
from .stock import Stock


class StockHistory(Base):
    __tablename__ = 'stock_history'

    id = sa.Column(sa.Integer, primary_key=True)
    stock_id = sa.Column(sa.Integer, sa.ForeignKey(Stock.id))
    time = sa.Column(sa.DateTime(timezone=True))
    volume = sa.Column(sa.Integer)
    price = sa.Column(sa.Float)