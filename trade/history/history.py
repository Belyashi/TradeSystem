from sqlalchemy import func

from db import session
from models import StockHistory


def get_history_range(stock_id):
    query = (session.query(
        func.min(StockHistory.time).label('min_time'),
        func.max(StockHistory.time).label('max_time'))
             .filter_by(stock_id=stock_id)
             .one())
    return query.min_time, query.max_time


def save_history(stock_id, history):
    if len(history) == 0:
        return

    min_time, max_time = get_history_range(stock_id)
    if min_time:
        data = history[(history['time'] < min_time) | (history['time'] > max_time)].copy()
    else:
        data = history.copy()

    data['stock_id'] = stock_id
    session.bulk_insert_mappings(
        StockHistory,
        data.T.to_dict().values()
    )
