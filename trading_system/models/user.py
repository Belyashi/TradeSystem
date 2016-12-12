import sqlalchemy as sa
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    token = sa.Column(sa.String(50), unique=True)
