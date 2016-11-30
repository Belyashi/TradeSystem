import datetime
import time


def str_to_date(s):
    if s is None:
        return None

    t = time.strptime(s, '%d.%m.%Y')
    date = datetime.date(year=t.tm_year, month=t.tm_mon, day=t.tm_mday)

    return date