import logging
import json

import server
from db import engine
from models import Base
from settings import SERVER_HOST, SERVER_PORT, STOCKS
from trade.history import HistoryUpdater
from trade.stocks import create_or_get_stock


def load_stocks():
    with open(STOCKS) as f:
        data = json.loads(f.read())
    for item in data:
        create_or_get_stock(**item)


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(message)s')

    Base.metadata.create_all(engine)

    load_stocks()

    updater = HistoryUpdater()
    updater.run()

    server.app.run(host=SERVER_HOST, port=SERVER_PORT)


if __name__ == '__main__':
    main()
