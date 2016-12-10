import sqlalchemy as sa
from .base import Base


class Stock(Base):
    __tablename__ = 'stocks'

    id = sa.Column(sa.Integer, primary_key=True)
    market = sa.Column(sa.String(50))
    code = sa.Column(sa.String(50))
    name = sa.Column(sa.String(50))

    @property
    def tag(self):
        return '{}-{}'.format(self.market, self.code).lower()
