import json
import logging

from trading_system.models import Base

from trading_system.api import server
from trading_system.db import engine, session
from trading_system.settings import SERVER_HOST, SERVER_PORT, STOCKS
from trading_system.trade.stock_history.update import StockHistoryUpdater
import trading_system


def load_stocks():
    with open(STOCKS) as f:
        data = json.loads(f.read())

    trading_system.trade.stocks.create_stocks(session, data)


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
