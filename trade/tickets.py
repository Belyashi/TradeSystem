import datetime

from db import session
from models import Ticket

from . import balance


def get_total_price(ticket):
    return ticket.count * ticket.price


def open_ticket(user_id, stock_id, count, price, buy, duration):
    ticket = Ticket(user_id=user_id,
                    stock_id=stock_id,
                    count=count,
                    price=price,
                    buy=buy,
                    open_time=datetime.datetime.now(),
                    duration=duration)
    session.add(ticket)
    session.flush()

    if buy:
        balance.transfer_money(user_id, -get_total_price(ticket))
    else:
        balance.transfer_stocks(user_id, stock_id, -count)

    return ticket


def close_ticket(ticket_id, success):
    ticket = session.query(Ticket).filter_by(id=ticket_id).one()
    ticket.opened = False

    if success == ticket.buy:
        balance.transfer_stocks(ticket.user_id, ticket.stock_id, ticket.count)
    else:
        balance.transfer_money(ticket.user_id, get_total_price(ticket))
