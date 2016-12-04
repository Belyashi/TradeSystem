import logging
import json

import server
from db import engine, session
from models import Base
from settings import SERVER_HOST, SERVER_PORT, STOCKS
import trade
from trade.stock_history.update import StockHistoryUpdater


def load_stocks():
    with open(STOCKS) as f:
        data = json.loads(f.read())

    trade.stocks.create_stocks(session, data)


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s')

    Base.metadata.create_all(engine)

    load_stocks()

    updater = StockHistoryUpdater(session)
    updater.run()

    server.app.run(host=SERVER_HOST, port=SERVER_PORT)

    updater.stop()


if __name__ == '__main__':
    main()
