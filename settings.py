import datetime

DATABASE = 'mysql://root@localhost:3306/trade'

HISTORY_DAYS_BEFORE = 10
HISTORY_LOAD_BATCH = 2
HISTORY_UPDATE_TIMEDELTA = datetime.timedelta(minutes=1)

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000

STOCKS = './stocks.json'
