import copy
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
    kwargs = copy.copy(kwargs)
    if isinstance(data, list):
        result = [json_data(item, **kwargs) for item in data]
    elif isinstance(data, mx.Base):
        if isinstance(data, mx.Ticket):
            kwargs['exluded_keys'] = set('duration')
            result = data.__json__(**kwargs)
            result['duration'] = data.duration.total_seconds() / 60

        else:
            result = data.__json__(**kwargs)

    return jsonify(result)
