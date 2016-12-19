import datetime
import time
from flask import jsonify
from trading_system import models as mx


def str_to_date(s):
    if s is None:
        return None

    t = time.strptime(s, '%d.%m.%Y')
    date = datetime.date(year=t.tm_year, month=t.tm_mon, day=t.tm_mday)

    return date


def json_data(data, **kwargs):
    """Serialize data into json. If data is list then it MUST be sequence of
        similar objects.
    :param kwargs: support kwarg `excluded_keys` for non-serializable fields
        of SQLAlchemy models
    """
    if isinstance(data, list):
        if data and isinstance(data[0], mx.Base):
            data = [item.__json__(**kwargs) for item in data]
    elif isinstance(data, mx.Base):
        data = data.__json__(**kwargs)

    return jsonify(data)
