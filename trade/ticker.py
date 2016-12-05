from sqlalchemy import and_

from models import StockHistory


def get_trade_moment(session, ticket, from_time=None):
    criterion = [StockHistory.stock_id == ticket.stock_id]
    if ticket.buy:
        criterion.append(StockHistory.price <= ticket.price)
    else:
        criterion.append(StockHistory.price >= ticket.price)
    if from_time:
        criterion.append(StockHistory.time >= from_time)

    trade = (session
             .query(StockHistory)
             .order_by(StockHistory.time)
             .filter(and_(*criterion))
             .first())

    return trade.time if trade else None
