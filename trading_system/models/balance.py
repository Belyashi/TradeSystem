import sqlalchemy as sa
from .base import Base
from .user import User


class Balance(Base):
    __tablename__ = 'balance'

    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), primary_key=True)
    value = sa.Column(sa.Float, default=0.)
