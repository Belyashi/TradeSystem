from flask import request
from flask.blueprints import Blueprint

import trade
from db import session
from models import Stock, StockHistory
from utils import str_to_date, json_data


stocks = Blueprint('stocks', __name__)


@stocks.route('/stocks')
def stocks_list():
    data = []
    for stock in session.query(Stock):
        data.append({
            'market': stock.market,
            'code': stock.code,
            'name': stock.name,
            'tag': stock.tag,
        })
    return json_data(data)


@stocks.route('/stocks/<tag>/history')
def stock_history(tag):
    stock = trade.stocks.get_by_tag(session, tag)

    from_date = str_to_date(request.args.get('from_date'))
    to_date = str_to_date(request.args.get('to_date'))

    criterion = [StockHistory.stock_id == stock.id]
    if from_date:
        criterion.append(StockHistory.time >= from_date)
    if to_date:
        criterion.append(StockHistory.time < (to_date + datetime.timedelta(days=1)))

    query = session.query(StockHistory).filter(*criterion).order_by(StockHistory.time)

    data = []
    for item in query:
        data.append({
            'time': item.time,
            'volume': item.volume,
            'price': item.price
        })
    return json_data(data)
