import logging
import datetime

from db import engine, session
from models import Base
import trade


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s')

    Base.metadata.create_all(engine)

    token = trade.users.register()
    user = trade.users.get_by_token(token)

    stock = trade.stocks.get_by_tag('nasdaq-goog')

    # trade.tickets.open_ticket(user.id, stock.id, 10, 99.5, True, datetime.timedelta(days=1))
    trade.tickets.close_ticket(3, False)

    session.commit()


if __name__ == '__main__':
    main()
