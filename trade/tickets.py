import datetime

from models import Ticket

from . import balance


def open_ticket(session, user_id, stock_id, count, price, buy, duration):
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
        balance.transfer_money(session, user_id, -ticket.total_price)
    else:
        balance.transfer_stocks(session, user_id, stock_id, -count)

    return ticket


def close_ticket(session, ticket_id, success):
    ticket = session.query(Ticket).filter_by(id=ticket_id).one()
    ticket.opened = False

    if success == ticket.buy:
        balance.transfer_stocks(session, ticket.user_id, ticket.stock_id, ticket.count)
    else:
        balance.transfer_money(session, ticket.user_id, ticket.total_price)
