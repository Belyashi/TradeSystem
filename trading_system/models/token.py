import datetime
import dateutil
import sqlalchemy as sa
from .base import Base
from .user import User


def get_expiration_date():
    result = datetime.datetime.now() + dateutil.relativedelta(days=14)
    return result


class Token(Base):
    __tablename__ = 'tokens'

    id = sa.Column(sa.Integer, primary_key=True)
    token = sa.Column(sa.String(100), unique=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(User.id), nullable=False)
    expiration_date = sa.Column(
        sa.DateTime,
        default=get_expiration_date,
    )
