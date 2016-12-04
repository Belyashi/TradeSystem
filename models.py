from sqlalchemy import Column, Integer, Float, Interval, Boolean, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    token = Column(String(50), unique=True)


class Balance(Base):
    __tablename__ = 'balance'

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    value = Column(Float, default=0.)


class Stock(Base):
    __tablename__ = 'stocks'

    id = Column(Integer, primary_key=True)
    market = Column(String(50))
    code = Column(String(50))
    name = Column(String(50))

    @property
    def tag(self):
        return '{}-{}'.format(self.market, self.code).lower()


class StockHistory(Base):
    __tablename__ = 'stock_history'

    id = Column(Integer, primary_key=True)
    stock_id = Column(Integer, ForeignKey(Stock.id))
    time = Column(DateTime(timezone=True))
    volume = Column(Integer)
    price = Column(Float)


class StockBalance(Base):
    __tablename__ = 'stock_balance'

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    stock_id = Column(Integer, ForeignKey(Stock.id), primary_key=True)
    value = Column(Integer)


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    stock_id = Column(Integer, ForeignKey(Stock.id))
    count = Column(Integer)
    price = Column(Float)
    buy = Column(Boolean)
    opened = Column(Boolean, default=True)
    open_time = Column(DateTime)
    duration = Column(Interval)

    @property
    def total_price(self):
        return self.count * self.price


class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey(User.id))
    stock_id = Column(Integer, ForeignKey(Stock.id))
    ticket_id = Column(Integer, ForeignKey(Ticket.id))
    count = Column(Integer)
    total_price = Column(Float)
    time = Column(DateTime)
