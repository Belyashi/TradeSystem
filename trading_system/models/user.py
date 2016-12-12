import sqlalchemy as sa
from .base import Base


class User(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    username = sa.Column(sa.String(100), unique=True, nullable=False)
    password = sa.Column(sa.String(100), nullable=False)
