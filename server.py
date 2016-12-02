import datetime

from flask import Flask, request, jsonify

from db import session
from models import Stock, StockHistory
import trade
from utils import str_to_date

app = Flask(__name__)


def json_data(data):
    return jsonify({'data': data})


@app.route('/users/register')
def user_register():
    token = trade.users.register()
    return json_data({'token': token})


@app.route('/stocks')
def stocks_list():
    data = []
    for stock in session.query(Stock):
        data.append({
            'market': stock.market,
            'code': stock.code,
            'name': stock.name,
            'tag': trade.stocks.get_tag(stock),
        })
    return json_data(data)


@app.route('/stocks/<tag>/history')
def stock_history(tag):
    stock = trade.stocks.get_by_tag(tag)

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
