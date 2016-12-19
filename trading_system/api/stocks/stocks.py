import datetime

from flask import request
from flask.blueprints import Blueprint
from trading_system.models import Stock, StockHistory

from trading_system.api.utils import str_to_date, json_data
from trading_system.api.auth_middleware import auth_middleware
from trading_system.db import session
import trading_system

stocks = Blueprint('stocks', __name__, url_prefix='/stocks')
stocks.before_request(auth_middleware)


@stocks.route('/')
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


@stocks.route('/<tag>/history')
def stock_history(tag):
    stock = trading_system.trade.stocks.get_by_tag(session, tag)

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
