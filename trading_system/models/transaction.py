import sqlalchemy as sa
from .base import Base
from .stock import Stock
from .ticket import Ticket
from .user import User


class Transaction(Base):
    __tablename__ = 'transactions'

    id = sa.Column(sa.Integer, primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id))
    stock_id = sa.Column(sa.Integer, sa.ForeignKey(Stock.id))
    ticket_id = sa.Column(sa.Integer, sa.ForeignKey(Ticket.id))
    count = sa.Column(sa.Integer)
    total_price = sa.Column(sa.Float)
    time = sa.Column(sa.DateTime)
